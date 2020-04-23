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

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Set;

public class MainActivity extends AppCompatActivity implements NavigationView.OnNavigationItemSelectedListener {


    public static final int MESSAGE_STATE_CHANGE = 1;
    public static final int MESSAGE_READ = 2;
    public static final int MESSAGE_WRITE = 3;
    public static final int MESSAGE_DEVICE_NAME = 4;
    public static final int MESSAGE_TOAST = 5;

    public static final String DEVICE_NAME = "device_name";
    public static final String INCOMING_DATA = "incoming_data";
    public static final String TOAST = "toast";

    private String mConnectedDeviceName = null;
    private DrawerLayout drawer;
    public NavigationView navView;

    public StringBuffer outStringBuff = new StringBuffer("");

    public BTService BTservice;

    // Bluetooth adaptor to use
    public BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    // List of previously paired devices, pairing is required before connecting
    public Set<BluetoothDevice> pairedDevices;
    // Bluetooth request code
    int REQUEST_ENABLE_BT = 1;

    // The list view of bluetooth devices
    public ListView lstView;
    public ArrayAdapter<String> arrayAdapter;
    public ArrayList<String> deviceNames = new ArrayList<>();
    public ArrayList<String> macAddresses = new ArrayList<>();

    public HashMap<String, String> listOfDevices = new HashMap<String, String>();

    public FragmentManager fm = getSupportFragmentManager();
    public BluetoothFragment btfm;

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
            Log.d("aaaa", "FUCK");

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

        //btfm.populateListView(deviceNames);
        populateListView();
        //setUpListner();

        BTservice = new BTService(this, mHandler);
        BTservice.start();

        if(savedInstanceState == null)
        {
            getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container, new BluetoothFragment(), "BTFrag").addToBackStack(null).commit();
            navView.setCheckedItem(R.id.nav_bluetooth);
        }
    }

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
     * This method requests bluetooth access from the user
     */
    public void requestBluetooth() {
        if (!bluetoothAdapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
        }
        connectBluetooth();
    }

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

        //btfm.populateListView(deviceNames);
        populateListView();
    }

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
     *
     * @param v
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
            case R.id.btnOn:
                outStringBuff.setLength(0);
                outStringBuff.append('H');
                send = outStringBuff.toString().getBytes();
                BTservice.write(send);

                break;

            case R.id.btnOff:
                outStringBuff.setLength(0);
                outStringBuff.append('L');
                send = outStringBuff.toString().getBytes();
                BTservice.write(send);
                break;

            case R.id.NewRule:
                getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container, new AddRuleFragment(), "AddRule").addToBackStack(null).commit();
                break;

            /*case R.id.btnSOS:
                outStringBuff.setLength(0);
                outStringBuff.append('S');
                send = outStringBuff.toString().getBytes();
                BTservice.write(send);
                break;*/
            default:
                throw new RuntimeException("Unknown button ID");

        }

    }

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


    public void onResume() {
        super.onResume();
    }

    private final Handler mHandler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            switch (msg.what) {
                case MESSAGE_WRITE:

                    break;
                case MESSAGE_READ:
                    TextView outBox = findViewById(R.id.Received);
                    outBox.setText(msg.getData().getString(INCOMING_DATA));
                    Log.d("d", msg.getData().getString(INCOMING_DATA));
                    break;
                case MESSAGE_DEVICE_NAME:

                    mConnectedDeviceName = msg.getData().getString(DEVICE_NAME);
                    Toast.makeText(getApplicationContext(), "Connected to " + mConnectedDeviceName, Toast.LENGTH_SHORT).show();

                    break;
                case MESSAGE_TOAST:

                    break;
                case MESSAGE_STATE_CHANGE:
                    switch (msg.arg1) {
                        case BTService.STATE_NONE:
                            findViewById(R.id.txtBTStatus).setBackgroundColor(Color.BLACK);
                            Log.d("Status", "BT None");
                            break;
                        case BTService.STATE_LISTEN:
                            findViewById(R.id.txtBTStatus).setBackgroundColor(Color.RED);
                            Log.d("Status", "BT listening");
                            break;
                        case BTService.STATE_CONNECTING:
                            findViewById(R.id.txtBTStatus).setBackgroundColor(Color.YELLOW);
                            Log.d("Status", "BT Connecting");
                            break;
                        case BTService.STATE_CONNECTED:
                            findViewById(R.id.txtBTStatus).setBackgroundColor(Color.GREEN);
                            Log.d("Status", "BT Connected");
                            break;
                        default:
                            Log.d("Status", "Error, no status recognised");
                            break;
                    }
            }
        }
    };

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

