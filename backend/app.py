from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
CORS(app)

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ✅ CLEAN TEXT (VERY IMPORTANT)
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)

    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))

    words = [w for w in words if w not in stop_words]

    return " ".join(words)

# ✅ STRONG SMART LOGIC
def smart_logic(text):
    text = text.lower()
    ipc = []
    reasoning = []
    punishment_map = {}

    rules = [
        ("IPC 302", ["murder", "killed", "death", "stabbed", "shot"], 
         "Life imprisonment or death penalty"),

        ("IPC 379", ["theft", "stolen", "robbery", "snatched"], 
         "Up to 3 years imprisonment"),

        ("IPC 420", ["fraud", "cheating", "scam", "online fraud"], 
         "Up to 7 years imprisonment"),

        ("IPC 376", ["rape", "sexual assault"], 
         "Minimum 10 years imprisonment"),

        ("IPC 324", ["knife", "weapon", "attack", "injured"], 
         "Up to 3 years imprisonment"),

        ("IPC 506", ["threat", "intimidation"], 
         "Criminal intimidation punishment"),
    ]

    for code, keywords, punishment in rules:
        for word in keywords:
            if word in text:
                ipc.append(code)
                reasoning.append(f"{code} triggered due to keyword: {word}")
                punishment_map[code] = punishment
                break

    return ipc, reasoning, punishment_map

# 🚀 API
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text.strip():
            return jsonify({"error": "Empty input"}), 400

        # ✅ Clean text BEFORE ML
        cleaned = clean_text(text)

        # ✅ ML Prediction
        vec = vectorizer.transform([cleaned])
        probs = model.predict_proba(vec)[0]

        classes = model.classes_

        # 🔥 TAKE ONLY STRONG PREDICTIONS (>20%)
        ipc_ml = []
        for i, prob in enumerate(probs):
            if prob > 0.2:
                ipc_ml.append(classes[i])

        # 🔥 If nothing strong → take top 2
        if not ipc_ml:
            top_indices = probs.argsort()[-2:][::-1]
            ipc_ml = [classes[i] for i in top_indices]

        # ✅ Smart logic
        ipc_rule, reasoning, punishment_map = smart_logic(text)

        # ✅ Merge both
        final_ipc = list(set(ipc_ml + ipc_rule))

        # ✅ Confidence (average of selected IPCs)
        confidence = round(float(np.max(probs)) * 100, 2)

        return jsonify({
            "verdict": "Predicted",
            "ipc": final_ipc,
            "ml_ipc": ipc_ml,
            "rule_ipc": ipc_rule,
            "confidence": confidence,
            "reasoning": reasoning,
            "punishments": punishment_map,
            "recommendation": "Consult legal expert for confirmation"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
