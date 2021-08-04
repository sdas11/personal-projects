package com.gahmed.problems.flight_1;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class CityGraph {
    public Set<City> cities = new HashSet<>();
    public Map<City, List<Flight>> outgoing = new HashMap<>();

    public void addRoute(City a, Flight flight) {
        cities.add(a);
        cities.add(flight.dest);

        if (flight.dest.equals(a)) {
            System.out.println("Cannot add a flight to self");
            return;
        }

        // I am not checking for duplicate flights on the same day - so don't put it -
        // If user deliberately wants to put duplicates, use a Set<Route>
        if (outgoing.containsKey(a)) {
            outgoing.get(a).add(flight);
        } else {
            List<Flight> temp = new ArrayList<>();
            temp.add(flight);
            outgoing.put(a, temp);
        }
    }
}
