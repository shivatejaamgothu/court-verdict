from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)

# Allow frontend (Vercel / localhost)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load ML model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# =========================
# IPC KNOWLEDGE BASE
# =========================
IPC_DATABASE = {
    "murder": {
        "sections": ["IPC 302 - Murder"],
        "severity": "High"
    },
    "kill": {
        "sections": ["IPC 302 - Murder"],
        "severity": "High"
    },
    "theft": {
        "sections": ["IPC 379 - Theft"],
        "severity": "Medium"
    },
    "mobile": {
        "sections": ["IPC 379 - Theft"],
        "severity": "Medium"
    },
    "fraud": {
        "sections": ["IPC 420 - Cheating"],
        "severity": "High"
    },
    "cheating": {
        "sections": ["IPC 420 - Cheating"],
        "severity": "High"
    },
    "assault": {
        "sections": ["IPC 323 - Voluntarily Causing Hurt"],
        "severity": "Medium"
    },
    "injury": {
        "sections": ["IPC 323 - Voluntarily Causing Hurt"],
        "severity": "Medium"
    },
    "false": {
        "sections": ["IPC 211 - False Charge"],
        "severity": "Low"
    }
}

# =========================
# HELPER FUNCTION
# =========================
def analyze_case(text):
    text = text.lower()

    matched_sections = []
    severity_levels = []

    for key, value in IPC_DATABASE.items():
        if key in text:
            matched_sections.extend(value["sections"])
            severity_levels.append(value["severity"])

    # Remove duplicates
    matched_sections = list(set(matched_sections))

    # Determine severity
    if "High" in severity_levels:
        severity = "High"
    elif "Medium" in severity_levels:
        severity = "Medium"
    else:
        severity = "Low"

    # ML fallback prediction
    vect = vectorizer.transform([text])
    ml_prediction = model.predict(vect)[0]

    # Verdict logic
    if severity == "High":
        verdict = "Guilty Likely"
    elif severity == "Medium":
        verdict = "Needs Investigation"
    else:
        verdict = "Not Guilty Likely"

    return {
        "ipc_sections": matched_sections if matched_sections else ["No IPC matched"],
        "severity": severity,
        "ml_prediction": str(ml_prediction),
        "verdict": verdict
    }

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return "⚖️ Final Year Legal AI System Running"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        text = data.get("message", "")

        if not text:
            return jsonify({"error": "No input provided"}), 400

        result = analyze_case(text)

        return jsonify({
            "input": text,
            "prediction": result["ml_prediction"],
            "ipc_sections": result["ipc_sections"],
            "severity": result["severity"],
            "verdict": result["verdict"],
            "confidence": 85  # static for now (can upgrade later)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
