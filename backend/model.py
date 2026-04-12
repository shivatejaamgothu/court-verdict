from openai import OpenAI

# Initialize client (API key will come from environment variable)
client = OpenAI()

def get_ai_response(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
        from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("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"))
