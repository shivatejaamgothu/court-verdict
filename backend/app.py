from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

# Load model and vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# 🧠 AI-like smart logic
def smart_logic(text, ml_prediction):
    text = text.lower()
    ipc = [ml_prediction]
    reasoning = []
    punishment = "Based on IPC sections"
    recommendation = "Consult a legal expert"

    if "murder" in text or "killed" in text or "death" in text:
        ipc.append("IPC 302")
        reasoning.append("Detected intent to kill (murder-related keywords)")
        punishment = "Life imprisonment or death penalty"

    if "knife" in text or "weapon" in text or "attack" in text:
        ipc.append("IPC 324")
        reasoning.append("Use of weapon or violent attack detected")

    if "theft" in text or "stolen" in text or "robbery" in text:
        ipc.append("IPC 379")
        reasoning.append("Theft or robbery-related keywords found")
        punishment = "Up to 3 years imprisonment"

    if "fraud" in text or "cheating" in text or "scam" in text:
        ipc.append("IPC 420")
        reasoning.append("Financial fraud or cheating detected")
        punishment = "Up to 7 years imprisonment"

    if "threat" in text or "intimidation" in text:
        ipc.append("IPC 506")
        reasoning.append("Criminal intimidation detected")

    # Remove duplicates
    ipc = list(set(ipc))

    return ipc, punishment, recommendation, reasoning


# 🚀 Prediction API
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if text.strip() == "":
            return jsonify({"error": "Empty input"}), 400

        # 🔹 Convert text → vector
        text_vec = vectorizer.transform([text])

        # 🔹 ML prediction
        prediction = model.predict(text_vec)[0]
        probs = model.predict_proba(text_vec)[0]

        confidence = round(max(probs) * 100, 2)

        # 🔹 Top 3 predictions (AI-like)
        top_indices = np.argsort(probs)[-3:]
        top_ipc = [model.classes_[i] for i in top_indices]

        # 🔹 Smart reasoning logic
        ipc, punishment, recommendation, reasoning = smart_logic(text, prediction)

        # Merge ML + rule-based
        ipc = list(set(ipc + top_ipc))

        return jsonify({
            "verdict": "Predicted",
            "ipc": ipc,
            "top_predictions": top_ipc,
            "punishment": punishment,
            "recommendation": recommendation,
            "reasoning": reasoning,
            "confidence": confidence
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run server
if __name__ == "__main__":
    app.run(debug=True)
