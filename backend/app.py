from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import datetime
import os

app = Flask(__name__)

# ✅ FIX CORS COMPLETELY
CORS(app)

# =========================
# LOAD MODEL SAFELY
# =========================
model = None
vectorizer = None

try:
    model = pickle.load(open("model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
except:
    print("⚠️ ML model not loaded, using rule-based only")

# =========================
# LEGAL RULES
# =========================
LEGAL_RULES = {
    "murder": "IPC 302",
    "kill": "IPC 302",
    "theft": "IPC 379",
    "stolen": "IPC 379",
    "fraud": "IPC 420",
    "cheating": "IPC 420",
    "assault": "IPC 323",
    "injury": "IPC 323",
    "threat": "IPC 506",
    "intimidation": "IPC 506",
    "false": "IPC 211",
    "conspiracy": "IPC 120B",
    "group": "IPC 34"
}

PUNISHMENT_MAP = {
    "IPC 302": "Life Imprisonment / Death Penalty",
    "IPC 379": "Up to 3 years imprisonment + fine",
    "IPC 420": "Up to 7 years imprisonment + fine",
    "IPC 323": "Up to 1 year imprisonment or fine",
    "IPC 506": "Up to 7 years imprisonment",
    "IPC 211": "Up to 2 years imprisonment + fine",
    "IPC 120B": "Criminal conspiracy punishment applicable",
    "IPC 34": "Common intention clause applied"
}

# =========================
# IPC ENGINE
# =========================
def extract_ipc(text):
    text = text.lower()
    ipc_set = set()

    for k, v in LEGAL_RULES.items():
        if k in text:
            ipc_set.add(v)

    if model and vectorizer:
        try:
            vect = vectorizer.transform([text])
            pred = model.predict(vect)[0]

            if isinstance(pred, list):
                for p in pred:
                    ipc_set.add(str(p))
            else:
                ipc_set.add(str(pred))
        except:
            pass

    return list(ipc_set)

def get_punishment(ipc_list):
    return " | ".join([PUNISHMENT_MAP.get(i, "Not defined") for i in ipc_list]) if ipc_list else "No punishment found"

def get_verdict(ipc_list):
    if not ipc_list:
        return "NOT CLEAR"
    if "IPC 302" in ipc_list:
        return "GUILTY (SEVERE)"
    if len(ipc_list) > 1:
        return "GUILTY (MULTIPLE CHARGES)"
    return "GUILTY"

def get_confidence(ipc_list):
    return min(95, 60 + len(ipc_list) * 10)

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return jsonify({"status": "OK", "time": str(datetime.datetime.now())})

# =========================
# 🔥 MAIN ENDPOINT (IMPORTANT FOR FRONTEND)
# =========================
@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json()
    text = data.get("text", "")

    ipc_list = extract_ipc(text)
    result = {
        "ipc": ipc_list,
        "punishment": get_punishment(ipc_list),
        "verdict": get_verdict(ipc_list),
        "confidence": get_confidence(ipc_list),
        "timestamp": str(datetime.datetime.now())
    }

    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
