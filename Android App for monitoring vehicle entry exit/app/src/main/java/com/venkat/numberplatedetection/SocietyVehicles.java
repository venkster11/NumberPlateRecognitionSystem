package com.venkat.numberplatedetection;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;

import com.firebase.ui.firestore.FirestoreRecyclerOptions;
import com.google.firebase.firestore.CollectionReference;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.Query;

public class SocietyVehicles extends AppCompatActivity {

    private FirebaseFirestore db = FirebaseFirestore.getInstance();
    private CollectionReference colref_soc_vehi = db.collection("Society_Vehicles");
    private Adapter_SocietyVehicles adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_society_vehicles);
        setupRecycler();
    }

    public void setupRecycler(){

        Query query = colref_soc_vehi.orderBy("vehi_num",Query.Direction.ASCENDING);
        FirestoreRecyclerOptions<Model_SocietyVehivcles> options = new FirestoreRecyclerOptions.Builder<Model_SocietyVehivcles>()
                .setQuery(query,Model_SocietyVehivcles.class)
                .build();

        adapter = new Adapter_SocietyVehicles(options);

        RecyclerView recyclerView = findViewById(R.id.rv_soc_vehicles);
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
