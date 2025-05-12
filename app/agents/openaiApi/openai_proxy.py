from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
client = OpenAI(api_key="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")

app = Flask(__name__)

@app.route("/openai-chat", methods=["POST"])
def proxy_chat():
    try:
        body = request.get_json()
        messages = body.get("messages", [])
        model = body.get("model", "gpt-4")
        temperature = body.get("temperature", 0.7)

        # Call OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )

        # Return raw response as dict
        return jsonify(response.dict())

    except Exception as e:
        print("❌ OpenAI call failed:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
