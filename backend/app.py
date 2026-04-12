from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# 🔑 Replace with your NEW API key
client = OpenAI(api_key="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")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",   # fast + cheap
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant like ChatGPT."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )

        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
