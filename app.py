from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():

    data = request.get_json()

    text = data["text"]

    prompt = f"""
You are an expert in Manipuri (Meiteilon).

Convert the following Romanized Manipuri text into Meitei Mayek.

Rules:
- Convert ONLY from Romanized Manipuri to Meitei Mayek.
- Do NOT translate the meaning.
- Preserve the pronunciation.
- Return ONLY the Meitei Mayek text.
- Do not add explanations.

Romanized Manipuri:
{text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return jsonify({
        "translation": response.text
    })


if __name__ == "__main__":
    app.run(debug=True)