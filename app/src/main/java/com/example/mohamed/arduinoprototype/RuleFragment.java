package com.example.mohamed.arduinoprototype;

import android.bluetooth.BluetoothDevice;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

public class RuleFragment extends Fragment
{
    public ListView lstRule;


    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_rule, container, false);
    }

    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        lstRule = (ListView) getView().findViewById(R.id.lstRule);

        //setUpListner();
    }
    @Override
    public void onResume(){
        super.onResume();
        ((MainActivity)getActivity()).navView.setCheckedItem(R.id.nav_rule);
    }
    public void setUpListner() {

        //lstView = (ListView) findViewById(R.id.lstDevices);
        lstRule.setClickable(true);
        lstRule.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> arg0, View view, int position, long arg3) {
                /*
                TextView deviceName = (TextView) view.findViewById(R.id.txtName);
                String deviceNameString = deviceName.getText().toString();
                String deviceAddressString = listOfDevices.get(deviceNameString);
                Toast.makeText(getView().getContext(), "" + deviceNameString + " : " + deviceAddressString, Toast.LENGTH_LONG).show();


                String MAC_ADDR = deviceAddressString;
                BluetoothDevice device = ((MainActivity)getActivity()).bluetoothAdapter.getRemoteDevice(MAC_ADDR);
                ((MainActivity)getActivity()).BTservice.connect(device);
                */
            }
        });
    }
}
