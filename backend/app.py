from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import random

app = Flask(__name__)
CORS(app)

model = pickle.load(open("model.pkl","rb"))
vectorizer = pickle.load(open("vectorizer.pkl","rb"))

def predict_ipc(text):
    text = text.lower()
    ipc = []
    punishment = ""
    recommendation = ""

    if "murder" in text:
        ipc += ["IPC 302 - Murder", "IPC 34 - Common Intention"]
        punishment = "Life imprisonment or death penalty"
        recommendation = "Strong criminal defense required"

    if "theft" in text:
        ipc += ["IPC 379 - Theft"]
        punishment = "Up to 3 years imprisonment"
        recommendation = "Check intent and evidence"

    if "fraud" in text:
        ipc += ["IPC 420 - Cheating"]
        punishment = "Up to 7 years imprisonment"
        recommendation = "Financial records required"

    if not ipc:
        ipc = ["No clear IPC found"]
        punishment = "Unknown"
        recommendation = "Provide more details"

    return ipc, punishment, recommendation

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text")

    # fallback values
    ipc = ["392", "506"]
    punishment = "3 years imprisonment"

    verdict = "Guilty"
    recommendation = "Strict punishment recommended"
    confidence = 85

    return jsonify({
        "verdict": verdict,
        "ipc": ipc,
        "punishment": punishment,
        "recommendation": recommendation,
        "confidence": confidence
    })

if __name__ == "__main__":
    app.run(debug=True)
    
