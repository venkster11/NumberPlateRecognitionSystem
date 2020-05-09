package com.venkat.numberplatedetection;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    private Button society_vehicles;
    private Button vehicles_logs;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        society_vehicles = findViewById(R.id.soc_vehicles_btn);
        vehicles_logs = findViewById(R.id.vehicles_logs);

        society_vehicles.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this,SocietyVehicles.class);
                startActivity(intent);
            }
        });

        vehicles_logs.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this,VehiclesLogs.class);
                startActivity(intent);
            }
        });
    }
}
