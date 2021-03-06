package com.example.mohamed.arduinoprototype;

import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import java.util.ArrayList;
import java.util.HashMap;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

public class SensorFragment extends Fragment
{
    public ListView lstSen;
    private ArrayAdapter<String> sensorAdaptor;
    private ArrayList<String> sensors;
    private HashMap<String, String> ListOfSensors;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_sensor, container, false);

        ((MainActivity)getActivity()).setfragmentstate(MainActivity.fragmentState.SENSOR);

        return v;
    }
    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        lstSen = (ListView) getView().findViewById(R.id.lstSen);
        sensorAdaptor = ((MainActivity)getActivity()).ruleAdaptor;

        populateListView();
    }

    @Override
    public void onResume(){
        super.onResume();
        ((MainActivity)getActivity()).navView.setCheckedItem(R.id.nav_sensor);
    }

    /**
     * Populates the list with the data from the adapter in main activity
     * */
    private void populateListView() {
        sensorAdaptor = null;
        sensorAdaptor = ((MainActivity)getActivity()).sensorAdaptor;

        lstSen.setAdapter(sensorAdaptor);

        if(sensorAdaptor != null)
        {
            Log.d("aaaa", "senAdaptor != null");
            sensorAdaptor.notifyDataSetChanged();
        }
    }


    /**
     * Called by main activity when the adapter data for sensors is updated. The local lists are updated and populatelistView is called to show the list of sensors to the user
     * */
    public void updatelist(){
        Log.d("aaaa", "updating");

        sensors = ((MainActivity)getActivity()).sensorList;
        ListOfSensors = ((MainActivity)getActivity()).listOfSensors;

        populateListView();
    }

    /**
     * Handles the onClick events for this fragment.
     * When the button is pressed, a list of sensors are requested from the server
     * */
    public void onClickOp(View v){
        switch(v.getId()){
            case R.id.GetSen:
                try {
                    Log.d("aaaa", "Fetching...");
                    byte[] send;
                    StringBuffer outStringBuff = new StringBuffer("");
                    outStringBuff.setLength(0);
                    outStringBuff.append("R:AS");
                    send = outStringBuff.toString().getBytes();
                    ((MainActivity) getActivity()).BTservice.write(send);
                }catch(Exception e){
                    Log.d("aaaa", "Couldn't send request.");
                    e.printStackTrace();
                }
                break;
        }

    }
}
