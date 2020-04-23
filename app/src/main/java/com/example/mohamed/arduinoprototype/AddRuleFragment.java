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
    private View view;
    private static String commandStr;
    private static String userStr = "";
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

        SetSpinners();

        return view;
    }

    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        commandStr = "C:R:C:";
        commandLn = getView().findViewById(R.id.commandLine);
        rulecount = 0;
        multi.setVisibility(View.GONE);

        updateStr(null);

    }
    private void SetSpinners(){
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

        Log.d("aaaa", "userstr : " + str );
        str = str.replace("GE", "Greater Than");
        str = str.replace(":", " ");
        str = str.replace("LE", "Less Than");
        str = str.replace("EQ", "Equals");

        userStr = userStr + str;
        commandLn.setText(userStr);
    }

    public void onClickOp(View v){
        switch (v.getId()){
            /*case R.id.GE:
                Log.d("aaaa", ":GE");
                updateStr(":GE");
                break;
            case R.id.LE:
                Log.d("aaaa", ":LE");
                updateStr(":LE");
                break;
            case R.id.EQ:
                Log.d("aaaa", "EQ");
                updateStr(":EQ");
                break;
            case R.id.AND:
                Log.d("aaaa", "AND");
                updateStr(":AND");
                break;
            case R.id.OR:
                Log.d("aaaa", "OR");
                updateStr(":OR");
                break;
            case R.id.NOT:
                Log.d("aaaa", "NOT");
                updateStr(":NOT");
                break;*/
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

                SetSpinners();
                break;
        }
    }
}
