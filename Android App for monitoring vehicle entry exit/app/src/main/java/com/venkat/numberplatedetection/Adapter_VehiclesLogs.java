package com.venkat.numberplatedetection;

import android.support.annotation.NonNull;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.firebase.ui.firestore.FirestoreRecyclerAdapter;
import com.firebase.ui.firestore.FirestoreRecyclerOptions;
import com.google.firebase.firestore.CollectionReference;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.EventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.FirebaseFirestoreException;
import com.google.firebase.firestore.Query;
import com.google.firebase.firestore.QueryDocumentSnapshot;
import com.google.firebase.firestore.QuerySnapshot;

import javax.annotation.Nullable;

public class Adapter_VehiclesLogs extends FirestoreRecyclerAdapter<Model_VehiclesLogs,Adapter_VehiclesLogs.VehiclesLogsViewHolder> {

    /**
     * Create a new RecyclerView adapter that listens to a Firestore Query.  See {@link
     * FirestoreRecyclerOptions} for configuration options.
     *
     * @param options
     */
    public Adapter_VehiclesLogs(@NonNull FirestoreRecyclerOptions<Model_VehiclesLogs> options) {
        super(options);
    }

    @Override
    protected void onBindViewHolder(@NonNull final VehiclesLogsViewHolder holder, int position, @NonNull final Model_VehiclesLogs model) {
        holder.vehicleNum.setText(model.getPlate_num());
        holder.timeStamp.setText(model.getTime_stamp());
        final String vnum = model.getPlate_num();
        final int[] flag = {0};
        CollectionReference collref_status = FirebaseFirestore.getInstance().collection("Society_Vehicles");
        CollectionReference collref_entry = FirebaseFirestore.getInstance().collection("currentlogs");

        collref_status.addSnapshotListener(new EventListener<QuerySnapshot>() {
            @Override
            public void onEvent(@Nullable QuerySnapshot queryDocumentSnapshots, @Nullable FirebaseFirestoreException e) {
                //Log.d("mello", "onEvent:vnum ");

                if (e != null) {
                    return;
                }

                for (QueryDocumentSnapshot documentSnapshot : queryDocumentSnapshots){

//                    Log.d("mello", "onEvent:vnum "+vnum);
//                    Log.d("mello", "onEvent:docnum "+documentSnapshot.getString("vehi_num"));
                    if(vnum.equals(documentSnapshot.getString("vehi_num"))){
//                        Log.d("mello", "onEvent:vnum "+vnum);
//                        Log.d("mello", "onEvent:docnum "+documentSnapshot.getString("vehi_num"));
                        holder.status.setText("Society Vehicle");
                        flag[0] = 1;
                        break;
                    }
                }
//                Log.d("mello", "onEvent:vnum flag "+flag[0]);
                if( flag[0] == 0){
                    holder.status.setText("Not a Society Vehicle");
                }
            }
        });

        Query query = FirebaseFirestore.getInstance()
                .collection("currentlogs")
                .orderBy("time_stamp");
        final int[] count = new int[1];
        query.addSnapshotListener(new EventListener<QuerySnapshot>() {
            @Override
            public void onEvent(@Nullable QuerySnapshot queryDocumentSnapshots, @Nullable FirebaseFirestoreException e) {
                if (e != null) {
                    return;
                }

                int count11 = 0;
                for (QueryDocumentSnapshot documentSnapshot : queryDocumentSnapshots){
                    if(vnum.equals(documentSnapshot.getString("plate_num"))){
                        count11++;
                    }
                }

                String DocID = null;
                for (QueryDocumentSnapshot documentSnapshot : queryDocumentSnapshots){
                    if(vnum.equals(documentSnapshot.getString("plate_num"))){
                        count[0]++;
                        Log.d("mello", documentSnapshot.getId()+" onEvent:vnum "+count[0]);
                        DocID = documentSnapshot.getId();
                        FirebaseFirestore db = FirebaseFirestore.getInstance();
                        DocumentReference vehi_log_Ref = db.collection("currentlogs").document(DocID);
                        if(count[0]%2 == 0){
                            vehi_log_Ref.update("entry_status", "Vehicle Exited");
                            holder.entryStatus.setText(model.getEntry_status());
                            Log.d("abc", "Vehicle Exited");
                        }
                        else{
                            vehi_log_Ref.update("entry_status", "Vehicle Entered");
                            holder.entryStatus.setText(model.getEntry_status());
                            Log.d("abc", "Vehicle Entered");
                        }
                    }
                    if(count[0] == count11){
                        break;
                    }
                }

                count[0]=0;



                //Log.d("mello", "last "+count[0]+" "+vnum);
            }
        });

    }

    @NonNull
    @Override
    public VehiclesLogsViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
        View v = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.item_vehicle_logs,viewGroup,false);
        return new Adapter_VehiclesLogs.VehiclesLogsViewHolder(v);
    }

    class VehiclesLogsViewHolder extends RecyclerView.ViewHolder{

        TextView vehicleNum;
        TextView timeStamp;
        TextView status;
        TextView entryStatus;

        public VehiclesLogsViewHolder(@NonNull View itemView) {
            super(itemView);

            vehicleNum = itemView.findViewById(R.id.logs_vehi_num);
            timeStamp = itemView.findViewById(R.id.logs_timestamp);
            status = itemView.findViewById(R.id.logs_status);
            entryStatus = itemView.findViewById(R.id.logs_entry_status);
        }
    }
}
