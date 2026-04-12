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
# LEGAL KNOWLEDGE GRAPH
# =========================
LEGAL_KG = {
    "murder": {"ipc": ["IPC 302"], "severity": 3},
    "kill": {"ipc": ["IPC 302"], "severity": 3},
    "theft": {"ipc": ["IPC 379"], "severity": 2},
    "fraud": {"ipc": ["IPC 420"], "severity": 3},
    "cheating": {"ipc": ["IPC 420"], "severity": 3},
    "assault": {"ipc": ["IPC 323"], "severity": 2},
    "injury": {"ipc": ["IPC 323"], "severity": 2},
    "threat": {"ipc": ["IPC 506"], "severity": 2},
    "false": {"ipc": ["IPC 211"], "severity": 1}
}

# =========================
# AI DECISION ENGINE
# =========================
def ai_engine(text):
    text = text.lower()

    matched_ipc = []
    severity = 0

    # Rule-based extraction
    for key, value in LEGAL_KG.items():
        if key in text:
            matched_ipc += value["ipc"]
            severity = max(severity, value["severity"])

    matched_ipc = list(set(matched_ipc))

    # ML Prediction
    vect = vectorizer.transform([text])
    ml_prediction = model.predict(vect)[0]

    # Confidence model (advanced simulation)
    confidence = min(97, 65 + len(text) % 20 + severity * 10)

    # Verdict engine
    if severity == 3:
        verdict = "GUILTY (High Probability)"
    elif severity == 2:
        verdict = "UNDER INVESTIGATION"
    elif severity == 1:
        verdict = "LOW EVIDENCE CASE"
    else:
        verdict = "NO CRIMINAL INTENT FOUND"

    return {
        "ipc_sections": matched_ipc if matched_ipc else ["No IPC Detected"],
        "ml_prediction": str(ml_prediction),
        "severity": severity,
        "confidence": confidence,
        "verdict": verdict
    }

# =========================
# API ENDPOINTS
# =========================

@app.route("/")
def home():
    return {
        "system": "National Legal AI System",
        "status": "Active",
        "version": "2.0"
    }

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        text = data.get("message", "")

        if not text:
            return jsonify({"error": "Empty input"}), 400

        result = ai_engine(text)

        return jsonify({
            "input": text,
            "prediction": result["ml_prediction"],
            "ipc_sections": result["ipc_sections"],
            "severity": result["severity"],
            "confidence": result["confidence"],
            "verdict": result["verdict"],
            "timestamp": str(datetime.datetime.now()),
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
