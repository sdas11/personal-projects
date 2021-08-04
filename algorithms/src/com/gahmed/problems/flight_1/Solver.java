package com.gahmed.problems.flight_1;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Solver {
    private CityGraph cityGraph;
    private City home;

    public Solver(CityGraph cityGraph, City home) {
        this.cityGraph = cityGraph;
        this.home = home;
    }

    // First lets do regular recursion DFS - later we will adapt to BFS
    public void solve(int startDate, int maxDays, int budget) {
        dfs(
            this.home,
            startDate,
            maxDays,
            budget,
            new HashSet<>(),
        0,
            new ArrayList<>()
        );
    }

    public int maxTripTotal = -1;
    public int finalMoneyLeft = 0;
    public List<Flight> maxTripRoute = null;

    public void dfs(
            City currCity, int arrivalDate, int daysLeft, int budgetLeft,
            Set<City> visited, int tripTotal, List<Flight> routeUptoNow
    ) {
        if (budgetLeft < 0 || daysLeft < 0) {
            return;
        }

        if (routeUptoNow.size() > 0 && currCity == this.home) {
            if (tripTotal > maxTripTotal) {
                // better solution found
                maxTripTotal = tripTotal;
                finalMoneyLeft = budgetLeft;
                maxTripRoute = routeUptoNow;
            }
        }

        if (!(currCity == this.home)) {
            visited.add(currCity); // don't add starting city / home city to visited - to be able to return back
        }
        List<Flight> flights = cityGraph.outgoing.get(currCity);
        for (Flight flight : flights) {
            int daysUsedUp = flight.date - arrivalDate;
            int daysSpentOnTrip = routeUptoNow.size() > 0 ? daysUsedUp : 0; // don't start trip counter till first flight

            // for home city - anyways chargePerNight = 0 , so adding no check - otherwise substitute with daysSpentOnTrip
            int budgetLeftAfterAcc = budgetLeft - (daysUsedUp * currCity.chargePerNight);

            if (flight.date >= arrivalDate && !visited.contains(flight.dest) && budgetLeftAfterAcc >= flight.charge) {
                List<Flight> copy = new ArrayList<>(routeUptoNow);
                copy.add(flight);
                dfs(
                    flight.dest,
                    flight.date,
                    daysLeft - daysUsedUp,
                    budgetLeftAfterAcc - flight.charge,
                    new HashSet<>(visited),
                    tripTotal + daysSpentOnTrip,
                    copy
                );
            }
        }
    }
}
