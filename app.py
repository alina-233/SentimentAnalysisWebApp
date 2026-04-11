from flask import Flask, render_template, request, redirect, session
import whisper
from transformers import pipeline
import os
from auth import register_user, login_user
from db import history_collection

app = Flask(__name__)
app.secret_key = "secret123"

# models
model = whisper.load_model("base")
sentiment_model = pipeline("sentiment-analysis")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------- AUTH ROUTES ----------

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


# ---------- MAIN APP ----------

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
    sentiment = sentiment_model(transcription)

    # save to DB
    history_collection.insert_one({
        "username": session["user"],
        "text": transcription,
        "sentiment": sentiment[0]["label"]
    })

    return render_template(
        "dashboard.html",
        transcription=transcription,
        sentiment=sentiment
    )


@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/")

    data = history_collection.find({"username": session["user"]})
    return render_template("history.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)