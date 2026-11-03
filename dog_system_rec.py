import pandas as pd

from pyswip import Prolog
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, f1_score

import numpy as np

print("===================================================================")
print(" DOG SYSTEM HYBRID ICON" )
print("==================================================================\n")


print("[1/4] Caricamento del dataset...")
df = pd.read_csv("dataset_dogs_pulito.csv", sep=';')

print("[2/4] Esecuzione inferenza logica con Prolog (Background Knowledge)...")
prolog = Prolog()
prolog.consult("regole.pl")

prolog_results = []
for index, row in df.iterrows():
    breed = row.get('DogBreed', row.iloc[0])
    try:
        query_result = list(prolog.query(f"target('{breed}', Result)"))
        if query_result:
            prolog_results.append(query_result[0]['Result'])
        else:
            prolog_results.append('no')
    except Exception:
        prolog_results.append('no')

df['prolog_target'] = prolog_results

features = ['DogSize', 'DogEnergy']
X_raw = df[features].copy()
y_ml = (df['prolog_target'] == 'yes').astype(int)
X_encoded = pd.get_dummies(X_raw, drop_first=True)

print("[3/4] Valutazione delle performance con K-Fold Cross-Validation (K=5)...")
kf = KFold(n_splits=5, shuffle=True, random_state=42)

accuracies = []
f1_scores = []

for train_index, test_index in kf.split(X_encoded):
    X_train, X_test = X_encoded.iloc[train_index], X_encoded.iloc[test_index]
    y_train, y_test = y_ml.iloc[train_index], y_ml.iloc[test_index]
    
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred = rf_model.predict(X_test)
    
    accuracies.append(accuracy_score(y_test, y_pred))
    f1_scores.append(f1_score(y_test, y_pred, zero_division=0))


print("\n--- RISULTATI DELLA VALUTAZIONE AGGREGATA ---")
print(f"Accuratezza Media: {np.mean(accuracies):.4f} (dev. std: ±{np.std(accuracies):.4f})")
print(f"F1-Score Medio:    {np.mean(f1_scores):.4f} (dev. std: ±{np.std(f1_scores):.4f})")


print("\n[4/4] Generazione dello score ibrido finale...")
final_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
final_model.fit(X_encoded, y_ml)
df['ml_probability'] = final_model.predict_proba(X_encoded)[:, 1]

df['score_finale'] = (0.5 * y_ml) + (0.5 * df['ml_probability'])
df_sorted = df.sort_values(by='score_finale', ascending=False).reset_index(drop=True)

output_file = "dataset_dogs_finale_con_target.csv"
df_sorted.to_csv(output_file, index=False, sep=';')
print(f"Pipeline completata con successo! Salvato come '{output_file}'.")

