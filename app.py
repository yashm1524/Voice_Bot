from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "Voice Bot running on Render"}

# Just a dummy API endpoint (you can expand later)
@app.route("/bot", methods=["POST"])
def bot():
    text = request.json.get("text", "")
    return {"response": f"You said: {text}"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
