from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import datetime

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

# ML Model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# =========================
# IPC INTELLIGENCE ENGINE
# =========================
IPC_RULES = {
    "murder": {
        "sections": ["IPC 302 - Murder"],
        "severity": 3
    },
    "kill": {
        "sections": ["IPC 302 - Murder"],
        "severity": 3
    },
    "theft": {
        "sections": ["IPC 379 - Theft"],
        "severity": 2
    },
    "fraud": {
        "sections": ["IPC 420 - Cheating"],
        "severity": 3
    },
    "cheating": {
        "sections": ["IPC 420 - Cheating"],
        "severity": 3
    },
    "assault": {
        "sections": ["IPC 323 - Hurt"],
        "severity": 2
    },
    "injury": {
        "sections": ["IPC 323 - Hurt"],
        "severity": 2
    },
    "false": {
        "sections": ["IPC 211 - False Charge"],
        "severity": 1
    }
}

# =========================
# CORE AI ENGINE
# =========================
def predict_case(text):
    text_lower = text.lower()

    matched_sections = []
    severity_score = 0

    for key, value in IPC_RULES.items():
        if key in text_lower:
            matched_sections.extend(value["sections"])
            severity_score = max(severity_score, value["severity"])

    matched_sections = list(set(matched_sections))

    # ML Prediction
    vect = vectorizer.transform([text])
    ml_result = model.predict(vect)[0]

    # Verdict logic
    if severity_score == 3:
        verdict = "Guilty Likely ⚖️"
    elif severity_score == 2:
        verdict = "Requires Investigation 🔍"
    elif severity_score == 1:
        verdict = "Weak Case ⚠️"
    else:
        verdict = "No Clear Evidence ❌"

    # Confidence logic (simulated upgrade-ready)
    confidence = min(95, 60 + len(text) % 30 + severity_score * 10)

    return {
        "ipc_sections": matched_sections if matched_sections else ["No IPC Matched"],
        "severity_score": severity_score,
        "ml_prediction": str(ml_result),
        "verdict": verdict,
        "confidence": confidence
    }

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return {
        "status": "AI Legal System Running",
        "version": "1.0",
        "timestamp": str(datetime.datetime.now())
    }

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        text = data.get("message", "")

        if not text:
            return jsonify({"error": "No input provided"}), 400

        result = predict_case(text)

        return jsonify({
            "input": text,
            "prediction": result["ml_prediction"],
            "ipc_sections": result["ipc_sections"],
            "verdict": result["verdict"],
            "confidence": result["confidence"],
            "severity_score": result["severity_score"],
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "failed"
        }), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
