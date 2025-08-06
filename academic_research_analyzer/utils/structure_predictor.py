import joblib
import os
import numpy as np

# Load both models
novelty_model = joblib.load(os.path.join("model", "novelty_model.pkl"))
clarity_model = joblib.load(os.path.join("model", "clarity_model.pkl"))

def predict_scores(features: dict):
    # Order of features must match training order
    input_features = np.array([
        features["num_citations"],
        features["num_figures"],
        features["num_equations"],
        features["total_words"],
        features["avg_sentence_length"]
    ]).reshape(1, -1)

    novelty_score = round(novelty_model.predict(input_features)[0], 2)
    clarity_score = round(clarity_model.predict(input_features)[0], 2)

    return novelty_score, clarity_score

