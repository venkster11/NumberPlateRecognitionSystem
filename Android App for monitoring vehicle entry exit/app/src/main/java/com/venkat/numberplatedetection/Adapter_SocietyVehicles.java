package com.venkat.numberplatedetection;

import android.support.annotation.NonNull;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.firebase.ui.firestore.FirestoreRecyclerAdapter;
import com.firebase.ui.firestore.FirestoreRecyclerOptions;

public class Adapter_SocietyVehicles extends FirestoreRecyclerAdapter<Model_SocietyVehivcles, Adapter_SocietyVehicles.VehicleSocietyViewHolder> {

    /**
     * Create a new RecyclerView adapter that listens to a Firestore Query.  See {@link
     * FirestoreRecyclerOptions} for configuration options.
     *
     * @param options
     */
    public Adapter_SocietyVehicles(@NonNull FirestoreRecyclerOptions<Model_SocietyVehivcles> options) {
        super(options);
    }

    @Override
    protected void onBindViewHolder(@NonNull VehicleSocietyViewHolder holder, int position, @NonNull Model_SocietyVehivcles model) {
        holder.vehicleNum.setText(model.getVehi_num());
        holder.vehicleName.setText(model.getVehi_name());
    }

    @NonNull
    @Override
    public VehicleSocietyViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
        View v = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.item_society_vehicles,viewGroup,false);
        return new Adapter_SocietyVehicles.VehicleSocietyViewHolder(v);
    }

    class VehicleSocietyViewHolder extends RecyclerView.ViewHolder{

        TextView vehicleName;
        TextView vehicleNum;

        public VehicleSocietyViewHolder(@NonNull View itemView) {
            super(itemView);

            vehicleNum = itemView.findViewById(R.id.vehi_num);
            vehicleName = itemView.findViewById(R.id.vehi_name);
        }
    }
}
