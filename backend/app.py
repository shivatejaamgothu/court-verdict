from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os

app = Flask(__name__)
CORS(app)

# Load model + vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorize.pkl", "rb"))

@app.route("/")
def home():
    return "ML Backend Running 🚀"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    text = data.get("text")

    if not text:
        return jsonify({"error": "No input text"}), 400

    try:
        vect = vectorizer.transform([text])
        prediction = model.predict(vect)[0]

        return jsonify({"prediction": str(prediction)})

    except Exception as e:
        return jsonify({"error": str(e)})

# IMPORTANT for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
