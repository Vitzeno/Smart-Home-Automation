package com.example.mohamed.arduinoprototype;

import android.app.Activity;
import android.bluetooth.BluetoothDevice;
import android.content.Context;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.mohamed.arduinoprototype.R;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

public class BluetoothFragment extends Fragment
{

    public ListView lstView;
    public ArrayAdapter<String> arrayAdapter;
    public ArrayList<String> devices;
    public ArrayList<String> macAddresses = new ArrayList<>();
    public HashMap<String, String> listOfDevices = new HashMap<String, String>();

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_bluetooth, container, false);

        ((MainActivity)getActivity()).setfragmentstate(MainActivity.fragmentState.BLUETOOTH);

        return v;
    }

    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        lstView = (ListView) getView().findViewById(R.id.lstDevices);
        devices = ((MainActivity)getActivity()).deviceNames;
        listOfDevices = ((MainActivity)getActivity()).listOfDevices;
        arrayAdapter = ((MainActivity)getActivity()).arrayAdapter;

        populateListView();
        setUpListner();
    }
    @Override
    public void onResume(){
        super.onResume();
        ((MainActivity)getActivity()).navView.setCheckedItem(R.id.nav_bluetooth);
    }
    private void populateListView() {
        arrayAdapter = ((MainActivity)getActivity()).arrayAdapter;
        lstView.setAdapter(arrayAdapter);
    }

    public void updateList()
    {
        Log.d("aaaa", "updating");
        devices = ((MainActivity)getActivity()).deviceNames;
        listOfDevices = ((MainActivity)getActivity()).listOfDevices;
        arrayAdapter.notifyDataSetChanged();
        populateListView();
    }

    /**
     * This method sets up a listener on the list view
     */
    public void setUpListner() {

        //lstView = (ListView) findViewById(R.id.lstDevices);
        lstView.setClickable(true);
        lstView.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> arg0, View view, int position, long arg3) {
                TextView deviceName = (TextView) view.findViewById(R.id.txtName);
                String deviceNameString = deviceName.getText().toString();
                String deviceAddressString = listOfDevices.get(deviceNameString);
                Toast.makeText(getView().getContext(), "" + deviceNameString + " : " + deviceAddressString, Toast.LENGTH_LONG).show();


                String MAC_ADDR = deviceAddressString;
                BluetoothDevice device = ((MainActivity)getActivity()).bluetoothAdapter.getRemoteDevice(MAC_ADDR);
                ((MainActivity)getActivity()).BTservice.connect(device);
            }
        });
    }
}
