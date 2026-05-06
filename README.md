# 🎧 Sentiment Analysis Web App

## 🔍 Overview

A Flask-based web application that analyzes the sentiment of audio input. Users can upload audio files or record live speech, which is converted into text and classified as positive or negative.

---

## ⚙️ Features

* 🔐 User Authentication (Login/Signup)
* 🎤 Live Audio Recording (Browser-based)
* 📁 Audio File Upload
* 🧠 Speech-to-Text using Whisper
* 💬 Sentiment Analysis using pre-trained model
* 🗂️ User-specific History Tracking

---

## 🧩 Tech Stack

* **Backend:** Flask (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Models:** Whisper + HuggingFace Transformers
* **Database:** MongoDB

---

## 🔄 Application Flow

1. User logs in
2. Uploads or records audio
3. Audio sent to `/analyze` (POST request)
4. Backend:

   * Converts speech → text
   * Performs sentiment analysis
   * Stores result in database
5. Results displayed on dashboard
6. History available via `/history`

---

## 🧠 Key Concepts Used

* Flask Routing (`/dashboard`, `/analyze`, `/history`)
* Form Handling & `request.files`
* JavaScript Fetch API (for live recording)
* Jinja Templating (`{{ }}`, `{% %}`)
* MongoDB operations (`insert_one`, `find`)

---

## ▶️ Run Locally

```bash id="k8as2m"
pip install -r requirements.txt
python app.py
```

---

## 📌 Notes

* Uses pre-trained models (no custom training)
* Live recording handled via MediaRecorder API
* Same backend route (`/analyze`) handles both upload and recording

---
