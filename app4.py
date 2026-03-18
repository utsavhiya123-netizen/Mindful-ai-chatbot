from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Replace this with your real Together.ai API key (no card required)
TOGETHER_API_KEY = "f801a7782cfc4c90f55a94ff5eeecd543cbbfbee808de333f8b81bdd33166d34"

@app.route("/")
def index():
    return "AI Chat Backend is running. POST to /chat with your message."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")

    try:
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "messages": [{"role": "user", "content": user_message}],
                "temperature": 0.7
            }
        )
        res_json = response.json()
        print("Response JSON:", res_json)

        if "choices" in res_json:
            ai_message = res_json["choices"][0]["message"]["content"]
        else:
            ai_message = res_json.get("error", {}).get("message", "Sorry, I couldn't get a response.")

    except Exception as e:
        print("Exception:", e)
        ai_message = f"Backend error: {str(e)}"

    return jsonify({"reply": ai_message})

if __name__ == "__main__":
    app.run(debug=True)
