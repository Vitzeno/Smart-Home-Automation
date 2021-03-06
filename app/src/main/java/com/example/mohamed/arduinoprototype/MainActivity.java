package com.example.mohamed.arduinoprototype;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.fragment.app.FragmentManager;

import android.app.AlertDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.material.navigation.NavigationView;

import org.w3c.dom.Text;

import java.sql.Time;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.HashMap;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MainActivity extends AppCompatActivity implements NavigationView.OnNavigationItemSelectedListener {

    //Enum used to keep track of the current fragment in the foreground
    public enum fragmentState{RULE,SENSOR,DEVICE, BLUETOOTH}
    private fragmentState fragState;
    //req is used to fetch data once a connection is made for early list population
    private int req = 0;

    //These five ints are used to respond appropriately to the signals received from the BTservice class
    public static final int MESSAGE_STATE_CHANGE = 1;
    public static final int MESSAGE_READ = 2;
    public static final int MESSAGE_WRITE = 3;
    public static final int MESSAGE_DEVICE_NAME = 4;
    public static final int MESSAGE_TOAST = 5;

    //Default string values for a few of the generic internal outputs. Almost always overwritten elsewhere
    public static final String DEVICE_NAME = "device_name";
    public static final String INCOMING_DATA = "incoming_data";
    public static final String TOAST = "toast";

    private String mConnectedDeviceName = null;
    private DrawerLayout drawer;
    public NavigationView navView;

    //Output/Input string buffers for the send/write functions for the BTservice.
    public StringBuffer outStringBuff = new StringBuffer("");
    public StringBuffer inStringBuff = new StringBuffer("");
    public BTService BTservice;

    // Bluetooth adaptor to use
    public BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    // List of previously paired devices, pairing is required before connecting
    public Set<BluetoothDevice> pairedDevices;
    // Bluetooth request code
    int REQUEST_ENABLE_BT = 1;

    // The list view of bluetooth devices, deprecated, now in Bluetooth Fragment
    public ListView lstView;
    // Adapter, Arraylists and the hashmap of values corresponding to the bluetooth devices that are available in the general area.
    public ArrayAdapter<String> arrayAdapter;
    public ArrayList<String> deviceNames = new ArrayList<>();
    public ArrayList<String> macAddresses = new ArrayList<>();
    public HashMap<String, String> listOfDevices = new HashMap<String, String>();

    // Adapter, Arraylists and the hashmap of values corresponding to the rules that are available on the server.
    public ArrayAdapter<String> ruleAdaptor;
    public ArrayList<String> ruleList = new ArrayList<>();
    public ArrayList<String> formattedRules = new ArrayList<>();
    public ArrayList<String> ruleIDList = new ArrayList<>();
    public HashMap<String,String> listOfRules = new HashMap<>();

    // Adapter, Arraylists and the hashmap of values corresponding to the sensor devices that are available on the server.
    public ArrayAdapter<String> sensorAdaptor;
    public ArrayList<String> sensorList = new ArrayList<>();
    public ArrayList<String> sensorIDList = new ArrayList<>();
    public HashMap<String,String> listOfSensors = new HashMap<>();

    // Adapter, Arraylists and the hashmap of values corresponding to the devices that are available on the server.
    public ArrayAdapter<String> ObjAdaptor;
    public ArrayList<String> ObjList = new ArrayList<>();
    public ArrayList<String> formattedObjs = new ArrayList<>();
    public ArrayList<String> ObjIDList = new ArrayList<>();
    public HashMap<String,String> listOfObjs = new HashMap<>();

    //Fragment manager which will allow this activity to handle and keep track of the fragments it makes
    public FragmentManager fm = getSupportFragmentManager();
    // A reference to each of the fragments available from this activity
    public BluetoothFragment btfm;
    public RuleFragment rlfm;
    public SensorFragment snfm;
    public DeviceFragment dvfm;

    /**
     * This method handles the initialisation of the app. It starts the BTService and registers to broadcast receivers.
     * */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = findViewById(R.id.Toolbar);
        setSupportActionBar(toolbar);
        drawer = findViewById(R.id.drawer_layout);
        navView = findViewById(R.id.nav_view);
        navView.setNavigationItemSelectedListener(this);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();

        btfm = (BluetoothFragment) fm.findFragmentByTag("BTFrag");
        if(btfm == null)
            Log.d("aaaa", "No fragment yet...");

        // Check if device supports bluetooth
        if (bluetoothAdapter == null) {
            AlertDialog alertDialog = new AlertDialog.Builder(MainActivity.this).create();
            alertDialog.setTitle("Error");
            alertDialog.setMessage("Your device does not support bluetooth");
            alertDialog.setButton(AlertDialog.BUTTON_NEUTRAL, "CLOSE",
                    new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int which) {
                            dialog.dismiss();
                            finish();
                        }
                    });
            alertDialog.show();
        }

        requestBluetooth();
        // Register for broadcasts when a device is discovered.
        IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
        filter.addAction(BluetoothAdapter.ACTION_DISCOVERY_STARTED);
        filter.addAction(BluetoothAdapter.ACTION_DISCOVERY_FINISHED);
        registerReceiver(receiver, filter);

        populateListView();

        BTservice = new BTService(this, mHandler);
        BTservice.start();

        if(savedInstanceState == null)
        {
            getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container, new BluetoothFragment(), "BTFrag").addToBackStack(null).commit();
            navView.setCheckedItem(R.id.nav_bluetooth);
        }
    }

    /**
     * Handles the Navigation bar, starting the correct fragment based on user input.
     * A new fragment is loaded and given an id to be used later and then added to the backstack.
     * Once something is selected, the bar is closed.
     * @param menuItem The item on the navigation bar that was pressed down
     * */
    @Override
    public boolean onNavigationItemSelected(@NonNull MenuItem menuItem) {
        Log.d("aaaa", "Nav Stuff " + menuItem.getItemId());
        switch (menuItem.getItemId())
        {
            case R.id.nav_sensor:
                getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container, new SensorFragment(), "SenFrag").addToBackStack(null).commit();
                break;
            case R.id.nav_device:
                getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container, new DeviceFragment(), "DevFrag").addToBackStack(null).commit();
                break;
            case R.id.nav_rule:
                getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container, new RuleFragment(), "RulFrag").addToBackStack(null).commit();
                break;
            case R.id.nav_bluetooth:
                getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container, new BluetoothFragment(), "BTFrag").addToBackStack(null).commit();
                break;
        }
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    /**
     * This method requests bluetooth access from the user. If the bluetooth functionality is turned off, requests for it to be turned on.
     * Then, attempts to connect to bluetooth
     */
    public void requestBluetooth() {
        if (!bluetoothAdapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
        }
        connectBluetooth();
    }
    /**
     * A list of paired devices is requested and used to populate the listView with the values.
     * */
    public void connectBluetooth() {
        pairedDevices = bluetoothAdapter.getBondedDevices();
        // First check if there are any already paired devices
        if (pairedDevices.size() > 0) {
            // There are paired devices. Get the name and address of each paired device.
            for (BluetoothDevice device : pairedDevices) {
                deviceNames.add(device.getName());
                macAddresses.add(device.getAddress());

                listOfDevices.put(device.getName(), device.getAddress());
            }
        } else {
            Toast.makeText(getApplicationContext(), "No Paired Bluetooth Devices Found.", Toast.LENGTH_LONG).show();
        }
        populateListView();
    }

    /**
     * Populates the list view with the devices names of bluetooth devices.
     * The array adapter is created and the update function on the bluetooth fragment is called
     **/
    public void populateListView() {
        //lstView = (ListView) findViewById(R.id.lstDevices);
        arrayAdapter = new ArrayAdapter<String>(this, R.layout.devices_view, R.id.txtName, deviceNames);

        arrayAdapter.notifyDataSetChanged();

        btfm = (BluetoothFragment) fm.findFragmentByTag("BTFrag");

        Log.d("aaaa", "populate");
        if(btfm != null) {
            btfm.updateList();
            Log.d("aaaa", "Update sent");
        }
        Log.d("aaaa", "fm = " + fm.getFragments());
        //btfm.lstView.setAdapter(arrayAdapter);
    }
    /**
     * Populates the list view in the rule fragment with the formatted rules
     * The adapter is formed and the update function is called in the rule fragment
     **/
    public void populateRuleView(){

        ruleAdaptor = new ArrayAdapter<String>(this, R.layout.devices_view, R.id.txtName, formattedRules);
        ruleAdaptor.notifyDataSetChanged();

        rlfm = (RuleFragment) fm.findFragmentByTag("RulFrag");
        Log.d("aaaa", "Populate!");
        if(rlfm != null){
            rlfm.updatelist();
            Log.d("aaaa", "update sent");
        }
    }
    /**
     * Populates the list view in the sensor fragment with the formatted sensor list
     * The adapter is formed and the update function is called in the sensor fragment
     **/
    public void populateSensorView(){

        sensorAdaptor = new ArrayAdapter<String>(this, R.layout.devices_view, R.id.txtName, sensorList);
        sensorAdaptor.notifyDataSetChanged();

        snfm = (SensorFragment) fm.findFragmentByTag("SenFrag");
        Log.d("aaaa", "Populate!");
        if(snfm != null){
            snfm.updatelist();
            Log.d("aaaa", "update sent");
        }
    }
    /**
     * Populates the list view in the Device fragment with the formatted objects list
     * The adapter is formed and the update function is called in the Device fragment
     **/
    public void populateObjView(){

        ObjAdaptor = new ArrayAdapter<String>(this, R.layout.devices_view, R.id.txtName, formattedObjs);
        ObjAdaptor.notifyDataSetChanged();

        dvfm = (DeviceFragment) fm.findFragmentByTag("DevFrag");
        Log.d("aaaa", "Populate!");
        if(dvfm != null){
            dvfm.updatelist();
            Log.d("aaaa", "update sent");
        }
    }

    /**
     * The Bluetooth list view is emptied and repopulated with default paired devices.
     * Used to ensure that new connections replace old invalid ones and prevent the list view from becoming over crowded
     * */
    private void clearBTList(){
        listOfDevices.clear();              //clear the existing lists
        pairedDevices = null;
        deviceNames.clear();
        macAddresses.clear();
        pairedDevices = bluetoothAdapter.getBondedDevices();
        // Then check if there are any already paired devices and add them to the List
        if (pairedDevices.size() > 0) {
            // There are paired devices. Get the name and address of each paired device.
            for (BluetoothDevice device : pairedDevices) {
                deviceNames.add(device.getName());
                macAddresses.add(device.getAddress());

                listOfDevices.put(device.getName(), device.getAddress());

            }
        }
    }
    /**
     * This method handles button clicks
     * @param v The current view
     */
    public void onClickButton(View v) {
        byte[] send;
        switch (v.getId()) {
            case R.id.btnScan:
                if (bluetoothAdapter.isDiscovering()) {
                    bluetoothAdapter.cancelDiscovery();
                }
                clearBTList();
                bluetoothAdapter.startDiscovery();
                Toast.makeText(getApplicationContext(), "Scanning for bluetooth devices", Toast.LENGTH_LONG).show();

                btfm = (BluetoothFragment) fm.findFragmentByTag("BTFrag");
                Log.d("aaaa", "aa: " + btfm);
                break;

            case R.id.NewRule:
                getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container, new AddRuleFragment(), "AddRule").addToBackStack(null).commit();
                break;

            default:
                throw new RuntimeException("Unknown button ID");

        }

    }
    /**
     * Helper function to assign Onclick events to the correct fragment.
     * Calls the onclick on the Add Rule Fragment to assigned buttons
     * @param v The current view
     **/
    public void onClickAddRuleFragOp(View v){
        AddRuleFragment ad = (AddRuleFragment) fm.findFragmentByTag("AddRule");
        ad.onClickOp(v);
    }
    /**
     * Helper function to assign Onclick events to the correct fragment.
     * Calls the onclick on the Rule Fragment to assigned buttons
     * @param v The current view
     **/
    public void onClickRuleFragOP(View v){
        RuleFragment rf = (RuleFragment) fm.findFragmentByTag("RulFrag");
        rf.onClickOp(v);
    }
    /**
     * Helper function to assign Onclick events to the correct fragment.
     * Calls the onclick on the Sensor Fragment to assigned buttons
     * @param v The current view
     **/
    public void onClickSenFragOP(View v){
        SensorFragment sf = (SensorFragment) fm.findFragmentByTag("SenFrag");
        sf.onClickOp(v);
    }
    /**
     * Helper function to assign Onclick events to the correct fragment.
     * Calls the onclick on the Device Fragment to assigned buttons
     * @param v The current view
     **/
    public void onClickObjFragOP(View v){
        DeviceFragment df = (DeviceFragment) fm.findFragmentByTag("DevFrag");
        df.onClickOp(v);
    }

    /**
     * Used to check user input to bluetooth request.
     * If request is denied, the request is made again until the user accepts it
     * @param data Data returned by the callback
     * @param requestCode The request code that has resulted in the callback
     * @param resultCode The result of that request
     **/
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        // Check is bluetooth request was granted
        if (requestCode == REQUEST_ENABLE_BT) {
            // If unsuccessful, repeat request until successful
            if (resultCode == RESULT_CANCELED) {
                AlertDialog alertDialog = new AlertDialog.Builder(MainActivity.this).create();
                alertDialog.setTitle("Error");
                alertDialog.setMessage("Bluetooth required for this app to work");
                alertDialog.setButton(AlertDialog.BUTTON_NEUTRAL, "OK",
                        new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int which) {
                                dialog.dismiss();
                                requestBluetooth();
                            }
                        });
                alertDialog.show();
            }
        }
    }

    // Create a BroadcastReceiver for ACTION_FOUND.
    private final BroadcastReceiver receiver = new BroadcastReceiver() {
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();

            if (BluetoothDevice.ACTION_FOUND.equals(action)) {
                // Discovery has found a device. Get the BluetoothDevice
                // object and its info from the Intent.

                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                if (device.getName() != null) {
                    deviceNames.add(device.getName());
                    macAddresses.add(device.getAddress());

                    listOfDevices.put(device.getName(), device.getAddress());

                    //Toast.makeText(getApplicationContext(), "Found: " + device.getName(), Toast.LENGTH_LONG).show();
                }

                //btfm.populateListView(deviceNames);
                populateListView();

                //Log.d("BT Discovery", deviceNames + " " + macAddresses);
            } else if (BluetoothAdapter.ACTION_DISCOVERY_FINISHED.equals(action)) {
                //Toast.makeText(getApplicationContext(), "Finished scan, no devices found", Toast.LENGTH_LONG).show();
            }
        }
    };

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unregisterReceiver(receiver);
    }

    @Override
    public void onResume() {
        super.onResume();
    }

    /**
     * Sets the color of the status bar to show the current state of the Bluetooth connection
     **/
    public void setStatusBar()
    {
        switch(BTservice.getState()){
            case BTService.STATE_NONE:
                findViewById(R.id.txtBTStatus).setBackgroundColor(Color.BLACK);
                break;
            case BTService.STATE_LISTEN:
                findViewById(R.id.txtBTStatus).setBackgroundColor(Color.RED);
                break;
            case BTService.STATE_CONNECTING:
                findViewById(R.id.txtBTStatus).setBackgroundColor(Color.YELLOW);
                break;
            case BTService.STATE_CONNECTED:
                findViewById(R.id.txtBTStatus).setBackgroundColor(Color.GREEN);
                break;

        }
    }

    /**
     * Handler responsible for communication between the BTService and the main activity.
     * keeps track of what the Service is receiving and returning to the Activity to respond appropriately.
     * Incoming data is sent off to be processed and state changes to the connection is also handled.
     **/
    private final Handler mHandler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            switch (msg.what) {
                case MESSAGE_WRITE:

                    break;
                case MESSAGE_READ:
                    //TextView outBox = findViewById(R.id.Received);
                    //outBox.setText(msg.getData().getString(INCOMING_DATA));
                    inStringBuff.append(msg.getData().getString(INCOMING_DATA));

                    Log.d("aaaa", "Data = " + msg.getData().getString(INCOMING_DATA));
                    Log.d("aaaa","InStream = " + inStringBuff.toString());

                    processInput(inStringBuff.toString());

                    inStringBuff.setLength(0);
                    break;
                case MESSAGE_DEVICE_NAME:

                    mConnectedDeviceName = msg.getData().getString(DEVICE_NAME);
                    Toast.makeText(getApplicationContext(), "Connected to " + mConnectedDeviceName, Toast.LENGTH_SHORT).show();

                    break;
                case MESSAGE_TOAST:

                    break;
                case MESSAGE_STATE_CHANGE:
                    if(fragState == fragmentState.BLUETOOTH) {
                        switch (msg.arg1) {
                            case BTService.STATE_NONE:
                                findViewById(R.id.txtBTStatus).setBackgroundColor(Color.BLACK);
                                Log.d("Status", "BT None");
                                break;
                            case BTService.STATE_LISTEN:
                                findViewById(R.id.txtBTStatus).setBackgroundColor(Color.RED);
                                Log.d("Status", "BT listening");
                                req = 0;
                                break;
                            case BTService.STATE_CONNECTING:
                                findViewById(R.id.txtBTStatus).setBackgroundColor(Color.YELLOW);
                                Log.d("Status", "BT Connecting");
                                break;
                            case BTService.STATE_CONNECTED:
                                findViewById(R.id.txtBTStatus).setBackgroundColor(Color.BLUE);
                                req = 1;
                                requestAll(req);
                                Log.d("Status", "BT Connected");
                                break;
                            default:
                                Log.d("Status", "Error, no status recognised");
                                break;
                        }
                    }
                    break;
            }
        }
    };

    /**
     * Default request once the connection is made for the first time to a server.
     * @param i The request code. Iterates through the different requests based on its value
     **/
    public void requestAll(int i) {
        if (i == 1) {
            byte[] send = "R:AR".getBytes();
            BTservice.write(send);
        }else if(i == 2){
            byte[] send = "R:AS".getBytes();
            BTservice.write(send);
        }else if(i == 3){
            byte[] send = "R:AD".getBytes();
            BTservice.write(send);
        }else if(i == 4){
            byte[] send = "R:AG".getBytes();
            BTservice.write(send);
        }else{
            req = 0;
            findViewById(R.id.txtBTStatus).setBackgroundColor(Color.GREEN);
        }
    }

    /**
     * Helper function used by the fragments to inform the main activity about which fragment is currently on top and in view.
     * @param frag The state to be set*/
    public void setfragmentstate(fragmentState frag){
        fragState = frag;
    }

    /**
     * Function used to create a list of rules from incoming data, formatting it into something user readable.
     * Cuts the incoming string into substrings containing the rule and id.
     * That substring is then further split into ID-Rule pairs.
     * Those Strings are then further processed to extract the raw rules and id values which are added to the hashmap.
     * The rules are passed along to ConvertRules() and WriteUserRule() to get a user readable version of it.
     *
     * @param inString The incoming string to be processed into valid rules
     **/
    private void processRules(String inString){
        String str = inString;
        ruleList.clear();
        ruleIDList.clear();
        listOfRules.clear();
        formattedRules.clear();
        if(!inString.equals("[Empty List]")) {

            Matcher m = Pattern.compile("ID:(.*?)]").matcher(str);
            while (m.find()) {
                //Log.d("aaaa", "match: " + m.group());

                String[] pairs = m.group().split("Rule: ");
                //Log.d("aaaa", Arrays.toString(pairs));

                String id = pairs[0].substring(4);
                String dev = pairs[1].split(":")[3];
                String state = pairs[1].split(":")[4];
                String rule = pairs[1].substring(1, pairs[1].length() - 1);
                String formatRule = rule.substring(0, rule.indexOf(dev)) + rule.substring(rule.indexOf(dev) + dev.length() + 1 + state.length() + 1);
                //Log.d("aaaa","ID: " + id +"Dev: " + dev +" rule: " + rule);
                //Log.d("aaaa","fR = " + formatRule);
                String format = convertRules(formatRule);
                format = writeUserRule(id, dev, state, format);

                //Log.d("aaaa", "converted: " + format);
                ruleIDList.add(id);
                ruleList.add(rule);
                formattedRules.add(format);

                listOfRules.put(id, rule);
            }
        }
        else{
            String id = "0", rule = "NO RULES SET", format = "ID: Nan } No rules set, Create one!";
            ruleIDList.add(id);
            ruleList.add(rule);
            formattedRules.add(format);

            listOfRules.put(id, rule);
        }
    }
    /**
     * The raw rules are converted into a more gramatically correct form. The raw string is processed slightly to make using a regex easier first.
     * Then, strings that fit the pattern is found, splitting it into two comparison values and the operator and a connector is there are multiple subrules.
     * The individual components of the rules are then stitched back together in the correct form and appended onto the return string.
     *
     * @param str The rule to be converted into a proper form
     * @return  The processed rule, in a grammatically correct order.
     **/
    private String convertRules(String str){
        String ret = "";
        ArrayList<String> array = new ArrayList<>();

        String s,d,op, cn, tmp;
        str = str.replace("C:R:C:", ":");

        str = str.replace(":AND", ":AND]");
        str = str.replace(":OR", ":OR]");
        str = str.replace(":NOT", ":NOT]");

        //str = str.replace("", ")");
        //String sub = str.substring(0, str.indexOf(":AND"));
        Matcher m = Pattern.compile("(\\[|OR:|AND:|NOT:|:)(.*?)(:GE|:LE|:EQ|:AND|:OR|:NOT|])").matcher(str);
        while(m.find()){
            array.add(m.group());
        }
        if(array != null)
        {
            tmp = array.get(0).substring(1);
            s = tmp.split(":")[0];
            d = tmp.split(":")[1];
            op = tmp.split(":")[2];
            ret = s + ":" + op + ":" + d;
            //Log.d("aaaa","split: " + Arrays.toString(tmp.split(":")));
            //Log.d("aaaa","ret: " + ret);
            if(array.size() > 2) {
                for (int i = 1; i <= array.size() - 1; i += 2) {
                    //Log.d("aaaa", "ar= " + array.get(i));
                    tmp = array.get(i).substring(1);
                    s = tmp.split(":")[0];
                    d = tmp.split(":")[1];
                    op = tmp.split(":")[2];

                    tmp = array.get(i + 1);
                    cn = tmp.substring(0, tmp.length() - 1);
                    ret += cn + ":" + s + ":" + op + ":" + d;
                    //Log.d("aaaa","split: " + Arrays.toString(tmp.split(":")));
                    //Log.d("aaaa", "ret: " + ret);
                }
            }
        }

        return ret;
    }
    /**
     * Writes a rule using the parameters passed in, into more user-friendly language.
     * It converts the internal language and symbols used by the system into english. Requires the str passed in has already been converted into a grammatically correct state.
     *
     * @param dev The name of the device the rule is applied to.
     * @param id The id of the rule
     * @param state The state the device should be switched to if the rule is true
     * @param str The string representing the rule.
     * @return The Formatted string, ready to be added to the arraylist and displayed to the user
     **/
    private String writeUserRule(String id, String dev, String state, String str){
        String ret;

        if(str != null) {
            //Log.d("aaaa", "userstr : " + str);
            str = str.replace("GE", "Greater Than");
            str = str.replace(":", " ");
            str = str.replace("LE", "Less Than");
            str = str.replace("EQ", "Equals");

        }
        else{
            str = "Null String";
        }

        ret = "ID: " + id + "Device: " + dev + "State: "+ state +" {" + str + "}";

        return ret;
    }

    /**
     * Function responsible for handling the data recieved from the sever in response to a request for sensor data
     * Similar to ProcessRules(), converts the incoming data packet into a user readable format.
     * Matches the instring to a regex to create individual sensor information strings which are then further processed
     * to extract useful data.
     * The data is then formatted into a string which is then added to the corresponding arraylists
     * @param inString The incoming data to be processed
     **/
    private void processSensors(String inString){
        //{Name: Time ID: 0 Time: 0} {Name: emonth6 ID: 1 Temp: 19.9 Time: 1587916150} {Name: emonth8 ID: 2 Temp: 19.8 Time: 1587916148} {Name: emonth7 ID: 3 Temp: 19.8 Time: 1587916161}
        String str = inString;
        //sensorAdaptor = null;
        //sensorAdaptor.notifyDataSetChanged();
        sensorList.clear();
        sensorIDList.clear();
        listOfSensors.clear();

        if(!inString.equals("[Empty String]")) {
            Matcher m = Pattern.compile("\\((.*?)\\)").matcher(str);
            while (m.find()) {
                String id = "";
                String name = "";
                String val = "";
                String time = "";
                String[] elements;

                elements = m.group().split("\\s+");
                //Log.d("aaaa", "ele = " + Arrays.toString(elements));
                id = elements[3];
                //Log.d("aaaa","id:" + id);
                Calendar c = Calendar.getInstance();
                if (id.equals("0")) {
                    name = "Time sensor";
                    time = c.get(Calendar.HOUR_OF_DAY) + ":" + c.get(Calendar.MINUTE);
                } else {
                    name = elements[1];
                    id = elements[3];
                    val = elements[5];
                    time = elements[7].substring(0, elements[7].length() - 1);
                    c.setTimeInMillis(Long.valueOf(time) * 1000);
                    time = c.get(Calendar.HOUR_OF_DAY) + ":" + c.get(Calendar.MINUTE);
                }
                String sensor;
                if(id.equals("0"))
                     sensor = "Sensor " + id + "} " + name + ": " + time;
                else
                    sensor = "Sensor " + id + "} " + name + " Temp: " + val + " at: " + time;

                Log.d("aaaa", "Sen = " + name + " id: " + id + " val: " + val + " Time: " + time);

                sensorList.add(sensor);
                sensorIDList.add(id);
                listOfSensors.put(id, sensor);
            }
        }else{
            String sensor = "Sensors in list", id = "No ";
            sensorList.add(sensor);
            sensorIDList.add(id);
            listOfSensors.put(id, sensor);
        }
    }

    /**
     * Handles the data coming in response to a request for controllable objects.
     * The instring is matched to a regex and the substrings are processed to extract data for individual devices.
     * The extracted data is formatted into a string which is then added to the proper arraylists, ready to populate the object lists
     *
     * @param inString Incoming data string from the server
     **/
    private void processObjects(String inString){
        //ObjAdaptor = null;
        //ObjAdaptor.notifyDataSetChanged();
        ObjList.clear();
        ObjIDList.clear();
        formattedObjs.clear();
        listOfObjs.clear();

        String str = inString;
        if(!inString.equals("[Empty List]")){
            Matcher m = Pattern.compile("\\((.*?)\\)").matcher(str);
            while(m.find()){
                String[] elements;
                String name;
                String id;
                String state;
                elements = m.group().split("\\s+");
                Log.d("aaaa", "ele: " + Arrays.toString(elements));

                name = elements[1];
                id = elements[3];
                state = elements[5];

                String obj = "ID:" + id + " Name: " + name + " State: " + state;

                ObjList.add(name);
                ObjIDList.add(id);
                formattedObjs.add(obj);
                listOfObjs.put(id,name);

            }
        }else{
            Log.d("aaaa","Fuck off ya dumb cow");

        }
    }

    /**
     * This method decides what to do when data is received from the server based upon the current fragState.
     * The correct data processing method is called to format the data properly.
     * If the the current fragment is the Bluetooth Fragment, all data is requested sequentially to populating the arraylists on startup.
     **/
    private void processInput(String inString){
        switch(fragState){
            case RULE:
                processRules(inString);
                populateRuleView();

                break;
            case BLUETOOTH:
                if(req == 1){
                    processRules(inString);
                    Log.d("aaaa","req = " + req + " : " + inString);
                }else if(req == 2){
                    processSensors(inString);
                    Log.d("aaaa", "req = " + req + " : " + inString);
                }else if(req == 3){
                    processObjects(inString);
                    Log.d("aaaa", "req = " + req + " : " + inString);
                }else if(req == 4){
                    Log.d("aaaa", "req = " + req + " : " + inString);
                }

                req ++;
                requestAll(req);

                break;
            case SENSOR:
                processSensors(inString);
                populateSensorView();
                break;
            case DEVICE:
                processObjects(inString);
                populateObjView();
                break;
        }
    }

    @Override
    public void onSaveInstanceState(Bundle savedInstance) {
        super.onSaveInstanceState(savedInstance);
    }

    @Override
    public void onRestoreInstanceState(Bundle savedInstance) {
        super.onRestoreInstanceState(savedInstance);
    }

    @Override
    public void onBackPressed()
    {
        if(drawer.isDrawerOpen(GravityCompat.START))
        {
            drawer.closeDrawer(GravityCompat.START);
        }
        else
        {
            super.onBackPressed();
        }
    }

}

