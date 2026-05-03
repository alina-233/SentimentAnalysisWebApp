from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session
import whisper
from transformers import pipeline
import os
from auth import register_user, login_user
from db import history_collection

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key")
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="None"
)

# models
model = whisper.load_model("base")
sentiment_model = pipeline("sentiment-analysis")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# AUTH ROUTES

@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # NO SPACES CHECK
        if " " in username:
            return "Username should not contain spaces"

        # PASSWORD STRENGTH CHECK
        import re
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$', password):
            return "Weak password"

        # EXISTING LOGIC
        if register_user(username, password):
            return redirect("/")
        else:
            return "User already exists"

    return render_template("signup.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = login_user(username, password)

    if user:
        session["user"] = username
        return redirect("/dashboard")
    
    # return "Invalid credentials"
    return render_template("login.html", error="Invalid credentials")
 


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# MAIN APP

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "user" not in session:
        return redirect("/")

    audio_file = request.files["audio"]

    filepath = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    audio_file.save(filepath)

    # speech to text
    result = model.transcribe(filepath)
    transcription = result["text"]

    # sentiment
    result = sentiment_model(transcription)[0]
    label = result["label"]
    score = round(result["score"] * 100, 2)

    # save to DB
    history_collection.insert_one({
        "username": session["user"],
        "text": transcription,
        "sentiment": label
    })

    return render_template(
        "dashboard.html",
        transcription=transcription,
        sentiment=label,
        score=score
    )


@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/")

    data = list(history_collection.find({"username": session["user"]}))
    return render_template("history.html", data=data)


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=7860)