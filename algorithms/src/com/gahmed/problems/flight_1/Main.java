package com.gahmed.problems.flight_1;

public class Main {
    public static void main(String[] args) {
        CityGraph cityGraph = new CityGraph();

        City ams = new City(1, "Amsterdam", 0);
        City paris = new City(2, "Paris", 300);
        City lisbon = new City(3, "Lisbon", 200);
        City london = new City(4, "London", 500);

        cityGraph.addRoute(ams, new Flight(paris, 150, 10));
        cityGraph.addRoute(paris, new Flight(london, 200, 15));
        cityGraph.addRoute(paris, new Flight(lisbon, 40, 14));
        cityGraph.addRoute(lisbon, new Flight(ams, 100, 20));
        cityGraph.addRoute(lisbon, new Flight(london, 100, 17));
        cityGraph.addRoute(london, new Flight(ams, 200, 21));

        Solver solver = new Solver(cityGraph, ams);
        solver.solve(10, 15, 5000);
        System.out.println("The route is: " + solver.maxTripRoute);
    }
}
