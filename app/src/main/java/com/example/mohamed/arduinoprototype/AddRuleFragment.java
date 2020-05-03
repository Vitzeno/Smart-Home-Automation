package com.example.mohamed.arduinoprototype;

import android.app.Dialog;
import android.app.TimePickerDialog;
import android.os.Bundle;
import android.text.format.DateFormat;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.TimePicker;

import java.sql.Time;
import java.util.Calendar;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.DialogFragment;
import androidx.fragment.app.Fragment;

public class AddRuleFragment extends Fragment
{
    private enum clear{ FULL, PARTIAL};

    private View view;
    private static String commandStr;
    private static String userStr = "Rule: (empty)";
    private TextView commandLn;
    private Spinner sen,type,op, multi, devices;
    private TextView time;
    private EditText temp;
    private Button stateSwitch;
    private String [] vals = {"1","2","3","4","5","6","7","8","9"};
    private String [] types = {"Time", "Temperature"};
    private String [] ops = {"<",">","=="};
    private String [] mult = {"AND", "OR", "NOT"};
    private long timeval;

    public int rulecount = 0;
    private int ruleState = 1;
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.fragment_add_rule, container, false);

        return view;
    }

    /**
     * Once the view is created, assign the objects and attach the listener to the time button
     * The variables are also initialised here
     **/
    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        commandStr = "C:R:C:";
        commandLn = getView().findViewById(R.id.commandLine);
        rulecount = 0;

        stateSwitch = view.findViewById(R.id.ruleState);
        type = view.findViewById(R.id.Type);
        devices = view.findViewById(R.id.Device);
        sen = view.findViewById(R.id.Sen);
        //val = view.findViewById(R.id.TimeVal);
        time = view.findViewById(R.id.TimeVal);
        temp = view.findViewById(R.id.Temp);
        op = view.findViewById(R.id.Op);
        multi = view.findViewById(R.id.Multi);
        multi.setVisibility(View.GONE);

        time.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Calendar mcurrentTime = Calendar.getInstance();
                int hour = mcurrentTime.get(Calendar.HOUR_OF_DAY);
                int minute = mcurrentTime.get(Calendar.MINUTE);

                TimePickerDialog tp = new TimePickerDialog(getActivity(), new TimePickerDialog.OnTimeSetListener() {
                    @Override
                    public void onTimeSet(TimePicker timePicker, int i, int i1) {
                        time.setText(i + ":" + i1);
                        timeval = 60*i + i1;
                    }
                }, hour, minute, true);
                tp.setTitle("Pick time");
                tp.show();
            }
        });
        time.setVisibility(View.GONE);

        temp.setVisibility(View.VISIBLE);

        Reset(clear.FULL);

