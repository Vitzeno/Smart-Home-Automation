package com.example.mohamed.arduinoprototype;

import android.content.Context;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Spinner;
import android.widget.TextView;

import java.util.Arrays;
import java.util.List;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

public class AddRuleFragment extends Fragment
{
    private enum clear{ FULL, PARTIAL};

    private View view;
    private static String commandStr;
    private static String userStr = "Rule: (empty)";
    private TextView commandLn;
    private Spinner sen,val,op, multi;
    private String [] vals = {"0","1","2","3","4","5","6","7","8","9"};
    private String [] ops = {"LE","GE","EQ"};
    private String [] mult = {"AND", "OR", "NOT"};

    public int rulecount = 0;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.fragment_add_rule, container, false);

        sen = view.findViewById(R.id.Sen);
        val = view.findViewById(R.id.Val);
        op = view.findViewById(R.id.Op);
        multi = view.findViewById(R.id.Multi);

        return view;
    }

    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        commandStr = "C:R:C:";
        commandLn = getView().findViewById(R.id.commandLine);
        rulecount = 0;
        multi.setVisibility(View.GONE);

        Reset(clear.FULL);

//        updateStr(null);

    }
    private void Reset(clear c){
        if(c == clear.PARTIAL || c == clear.FULL) {
            ArrayAdapter<String> valAdapter = new ArrayAdapter<String>(this.getActivity(), android.R.layout.simple_spinner_item, vals);
            ArrayAdapter<String> opAdapter = new ArrayAdapter<String>(this.getActivity(), android.R.layout.simple_spinner_item, ops);
            ArrayAdapter<String> multiAdapter = new ArrayAdapter<String>(this.getActivity(), android.R.layout.simple_spinner_item, mult);

            valAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
            opAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
            multiAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);

            sen.setAdapter(valAdapter);
            val.setAdapter(valAdapter);
            op.setAdapter(opAdapter);
            multi.setAdapter(multiAdapter);
        }
        if(c == clear.FULL) {
            updateStr(null);
            updateUserStr(null);
            rulecount = 0;
            multi.setVisibility(View.GONE);
        }
    }
    private void updateStr(String str){
        if(str != null)
            commandStr = commandStr + str;
        else
            commandStr = "C:R:C";

        //commandLn.setText(commandStr);
        Log.d("aaaa", commandStr);
        if(rulecount > 0){
            multi.setVisibility(View.VISIBLE);
        }

    }
    private void updateUserStr(String str){

        if(str != null) {
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

    public void onClickOp(View v){
        switch (v.getId()){

            case R.id.ADD:
                String value = ":" + val.getSelectedItem().toString();
                String sensor = ":" + sen.getSelectedItem().toString();
                String operator = ":" + op.getSelectedItem().toString();
                String additional = "";
                if(rulecount > 0)
                     additional =  ":" + multi.getSelectedItem().toString();

                updateUserStr(additional + sensor + operator + value);

                val.setAdapter(null);
                sen.setAdapter(null);
                op.setAdapter(null);
                multi.setAdapter(null);

                rulecount++;

                updateStr(sensor + value + operator + additional);

                Reset(clear.PARTIAL);
                break;

            case R.id.Clear:
                Log.d("aaaa","Clearing box");
                Reset(clear.FULL);
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
