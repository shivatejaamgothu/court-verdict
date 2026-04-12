from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)

# CORS for frontend (Vercel/localhost)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load ML models
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# IPC mapping (expandable)
IPC_MAP = {
    "murder accused killed victim": ["IPC 302 - Murder"],
    "planned murder with weapon": ["IPC 302 - Murder", "IPC 120B - Criminal Conspiracy"],
    "theft of mobile phone": ["IPC 379 - Theft"],
    "fraud bank cheating case": ["IPC 420 - Cheating"],
    "assault caused injury": ["IPC 323 - Voluntarily causing hurt"],
    "no evidence available": ["No IPC - Insufficient Evidence"],
    "false accusation": ["IPC 211 - False charge"],
    "insufficient proof": ["No IPC - Case weak / dismissed"]
}

@app.route("/")
def home():
    return "⚖️ IPC Prediction API Running"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        text = data.get("message", "")

        if not text:
            return jsonify({"error": "No input text provided"}), 400

        # ML prediction (fallback label)
        vect = vectorizer.transform([text])
        prediction = model.predict(vect)[0]

        # Try dictionary match first
        ipc_sections = None
        for key in IPC_MAP:
            if key in text.lower():
                ipc_sections = IPC_MAP[key]
                break

        # fallback if no match
        if not ipc_sections:
            ipc_sections = [f"IPC Predicted Label: {prediction}"]

        # Confidence simulation (you can improve later)
        confidence = int(min(95, 60 + len(text) % 35))

        return jsonify({
            "input": text,
            "prediction": str(prediction),
            "ipc_sections": ipc_sections,
            "confidence": confidence,
            "verdict": "guilty" if "murder" in text or "theft" in text else "needs_review"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
