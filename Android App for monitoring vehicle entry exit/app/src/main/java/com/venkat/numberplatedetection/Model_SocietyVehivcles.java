package com.venkat.numberplatedetection;

public class Model_SocietyVehivcles {

    private String vehi_num;
    private String vehi_name;

    public Model_SocietyVehivcles(String vehi_num, String vehi_name) {
        this.vehi_num = vehi_num;
        this.vehi_name = vehi_name;
    }

    public Model_SocietyVehivcles(){

    }

    public String getVehi_num() {
        return vehi_num;
    }

    public void setVehi_num(String vehi_num) {
        this.vehi_num = vehi_num;
    }

    public String getVehi_name() {
        return vehi_name;
    }

    public void setVehi_name(String vehi_name) {
        this.vehi_name = vehi_name;
    }
}
