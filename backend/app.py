from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# ML model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# OpenAI client (SAFE METHOD)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "⚖️ Legal AI Chatbot Running 🚀"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # 1️⃣ ML Prediction
        vect = vectorizer.transform([user_message])
        prediction = model.predict(vect)[0]

        # 2️⃣ ChatGPT explanation using OpenAI
        ai_response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a legal AI assistant. Explain clearly in simple words."},
                {"role": "user", "content": f"Case: {user_message}. Prediction: {prediction}. Explain this legally."}
            ]
        )

        explanation = ai_response.choices[0].message.content

        return jsonify({
            "prediction": str(prediction),
            "explanation": explanation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
