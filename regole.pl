% Categorie di taglia estese
compact_size(piccolo).
compact_size(medio).
heavy_size(grande).

manageable_energy(basso).
manageable_energy(medio).
excessive_energy(intenso).
excessive_energy(alto).

% Regola relazionale per l'ereditarietà delle proprietà comportamentali
has_behavior(Breed, Trait) :- comp_1(Breed, Trait).
has_behavior(Breed, Trait) :- comp_2(Breed, Trait).
has_behavior(Breed, Trait) :- comp_3(Breed, Trait).

% Regola plus: Un cane è "gestibile" se la sua taglia è compatibile e l'energia è gestibile
manageable_profile(Breed) :-
    dog_size(Breed, Size),
    compact_size(Size),
    dog_energy(Breed, Energy),
    manageable_energy(Energy).

% =====================================================================
% REGOLA 1,2,3,4  target(Breed, Result)
% =====================================================================

% Regola 1: Sfrutta la tassonomia astratta "manageable_profile"
target(Breed, yes) :-
    manageable_profile(Breed).

% Regola 2: I cani di media taglia con comportamento calmo ed energia non eccessiva
target(Breed, yes) :-
    dog_size(Breed, medio),
    has_behavior(Breed, calmo),
    dog_energy(Breed, Energy),
    \+ excessive_energy(Energy).

% Regola 3: Cani socievoli e giocherelloni a bassa energia
target(Breed, yes) :-
    dog_size(Breed, medio),
    has_behavior(Breed, socievole),
    has_behavior(Breed, giocherellone),
    dog_energy(Breed, basso).

% Regola 4: Cani di grande taglia ammessi SOLO con profili di calma assoluta
target(Breed, yes) :-
    dog_size(Breed, grande),
    has_behavior(Breed, calmo),
    dog_energy(Breed, basso),
    \+ has_behavior(Breed, attivo).

% =====================================================================
% REGOLE DI ESCLUSIONE
% =====================================================================

target(Breed, no) :-
    dog_energy(Breed, Energy),
    excessive_energy(Energy).

target(Breed, no) :-
    dog_size(Breed, grande),
    (has_behavior(Breed, attivo) ; has_behavior(Breed, protettivo)).

target(Breed, no) :-
    has_behavior(Breed, diffidente),
    dog_energy(Breed, alto).

% Fallback basato sulla Negazione come Fallimento (Negation as Failure)
target(Breed, no) :-
    \+ target(Breed, yes).
