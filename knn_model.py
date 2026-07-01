import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("Training Dataset")

# Separate symptoms and diseases
x = df.drop("prognosis", axis=1)
y = df["prognosis"]

# Convert to numpy arrays
X = x.values
Y = y.values

# Symptom names
symptoms = df.columns[:-1]


# Euclidean distance function
def distance(a, b):

    return np.sqrt(
        np.sum((a - b) ** 2)
    )


# KNN prediction function
def predict_disease(selected_symptoms, k=15):

    # Empty patient vector
    new_patient = np.zeros(len(symptoms))

    # Convert symptoms into vector
    for symptom in selected_symptoms:

        if symptom in symptoms:

            index = symptoms.get_loc(symptom)

            new_patient[index] = 1

    # Calculate distances
    distances = []

    for i in range(len(X)):

        d = distance(X[i], new_patient)

        distances.append((d, Y[i]))

    # Sort nearest first
    distances.sort(key=lambda x: x[0])

    # Take nearest neighbors
    neighbors = distances[:k]
    print(neighbors)

    # Get labels
    labels = [label for _, label in neighbors]
    print(labels)

    # Count votes
    unique_labels = set(labels)

    results = []

    for disease in unique_labels:

        count = labels.count(disease)

        probability = (count / k) * 100

        results.append(
            (disease, round(probability, 2))
        )

    # Sort highest probability first
    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # Return top 4 diseases
    return results[:4]

