package com.gahmed.problems.flight_1;

public class Flight {
    // no need for origin as of now .. maintained in adjacencyList in CityGraph class

    public City dest;
    public int charge; // assume currency is same for every flight

    // assume same month and year for every flight - else change this to Date class
    // assume every flight arrives at the destination city in the same day
    public int date;

    public Flight(City dest, int charge, int date) {
        this.dest = dest;
        this.charge = charge;
        this.date = date;
    }
}
