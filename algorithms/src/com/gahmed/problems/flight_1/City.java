package com.gahmed.problems.flight_1;

import java.util.Objects;

public class City {
    // id must be unique - user has to take care ..
    // if user doesn't want to take care, modify the CityGraph.addRoute method to throw error
    public int id;

    public String name;
    public int chargePerNight;

    public City(int id, String name, int chargePerNight) {
        this.id = id;
        this.name = name;
        this.chargePerNight = chargePerNight;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        City city = (City) o;
        return id == city.id;
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return "{name: '" + name + '\'' + "}";
    }
}
