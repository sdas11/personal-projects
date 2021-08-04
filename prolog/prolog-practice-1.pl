avg_temp(phx, 100).
avg_temp(sf, 68).

avg_temp_cels(Location, C_Temp) :-
	avg_temp(Location, F_Temp),      % first F_Temp will mutate from the fact match
	C_Temp is (F_Temp - 32) * 5/9.   % then C_Temp will be manually mutated

/*

Let's query the rule to store the "converted" answer in our variable

?- avg_temp_cels(sf, Cels).
Cels = 20.
	
*/