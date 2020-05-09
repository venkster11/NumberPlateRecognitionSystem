package com.venkat.numberplatedetection;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;

import com.firebase.ui.firestore.FirestoreRecyclerOptions;
import com.google.firebase.firestore.CollectionReference;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.Query;

public class VehiclesLogs extends AppCompatActivity {

    private FirebaseFirestore db = FirebaseFirestore.getInstance();
    private CollectionReference colref_vehi_logs = db.collection("currentlogs");
    private Adapter_VehiclesLogs adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_vehicles_logs);
        setupRecycler();
    }

    public void setupRecycler(){

        Query query = colref_vehi_logs.orderBy("time_stamp",Query.Direction.DESCENDING);
        FirestoreRecyclerOptions<Model_VehiclesLogs> options = new FirestoreRecyclerOptions.Builder<Model_VehiclesLogs>()
                .setQuery(query,Model_VehiclesLogs.class)
                .build();

        adapter = new Adapter_VehiclesLogs(options);

        RecyclerView recyclerView = findViewById(R.id.rv_vehicle_logs);
        recyclerView.setHasFixedSize(true);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setAdapter(adapter);
    }


    @Override
    protected void onStart() {
        super.onStart();
        adapter.startListening();
    }

    @Override
    protected void onStop() {
        super.onStop();
        adapter.stopListening();
    }
}
