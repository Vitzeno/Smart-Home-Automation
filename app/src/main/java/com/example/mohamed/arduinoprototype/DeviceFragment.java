package com.example.mohamed.arduinoprototype;

import android.bluetooth.BluetoothDevice;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.HashMap;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

public class DeviceFragment extends Fragment
{
    public ListView lstObj;
    private ArrayAdapter<String> objAdapter;
    private ArrayList<String> objs;
    private HashMap<String, String> listOfObjs;
    private Button getObj, switchObj;
    private String[] requests = {"R:AD"};

    private Boolean state = false;
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_device, container, false);

        ((MainActivity)getActivity()).setfragmentstate(MainActivity.fragmentState.DEVICE);

        return v;
    }
    /**
     * Called once the view is created to assign all the objects on the view.
     * Listeners are set up for the items in the list and variables are initialised
     * */
    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        lstObj = (ListView) getView().findViewById(R.id.lstObjs);
        objs = ((MainActivity)getActivity()).ObjList;
        listOfObjs = ((MainActivity)getActivity()).listOfObjs;
        objAdapter = ((MainActivity)getActivity()).ObjAdaptor;

        switchObj = getView().findViewById(R.id.SwitchDev);
        state = true;
        switchObj.setBackgroundColor(Color.GREEN);
        populateListView();
        setupListener();
        //((MainActivity)getActivity()).setStatusBar();
    }

    @Override
    public void onResume(){
        super.onResume();
        ((MainActivity)getActivity()).navView.setCheckedItem(R.id.nav_device);
    }

    /**
     * Populates the Listview with data from the adapter in main activity.
     * */
    private void populateListView() {
        objAdapter = null;
        objAdapter = ((MainActivity)getActivity()).ObjAdaptor;

        lstObj.setAdapter(objAdapter);

        if(objAdapter != null)
        {
            Log.d("aaaa", "objAdaptor != null");
            objAdapter.notifyDataSetChanged();
        }
    }
    /**
     * Called from main activity when the data in the adapter has changed.
     * Local lists are updated with the new data and the list is populated with the adapter data.
     * */
    public void updatelist() {
        Log.d("aaaa", "updating");
        objs = ((MainActivity) getActivity()).formattedObjs;
        listOfObjs = ((MainActivity) getActivity()).listOfObjs;

        populateListView();
    }
    /**
     * Handles the onClick events for this fragment.
     * Allows for two buttons, one to fetch data about devices from the server
     * and the other determines which state a device should be switched to
     * */
    public void onClickOp(View v){
        switch(v.getId()){
            case R.id.GetDev:
                if (((MainActivity) getActivity()).BTservice.getState() == BTService.STATE_CONNECTED) {
                    byte[] send;
                    send = requests[0].getBytes();
                    Log.d("aaaa", "send request: " + requests[0]);
                    ((MainActivity) getActivity()).BTservice.write(send);

                    break;
                }
                else
                {
                    Log.d("aaaa","Cant request. check connection");
                }
                break;
            case R.id.SwitchDev:
                state = !state;
                int color = (state) ? Color.GREEN: Color.RED;
                String op = (state) ? "On" : "Off";
                switchObj.setBackgroundColor(color);
                switchObj.setText(op);

                break;
        }

    }
    /**
     * Responsible for setting up the listener on the list items.
     * Depending on the state of the switch button, will either send an 'OFF' or 'ON' signal to the selected device
     * */
    private void setupListener(){
        lstObj.setClickable(true);
        lstObj.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> arg0, View view, int position, long arg3) {

                TextView rule = (TextView) view.findViewById(R.id.txtName);
                String tmp = rule.getText().toString();
                String id = tmp.substring(tmp.indexOf("ID: ") +4, tmp.indexOf(" Name"));
                Log.d("aaaa","Pressed!" + id);

                if(state) {
                    try {
                        Log.d("aaaa", "Switching...");
                        byte[] send;
                        StringBuffer outStringBuff = new StringBuffer("");
                        outStringBuff.setLength(0);
                        outStringBuff.append("C:D:S:");
                        outStringBuff.append(id);
                        outStringBuff.append(":1");
                        send = outStringBuff.toString().getBytes();
                        ((MainActivity) getActivity()).BTservice.write(send);
                    } catch (Exception e) {
                        Log.d("aaaa", "Couldn't send command.");
                        e.printStackTrace();
                    }
                }else{
                    try {
                        Log.d("aaaa", "Switching...");
                        byte[] send;
                        StringBuffer outStringBuff = new StringBuffer("");
                        outStringBuff.setLength(0);
                        outStringBuff.append("C:D:S:");
                        outStringBuff.append(id);
                        outStringBuff.append(":0");
                        send = outStringBuff.toString().getBytes();
                        ((MainActivity) getActivity()).BTservice.write(send);
                    } catch (Exception e) {
                        Log.d("aaaa", "Couldn't send command.");
                        e.printStackTrace();
                    }
                }
            }
        });
    }
}
