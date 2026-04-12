from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import datetime
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# =========================
# LOAD MODEL SAFELY
# =========================
model = None
vectorizer = None

try:
    model = pickle.load(open("model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
except:
    print("⚠️ ML model not loaded, running rule-based only")

# =========================
# LEGAL KNOWLEDGE BASE
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
    "IPC 506": "Up to 2–7 years imprisonment",
    "IPC 211": "Up to 2 years imprisonment + fine",
    "IPC 34": "Common intention clause applied",
    "IPC 120B": "Criminal conspiracy punishment applicable"
}

# =========================
# IPC EXTRACTION ENGINE
# =========================
def extract_ipc(text):
    text = text.lower()
    ipc_set = set()

    # Rule-based extraction
    for keyword, ipc in LEGAL_RULES.items():
        if keyword in text:
            ipc_set.add(ipc)

    # ML prediction (safe handling)
    if model and vectorizer:
        try:
            vect = vectorizer.transform([text])
            ml_pred = model.predict(vect)[0]

            if isinstance(ml_pred, list):
                for p in ml_pred:
                    ipc_set.add(str(p))
            else:
                ipc_set.add(str(ml_pred))
        except:
            pass

    return list(ipc_set)

# =========================
# PUNISHMENT ENGINE
# =========================
def get_punishment(ipc_list):
    punishments = []

    for ipc in ipc_list:
        if ipc in PUNISHMENT_MAP:
            punishments.append(PUNISHMENT_MAP[ipc])

    if len(punishments) == 0:
        return "No specific punishment found"

    return " | ".join(list(set(punishments)))

# =========================
# VERDICT ENGINE (IMPROVED)
# =========================
def get_verdict(ipc_list):
    if len(ipc_list) == 0:
        return "NOT CLEAR"
    elif "IPC 302" in ipc_list:
        return "GUILTY (SEVERE)"
    elif len(ipc_list) >= 2:
        return "GUILTY (MULTIPLE CHARGES)"
    else:
        return "GUILTY"

# =========================
# CONFIDENCE ENGINE
# =========================
def get_confidence(ipc_list):
    base = 60
    boost = len(ipc_list) * 12
    return min(95, base + boost)

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return jsonify({
        "status": "Legal AI Running",
        "version": "3.1",
        "time": str(datetime.datetime.now())
    })

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        print("REQUEST RECEIVED:", data)
        @app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        print("REQUEST RECEIVED:", data)

        text = data.get("message", "")

        if not text:
            return jsonify({"error": "Empty input"}), 400

        ipc_list = extract_ipc(text)
        punishment = get_punishment(ipc_list)
        verdict = get_verdict(ipc_list)
        confidence = get_confidence(ipc_list)

        return jsonify({
            "ipc_sections": ipc_list,
            "punishment": punishment,
            "verdict": verdict,
            "confidence": confidence
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
        
        

        if not text:
            return jsonify({"error": "Empty input"}), 400

        ipc_list = extract_ipc(text)
        punishment = get_punishment(ipc_list)
        verdict = get_verdict(ipc_list)
        confidence = get_confidence(ipc_list)

        return jsonify({
            "input": text,
            "ipc_sections": ipc_list,   # ✅ matches frontend
            "punishment": punishment,   # ✅ matches frontend
            "verdict": verdict,         # ✅ matches frontend
            "confidence": confidence,   # ✅ matches frontend
            "timestamp": str(datetime.datetime.now())
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "ipc_sections": [],
            "punishment": "Error",
            "verdict": "ERROR",
            "confidence": 0
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
