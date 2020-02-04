package com.example.mohamed.arduinoprototype;

import androidx.appcompat.app.AppCompatActivity;
import android.app.AlertDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Set;

public class MainActivity extends AppCompatActivity {


    public static final int MESSAGE_STATE_CHANGE = 1;
    public static final int MESSAGE_READ = 2;
    public static final int MESSAGE_WRITE = 3;
    public static final int MESSAGE_DEVICE_NAME = 4;
    public static final int MESSAGE_TOAST = 5;

    public static final String DEVICE_NAME = "device_name";
    public static final String TOAST = "toast";

    private String mConnectedDeviceName = null;


    public StringBuffer outStringBuff = new StringBuffer("");

    private BTService BTservice;

    // Bluetooth adaptor to use
    BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    // List of previously paired devices, pairing is required before connecting
    Set<BluetoothDevice> pairedDevices;
    // Bluetooth request code
    int REQUEST_ENABLE_BT = 1;

    // The list view of bluetooth devices
    ListView lstView;
    ArrayAdapter<String> arrayAdapter;
    ArrayList<String> deviceNames = new ArrayList<>();
    ArrayList<String> macAddresses = new ArrayList<>();

    HashMap<String, String> listOfDevices = new HashMap<String, String>();



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);



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
        setUpListner();

        BTservice = new BTService(this, mHandler);
        BTservice.start();
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

        populateListView();
    }

    public void populateListView() {
        lstView = (ListView) findViewById(R.id.lstDevices);
        arrayAdapter = new ArrayAdapter<String>(this, R.layout.devices_view, R.id.txtName, deviceNames);
        lstView.setAdapter(arrayAdapter);
    }

    /**
     * This method sets up a listener on the list view
     */
    public void setUpListner() {

        lstView = (ListView) findViewById(R.id.lstDevices);
        lstView.setClickable(true);
        lstView.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> arg0, View view, int position, long arg3) {
                TextView deviceName = (TextView) view.findViewById(R.id.txtName);
                String deviceNameString = deviceName.getText().toString();
                String deviceAddressString = listOfDevices.get(deviceNameString);
                Toast.makeText(getApplicationContext(), "" + deviceNameString + " : " + deviceAddressString , Toast.LENGTH_LONG).show();


                String MAC_ADDR = deviceAddressString;
                BluetoothDevice device = bluetoothAdapter.getRemoteDevice(MAC_ADDR);
                BTservice.connect(device);
            }
        });
    }

    /**
     * This method handles button clicks
     * @param v
     */
    public void onClickButton(View v) {
        byte[] send;
        switch (v.getId()) {
            case R.id.btnScan:
                if (bluetoothAdapter.isDiscovering()) {
                    bluetoothAdapter.cancelDiscovery();
                }
                bluetoothAdapter.startDiscovery();
                Toast.makeText(getApplicationContext(), "Scanning for bluetooth devices", Toast.LENGTH_LONG).show();
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
                if(device.getName() != null) {
                    deviceNames.add(device.getName());
                    macAddresses.add(device.getAddress());

                    listOfDevices.put(device.getName(), device.getAddress());

                    //Toast.makeText(getApplicationContext(), "Found: " + device.getName(), Toast.LENGTH_LONG).show();
                }

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


    public void onResume(){
        super.onResume();
    }

    private final Handler mHandler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            switch (msg.what) {
                case MESSAGE_WRITE:

                    break;
                case MESSAGE_READ:

                    break;
                case MESSAGE_DEVICE_NAME:

                    mConnectedDeviceName = msg.getData().getString(DEVICE_NAME);
                    Toast.makeText(getApplicationContext(), "Connected to " + mConnectedDeviceName, Toast.LENGTH_SHORT).show();

                    break;
                case MESSAGE_TOAST:

                    break;
            }
        }
    };

}

