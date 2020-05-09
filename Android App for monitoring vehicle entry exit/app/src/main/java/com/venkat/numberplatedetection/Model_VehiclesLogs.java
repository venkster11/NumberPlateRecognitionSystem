package com.venkat.numberplatedetection;

public class Model_VehiclesLogs {
    private String plate_num;
    private String status;
    private String time_stamp;
    private String entry_status;

    public Model_VehiclesLogs(String plate_num, String status, String time_stamp, String entry_status) {
        this.plate_num = plate_num;
        this.status = status;
        this.time_stamp = time_stamp;
        this.entry_status = entry_status;
    }

    public Model_VehiclesLogs() {
    }

    public String getPlate_num() {
        return plate_num;
    }

    public void setPlate_num(String plate_num) {
        this.plate_num = plate_num;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getTime_stamp() {
        return time_stamp;
    }

    public void setTime_stamp(String time_stamp) {
        this.time_stamp = time_stamp;
    }

    public String getEntry_status() {
        return entry_status;
    }

    public void setEntry_status(String entry_status) {
        this.entry_status = entry_status;
    }
}