//        updateStr(null);

    }
    /**
     * Responsible for maintaining the values held with the container. The values are reset whenever a message is sent over to the server.
     * Partial clearing, such as when a rule has multiple parts, only resets the spinners.
     * Full clearing resets everything, returning the fragment to a default state.
     *
     * @param c The level of clearing required. Can be FULL or PARTIAL
     * */
    private void Reset(clear c){
        if(c == clear.PARTIAL || c == clear.FULL) {
            ArrayAdapter<String> valAdapter = new ArrayAdapter<String>(this.getActivity(),R.layout.spinner_layout, vals);
            ArrayAdapter<String> opAdapter = new ArrayAdapter<String>(this.getActivity(),R.layout.spinner_layout, ops);
            ArrayAdapter<String> multiAdapter = new ArrayAdapter<String>(this.getActivity(), R.layout.spinner_layout, mult);
            ArrayAdapter<String> typeAdapter = new ArrayAdapter<String>(this.getActivity(), R.layout.spinner_layout, types);
            ArrayAdapter<String> deviceAdapter = new ArrayAdapter<String>(this.getActivity(), R.layout.spinner_layout, vals);

            valAdapter.setDropDownViewResource(R.layout.spinner_layout);
            opAdapter.setDropDownViewResource(R.layout.spinner_layout);

            multiAdapter.setDropDownViewResource(R.layout.spinner_layout);
            typeAdapter.setDropDownViewResource(R.layout.spinner_layout);
            deviceAdapter.setDropDownViewResource(R.layout.spinner_layout);

            devices.setAdapter(deviceAdapter);
            sen.setAdapter(valAdapter);
            type.setAdapter(typeAdapter);
            temp.setText("15");
            op.setAdapter(opAdapter);
            multi.setAdapter(multiAdapter);


            type.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
                @Override
                public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                    if(type.getSelectedItem().toString() == "Time"){
                        time.setVisibility(View.VISIBLE);
                        temp.setVisibility(View.GONE);
                    }else if( type.getSelectedItem().toString() == "Temperature"){
                        time.setVisibility(View.GONE);
                        temp.setVisibility(View.VISIBLE);
                    }else{
                        time.setVisibility(View.VISIBLE);
                        temp.setVisibility(View.GONE);
                    }
                }

                @Override
                public void onNothingSelected(AdapterView<?> adapterView) {
                    time.setVisibility(View.VISIBLE);
                    temp.setVisibility(View.GONE);

                    type.setSelection(1);
                }
            });
        }
        if(c == clear.FULL) {
            updateStr(null);
            updateUserStr(null);
            rulecount = 0;
            multi.setVisibility(View.GONE);
            stateSwitch.setVisibility(View.VISIBLE);

        }
    }
    /**
     * Takes a rule as a string, appending it the end of an existing rule string to be sent off to the server
     * @param str The rule to be added to the final rule list
     **/
    private void updateStr(String str){
        if(str != null)
            commandStr = commandStr + str;
        else
            commandStr = "C:R:C";

        //commandLn.setText(commandStr);
        Log.d("aaaa", commandStr);
        if(rulecount > 0){
            multi.setVisibility(View.VISIBLE);
            stateSwitch.setVisibility(View.GONE);
        }

    }

    /**
     * Converts the rule created by the user into something user readable, ready to be displayed.
     * @param str The string to be converted
     * */
    private void updateUserStr(String str){

        if(str != null) {
            if(rulecount == 0){
                str = str.replaceFirst(":", "Device ");
                str = str.replaceFirst(":" , ";");
            }
            Log.d("aaaa", "userstr : " + str);
            str = str.replace("GE", "Greater Than");
            str = str.replace(":", " ");
            str = str.replace("LE", "Less Than");
            str = str.replace("EQ", "Equals");
            userStr = userStr + str;
        }
        else{
            userStr = "";
        }
        //userStr = userStr + str;
        commandLn.setText(userStr);
    }

    /**
     * Function responsible for the button clicks within the fragment.
     * Handles the add, clear, send and state functionality.
     *
     * @param v The current view containing the buttons
     * */
    public void onClickOp(View v){
        switch (v.getId()){

            case R.id.ADD:
                String value = "";
                String sensor = "";
                String state = (rulecount > 0) ? "" : ":" + ruleState;
                String stateStr = (rulecount > 0) ? "" : stateSwitch.getText().toString();
                String device = "";
                device = ":" + devices.getSelectedItem().toString();

                if(type.getSelectedItem().toString() == "Time")
                {
                    value = ":" + timeval;
                    sensor = ":0";
                }
                else if(type.getSelectedItem().toString() == "Temperature")
                {
                    value = ":" + (temp.getText().toString().isEmpty() ? "15" : temp.getText().toString());
                    sensor =":" + sen.getSelectedItem().toString();
                }

                String operator =  op.getSelectedItem().toString();
                if(operator.equals("<"))
                    operator = ":LE";
                else if(operator.equals(">"))
                    operator = ":GE";
                else
                    operator = ":EQ";

                String additional = "";
                if(rulecount > 0)
                {
                    additional =  ":" + multi.getSelectedItem().toString();
                    device = "";
                }
                Log.d("aaaa",type.getSelectedItem().toString());
                if(type.getSelectedItem().toString() == "Time")
                    updateUserStr(device +":"+ stateStr + ":" + additional + ":Time" + operator + ":" + time.getText().toString());
                else if(type.getSelectedItem().toString() == "Temperature")
                    updateUserStr(device +":"+ stateStr + ":" + additional + sensor + operator + value);

                //val.setAdapter(null);
                sen.setAdapter(null);
                op.setAdapter(null);
                multi.setAdapter(null);


                rulecount++;

                updateStr(device + state + sensor + value + operator + additional);

                Reset(clear.PARTIAL);
                break;

            case R.id.Clear:
                Log.d("aaaa","Clearing box");
                Reset(clear.FULL);
                break;
            case R.id.ruleState:
                ruleState = (ruleState == 1)? 0 : 1;
                String t = (ruleState == 1) ? "On" : "Off";
                stateSwitch.setText(t);
                break;
            case R.id.Send:
                if(rulecount > 0) {
                    Log.d("aaaa", "Attempting to send");
                    try {
                        byte[] send;

                        StringBuffer outStringBuff = new StringBuffer("");
                        outStringBuff.setLength(0);
                        outStringBuff.append(commandStr);
                        send = outStringBuff.toString().getBytes();
                        ((MainActivity) getActivity()).BTservice.write(send);
                        //BTservice.write(send);

                    }catch (Exception e) {
                        Log.d("aaaa", "Error, couldn't send. Check connection");
                        Log.d("aaaa", e.toString());
                    }
                }
                else
                {
                    Log.d("aaaa", "Too few rules to send.");
                }
                Reset(clear.FULL);
                break;
        }
    }
}
