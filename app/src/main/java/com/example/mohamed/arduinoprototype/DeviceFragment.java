package com.example.mohamed.arduinoprototype;

import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

public class DeviceFragment extends Fragment
{
    public ListView lstDev;
    private ArrayAdapter<String> objAdapter;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_device, container, false);

        ((MainActivity)getActivity()).setfragmentstate(MainActivity.fragmentState.DEVICE);

        return v;
    }
    @Override
    public void onResume(){
        super.onResume();
        ((MainActivity)getActivity()).navView.setCheckedItem(R.id.nav_device);
    }

    private void populateListView() {
        objAdapter = null;
        objAdapter = ((MainActivity)getActivity()).ObjAdaptor;

        //lstRule.setAdapter(ruleAdaptor);

        if(objAdapter != null)
        {
            Log.d("aaaa", "Ruleadaptor == null");
            objAdapter.notifyDataSetChanged();
        }
    }


    public void onClickOp(View v){
        switch(v.getId()){

        }

    }

    public void updatelist(){
        Log.d("aaaa", "updating");

        //populateListView();
    }
}
