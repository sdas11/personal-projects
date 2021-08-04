testingdata:-dynamic(p_data/2).

age_input(Y):-
    (   p_data(age,Y),! );
    (   write("what is the age of the patient? (0 <= x <= 100)"),nl,
        read(Y),nl,
        assert(p_data(age,Y))
    ).

gender_input(X):-
    (   p_data(gender,X),! );
    (   write("what is the gender of the patient? (male/female)"),nl,
        read(X),nl,
        assert(p_data(gender,X))
    ).

incubationperiod_input(D):-
    (   p_data(incubationperiod,D),! );
    (   write("what is the incub per (0 <= x <= 100)"),nl,
        read(D),nl,
        assert(p_data(incubationperiod,D))
    ).

symptoms_input(Z):-
    (   p_data(symptoms,Z),! );
    (   write("input symptom"),nl,
        read(Z),nl,
        assert(p_data(symptoms,Z))
    ).

preexistingcondition_input(C):-
    (   p_data(preexistingcondition,C),! );
    (   write("input precondition"),nl,
        read(C),nl,
        assert(p_data(preexistingcondition,C))
    ).

% Defining the consultdoctor predicate and its arguments which are serious symptoms.
consultdoctor(chestpain).
consultdoctor(chestpressure).
consultdoctor(loss_of_speech_or_movement).
consultdoctor(breathingproblem).

% Common symptoms predicate and its arguments.
infectionpresent(fever).
infectionpresent(dry_cough).
infectionpresent(tiredness).


% Less common symptoms predicated and its arguments.
infectionpresent(conjunctivitis).
infectionpresent(sorethroat).
infectionpresent(diarrhoea).
infectionpresent(pains).
infectionpresent(headache).
infectionpresent(anosmia).
infectionpresent(runningnose).


% High chance of severe infection predicates and its arguments - precondition
seriousexistingcondition(diabetes).
seriousexistingcondition(hypertension).
seriousexistingcondition(cardiovasculardisease).
seriousexistingcondition(chronicrespiratorydisease).
seriousexistingcondition(cancer).

message_for_age_gdr_prec(Age, Gender, Precondition):-
    Age >=70, write('High chance of severe infection due to old age'), nl;
    Gender = 'male', write('High chance of severe infection due to gender(male)'), nl;
    seriousexistingcondition(Precondition), write('High chance of severe infection'), nl.

message_for_infection(IncubationPeriod, Symptom):-
    IncubationPeriod > 14, write('Low chances of Virus'), nl;
    infectionpresent(Symptom), not(consultdoctor(Symptom)), write('this is a symptom of new virus. stay at home'), nl;
    consultdoctor(Symptom), write('See a doctor'), nl.

checkAll(Message):-
    age_input(Age),
    gender_input(Gender),
    incubationperiod_input(IncubationPeriod),
    symptoms_input(Symptom),
    preexistingcondition_input(Precondition),
    message_for_age_gdr_prec(Age, Gender, Precondition),
    message_for_infection(IncubationPeriod, Symptom),
    Message = 'done'.

retractal.