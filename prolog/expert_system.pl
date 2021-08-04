% ---- HELPER PREDICATES START ---- %
% Helper predicate to capture 'yes' or 'no' input
valid_input(yes).
valid_input(no).
read_yes_no_input_as_atom(I):-
	read(Inp),
    string_lower(Inp, LInp),
    atom_string(I, LInp),
    valid_input(I).
% ---- HELPER PREDICATES END ---- %


% ---- RISK OF INFECTION START ---- %
visited_virusland(yes, 1).
visited_virusland(no, 0).
% check_country(RiskScore)
check_country(S):-
    write('Have you visited Virusland in the last 14 days? Type yes or no:'), nl,
    read_yes_no_input_as_atom(I),
    visited_virusland(I, S).

visited_virusville(yes, 1).
visited_virusville(no, 0).
% check_city(RiskScore)
check_city(S):-
    write('Have you visited Virusville in the last 14 days? Type yes or no:'), nl,
    read_yes_no_input_as_atom(I),
    visited_virusville(I, S).

% Proximity check
proximity(yes, 1).
proximity(no, 0).
check_proximity(S):-
    write('Have you been in close proximity with someone showing symptoms in the last 14 days? Type yes or no:'), nl,
    read_yes_no_input_as_atom(I),
    proximity(I, S).

% Facts for advising logic for risk of infection
% infection_risk(cumulative_score, advice)
infection_risk_score_advice(0, 'unlikely to be infected').
infection_risk_score_advice(1, 'moderate possibility of being infected').
infection_risk_score_advice(2, 'high chances of being infected').
infection_risk_score_advice(3, 'very high chances of being infected').

risk_infection_advice(Advice):-
    check_country(S1),		% score 1
    check_city(S2),			% score 2
    check_proximity(S3),	% score 3
    InfScr is S1 + S2 + S3,	% cumulative score
	infection_risk_score_advice(InfScr, Advice).
% ---- RISK OF INFECTION END ---- %


% ---- RISK OF DEVELOPING SEVERE SYMPTOMS START ---- %
% Rules for scoring the risk of developing severe symptoms
risk_for_age(Age, Risk):-
    Age =< 70,
    Risk = 0.
risk_for_age(Age, Risk):-
    Age > 70,
    Risk = 1.
preExistingConds(['hypertension', 'diabetes', 'cardiovascular disease', 
                 'chronic respiratory disease', 'cancer']).
risk_for_precondition(yes, 1).
risk_for_precondition(no, 0).
calculate_risk_severe_symptom(R):-
    write('What is your age? Type a number like 29'), nl,
    read(Age),
    risk_for_age(Age, R1),
    write('Do you already have any of the below conditions?'), nl,
    preExistingConds(L), write(L), nl,
    read_yes_no_input_as_atom(I),
    risk_for_precondition(I, R2),
    R is R1 + R2.

% Facts for advising logic for risk of infection
serious_symptom_risk_score_advice(0, 'unlikely chances of developing serious symptoms').
serious_symptom_risk_score_advice(1, 'high possibility of developing serious symptoms').
serious_symptom_risk_score_advice(2, 'extremely high possibility of developing serious symptoms').
risk_develop_serious_symptom_advice(Advice):-
    calculate_risk_severe_symptom(R1),	% Risk Score for Severe Symptoms
    serious_symptom_risk_score_advice(R1, Advice).
% ---- RISK OF DEVELOPING SEVERE SYMPTOMS END ---- %

% ---- GENDER BASED ADVICE START ---- %
% Rules for scoring gender related risk
risk_score_ismale(yes, 1).
risk_score_ismale(no, 0).
calculate_risk_gender(RiskScore):-
    write('Are you biologically identified as a male?'), nl,
    read_yes_no_input_as_atom(I),
    risk_score_ismale(I, RiskScore).

% Facts for advising logic based on gender risk score
gender_risk_score_advice(0, 'Your gender poses no additional risk').
gender_risk_score_advice(1, 
             'Your gender predisposes you to slightly higher chances of developing serious symptoms').
