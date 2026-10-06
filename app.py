from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Please add it to your .env file."
    )

client = Groq(api_key=api_key)

SYSTEM_PROMPT = """
You are an expert Python developer.

Convert the user's natural-language request into clean,
beginner-friendly Python code.

Requirements:
- Return only Python code.
- Do not use Markdown code fences.
- Use clear variable and function names.
- Add helpful comments.
- Make the code executable.
- Keep the solution simple and understandable.
"""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}

    user_request = (data.get("request") or "").strip()

    if not user_request:
        return jsonify({
            "error": "Please enter a request."
        }), 400

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_request
                }
            ],
            include_reasoning=False
        )

        code = completion.choices[0].message.content or ""

        return jsonify({
            "code": code
        })

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
