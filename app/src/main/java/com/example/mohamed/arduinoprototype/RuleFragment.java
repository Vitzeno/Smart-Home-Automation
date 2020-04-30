package com.example.mohamed.arduinoprototype;

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

import org.w3c.dom.Text;

import java.util.ArrayList;
import java.util.HashMap;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

public class RuleFragment extends Fragment
{
    public ListView lstRule;
    private Button del, add, rul;
    private boolean delete = false;
    private String[] requests = {"R:AR", "R:R"};


    private ArrayAdapter<String> ruleAdaptor;
    private ArrayList<String> rules;
    private ArrayList<String> ids = new ArrayList<>();
    private HashMap<String, String> listOfRules = new HashMap<String, String>();


    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_rule, container, false);

        ((MainActivity)getActivity()).setfragmentstate(MainActivity.fragmentState.RULE);

        del = v.findViewById(R.id.DeleteRules);
        add = v.findViewById(R.id.NewRule);
        rul = v.findViewById(R.id.GetRules);
        delete = false;


        return v;
    }

    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        lstRule = (ListView) getView().findViewById(R.id.lstRule);
        ruleAdaptor = ((MainActivity)getActivity()).ruleAdaptor;

        populateListView();
        setUpListner();
    }
    @Override
    public void onResume(){
        super.onResume();
        ((MainActivity)getActivity()).navView.setCheckedItem(R.id.nav_rule);
    }

    /**
     * Populates the list with data from the adaptor in main.
     * Called by the update function.
     * */
    private void populateListView() {
        ruleAdaptor = null;
        ruleAdaptor = ((MainActivity)getActivity()).ruleAdaptor;

        lstRule.setAdapter(ruleAdaptor);

        if(ruleAdaptor != null)
        {
            Log.d("aaaa", "Ruleadaptor != null");
            ruleAdaptor.notifyDataSetChanged();
        }
    }

    /**
     * Called by main when the adaptor for rules is changed. The corresponding local lists are updated and populateListView is called
     * */
    public void updatelist(){
        Log.d("aaaa", "updating");
        rules = ((MainActivity)getActivity()).ruleList;
        listOfRules = ((MainActivity)getActivity()).listOfRules;
        //ruleAdaptor.notifyDataSetChanged();
        populateListView();
    }

    /**
     * Responsible for the onClick events for this fragment.
     * Toggle the delete variable used to delete rules.
     * Fetch a set of existing rules from the server to populate the list with
     *
     * @param v The current view
     * */
    public void onClickOp(View v){
        switch (v.getId()) {
            case R.id.DeleteRules:
                delete = !delete;
                int color = (delete == true) ? Color.GREEN : Color.BLUE;
                v.findViewById(R.id.DeleteRules).setBackgroundColor(color);
                Log.d("aaaa", "Del: " + delete);
                break;
            case R.id.GetRules:

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
        }
    }

    /**
     * Set up the listener for items within the rule listview.
     * When presssed, if delete is true, a delete rule command is send over to the server to delete the selected rule from the list.
     * */
    public void setUpListner() {

        //lstView = (ListView) findViewById(R.id.lstDevices);
        lstRule.setClickable(true);
        lstRule.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> arg0, View view, int position, long arg3) {

                TextView rule = (TextView) view.findViewById(R.id.txtName);
                String tmp = rule.getText().toString();
                String id = tmp.substring(tmp.indexOf("ID: ") +4, tmp.indexOf(" Device"));
                Log.d("aaaa","Pressed!" + id);

                if(delete) {
                    try {
                        Log.d("aaaa", "Deleting...");
                        byte[] send;
                        StringBuffer outStringBuff = new StringBuffer("");
                        outStringBuff.setLength(0);
                        outStringBuff.append("C:R:D:");
                        outStringBuff.append(id);
                        send = outStringBuff.toString().getBytes();
                        ((MainActivity) getActivity()).BTservice.write(send);
                    }catch(Exception e){
                        Log.d("aaaa", "Couldn't send command.");
                        e.printStackTrace();
                    }
                }
            }
        });
    }
}
