import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("Training Dataset")

# Separate symptoms and disease labels
X = df.drop("prognosis", axis=1)
y = df["prognosis"]

# Train model
model = RandomForestClassifier()
model.fit(X, y)

serious_rules = {

    "AIDS": [
        "weight_loss",
        "extra_marital_contacts",
        "receiving_blood_transfusion",
        "muscle_wasting"
    ],

    "Hepatitis B": [
        "yellowish_skin",
        "yellowing_of_eyes",
        "dark_urine",
        "acute_liver_failure"
    ],

    "Hepatitis C": [
        "yellowish_skin",
        "dark_urine",
        "receiving_blood_transfusion"
    ],

    "Hepatitis D": [
        "yellowish_skin",
        "dark_urine",
        "abdominal_pain"
    ],

    "Hepatitis E": [
        "yellowish_skin",
        "dark_urine",
        "vomiting"
    ],

    "Alcoholic hepatitis": [
        "history_of_alcohol_consumption",
        "yellowish_skin",
        "abdominal_pain"
    ],

    "Tuberculosis": [
        "blood_in_sputum",
        "weight_loss",
        "chest_pain"
    ],

    "Heart attack": [
        "chest_pain",
        "fast_heart_rate",
        "sweating",
        "breathlessness"
    ],

    "Paralysis (brain hemorrhage)": [
        "weakness_of_one_body_side",
        "slurred_speech",
        "loss_of_balance"
    ]
}

def predict_disease(selected_symptoms):

    # Create empty symptom vector
    input_vector = [0] * len(X.columns)

    # Fill vector based on selected symptoms
    for symptom in selected_symptoms:

        if symptom in X.columns:

            index = X.columns.get_loc(symptom)

            input_vector[index] = 1

    # Convert to dataframe
    input_df = pd.DataFrame(
        [input_vector],
        columns=X.columns
    )

    # Predict probabilities
    probabilities = model.predict_proba(input_df)[0]

    # Disease names
    diseases = model.classes_

    # Combine disease names with probabilities
    results = list(zip(diseases, probabilities))

    # Sort highest probability first
    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # Take top 4 predictions
    top_results = results[:4]

    filtered_results = []

    for disease, prob in top_results:

        # If disease has rules
        if disease in serious_rules:

            required_symptoms = serious_rules[disease]

            # Check if ANY required symptom selected
            valid = False

            for symptom in required_symptoms:

                if symptom in selected_symptoms:

                    valid = True
                    break

            # Skip disease if no strong symptom found
            if not valid:
                continue

        filtered_results.append((disease, prob))

    # Convert probabilities to percentages
    formatted_results = []

    for disease, prob in filtered_results:

        formatted_results.append(
            (
                disease,
                round(prob * 100, 2)
            )
        )

    return formatted_results