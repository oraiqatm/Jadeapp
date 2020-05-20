package com.example.raspberrypi_app;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.io.UnsupportedEncodingException;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {
    public static final String TAG = "MYTAG";
    RequestQueue QUEUE;
    String URLHTTP;
    Button LIGHT_BTN;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //Server Components
        QUEUE = Volley.newRequestQueue(this);
        URLHTTP = getResources().getString(R.string.httpURL);

        //Buttons
        LIGHT_BTN = findViewById(R.id.light_btn);

        //Onlick Listen for Light BTN
        LIGHT_BTN.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                httpPost(URLHTTP, "LightOn");
            }
        });

        httpGet(URLHTTP);



    }
    public void httpGet(String url){
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        Log.d(TAG, "RESPONSE FROM SERVER [GET]: " + response);
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        try{
                            String responseBody = new String(error.networkResponse.data, "utf-8");
                        }catch (UnsupportedEncodingException errorr){
                            Log.d(TAG, errorr.toString());
                        }
                    }
                });
        QUEUE.add(stringRequest);
    }

    public void httpPost(String url, final String rasp_command){
        StringRequest postrequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        Log.d(TAG, "RESPONSE FROM SERVER: " + response);
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        try{
                            String responseBody = new String(error.networkResponse.data, "utf-8");
                        }catch (UnsupportedEncodingException errorr){
                            Log.d(TAG, errorr.toString());
                        }
                    }
        }){
            @Override
            protected Map<String, String> getParams(){
                Map<String, String> params = new HashMap<String, String>();
                params.put("Rasp_Command", rasp_command); //Post data key= Name, value = johndoe
                System.out.println(params);
                return params;
            }
        };
        QUEUE.add(postrequest);
    }



}