risk_gender_advice(Advice):-
    calculate_risk_gender(RiskScore),
    gender_risk_score_advice(RiskScore, Advice).
% ---- GENDER BASED ADVICE END ---- %

% ---- SYMPTOM BASED ADVICE START ---- %
% Facts for known symptoms
commonSymptoms(['fever', 'persistent dry cough', 'tiredness']).
lessCommonSymptoms(['aches and pains', 'sore throat', 'diarrhoea', 
                   'conjunctivitis', 'headache', 'anosmia/hyposmia (total/partial loss of smell)', 
                   'running nose']).
seriousSymptoms(['difficulty breathing', 'shortness of breath', 'chest pain', 
                'feeling of chest pressure', 'loss of speech', 'loss of movement']).

% check_symptoms(Common, LessCommon, Serious)
gather_sypmtom_input(C, L, S):-
    write('Do you already have any of the below symptoms? Answer yes or no'), nl,
    commonSymptoms(C1), write(C1), nl,
    read_yes_no_input_as_atom(C),
    write('Do you already have any of the below symptoms? Answer yes or no'), nl,
    lessCommonSymptoms(L1), write(L1), nl,
    read_yes_no_input_as_atom(L),
    write('Do you already have any of the below symptoms? Answer yes or no'), nl,
    seriousSymptoms(S1), write(S1), nl,
    read_yes_no_input_as_atom(S).

% Facts for advising logic for symptoms
specific_symptom_advice(
	common_symptom(no),
    less_common_symptom(no),
    serious_symptom(no),
    'You are not infected with the new virus.'
).
specific_symptom_advice(
	common_symptom(yes),
    less_common_symptom(no),
    serious_symptom(no),
    'You are showing the common symptoms (post-infection). Please stay at home. No medical intervention is necessary.'
).
specific_symptom_advice(
	common_symptom(yes),
    less_common_symptom(yes),
    serious_symptom(no),
    'Though you show less common symptoms (post-infection), please stay at home. No medical intervention is neccessary.'
).
specific_symptom_advice(
	common_symptom(yes),
    less_common_symptom(yes),
    serious_symptom(yes),
    'You are showing severe symptoms (post-infection). Please seek immediate medical attention!'
).

find_symptom_advice(C, L, S, Advice):-
    not(specific_symptom_advice(
       common_symptom(C),
            less_common_symptom(L),
            serious_symptom(S),
            Advice
    )),
    Advice = 'No consistent set of symptoms found. Please consult a doctor'.

find_symptom_advice(C, L, S, Advice):-
	specific_symptom_advice(
       common_symptom(C),
            less_common_symptom(L),
            serious_symptom(S),
            Advice
    ).

manifested_symptom_advice(Advice):-
    gather_sypmtom_input(Common, LessCommon, Serious),
    find_symptom_advice(Common, LessCommon, Serious, Advice).
    
% ---- SYMPTOM BASED ADVICE END ---- %

% MAIN PROGRAM
advice(Advice):-
    write('Please input accurately only yes or no when instructed or the program will exit with false'), nl,
    manifested_symptom_advice(DisplaySymptomAdvice),
    risk_infection_advice(InfectionRiskAdvice),
    risk_develop_serious_symptom_advice(SeriousSymptomRiskAdvice),
    risk_gender_advice(GenderSpecificAdvice),
 	% Concatenate Summary into input arg "Advice"
    string_concat(DisplaySymptomAdvice, 
                  ' \n Based on your movement information, your infection risk is: ', TempBuffer1),
    string_concat(TempBuffer1, InfectionRiskAdvice, TempBuffer2),
    string_concat(TempBuffer2, ' \n The risk of developing severe symptoms is: ', TempBuffer3),
    string_concat(TempBuffer3, SeriousSymptomRiskAdvice, TempBuffer4),
    string_concat(TempBuffer4, ' \n Based on your gender info: ', TempBuffer5),
    string_concat(TempBuffer5, GenderSpecificAdvice, Advice).



