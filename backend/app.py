from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import datetime

app = Flask(__name__)
CORS(app)

# Load ML model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

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
    "false": "IPC 211"
}

PUNISHMENT_MAP = {
    "IPC 302": "Life Imprisonment / Death Penalty",
    "IPC 379": "Up to 3 years imprisonment + fine",
    "IPC 420": "Up to 7 years imprisonment + fine",
    "IPC 323": "Up to 1 year imprisonment or fine",
    "IPC 506": "Up to 2–7 years imprisonment",
    "IPC 211": "Up to 2 years imprisonment + fine",
    "IPC 34": "Common intention clause (added in group crimes)",
    "IPC 120B": "Criminal conspiracy punishment applicable"
}

# =========================
# MULTI IPC ENGINE
# =========================
def extract_ipc(text):
    text = text.lower()
    ipc_set = set()

    for keyword, ipc in LEGAL_RULES.items():
        if keyword in text:
            ipc_set.add(ipc)

    # ML prediction also added
    vect = vectorizer.transform([text])
    ml_pred = model.predict(vect)[0]

    if isinstance(ml_pred, list):
        for p in ml_pred:
            ipc_set.add(p)
    else:
        ipc_set.add(str(ml_pred))

    return list(ipc_set)

# =========================
# PUNISHMENT ENGINE
# =========================
def get_punishment(ipc_list):
    punishments = []

    for ipc in ipc_list:
        if ipc in PUNISHMENT_MAP:
            punishments.append(PUNISHMENT_MAP[ipc])

    if not punishments:
        return "No specific punishment found"

    return " | ".join(set(punishments))

# =========================
# API
# =========================
@app.route("/")
def home():
    return {"status": "Legal AI Running", "version": "3.0"}

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        text = data.get("message", "")

        if not text:
            return jsonify({"error": "Empty input"}), 400

        ipc_list = extract_ipc(text)
        punishment = get_punishment(ipc_list)

        confidence = min(95, 60 + len(ipc_list) * 10)

        verdict = "GUILTY" if len(ipc_list) > 0 else "NOT CLEAR"

        return jsonify({
            "input": text,
            "ipc_sections": ipc_list,
            "punishment": punishment,
            "verdict": verdict,
            "confidence": confidence,
            "timestamp": str(datetime.datetime.now())
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
