# Student Analytics App — README

Student Analytics Dashboard 🎓

A modern and interactive Student Analytics Dashboard built using Streamlit, featuring Google Login Authentication, dynamic filters, performance analytics, and visual insights into student data.

**Date:** May 13, 2025  
**Project:** EduTrack — Student Performance Dashboard

---

## What was built

Two frontend projects were created today based on a student dataset (`student_data.csv`).

---

## Files

| File | Description |
|------|-------------|
| `app.py` | Streamlit version of the app |
| `student_analytics.html` | Standalone HTML version with Chart.js |
| `requirements.txt` | Python dependencies for the Streamlit app |

---

## Dataset

**File:** `student_data.csv`  
**Records:** 30 students  
**Columns:** NAME, AGE, ATTENDANCE, EXAM SCORE, VIDEO GAMES, TUTION, HEALTH, STRESS, DAILY WORK, SELF STUDY

---

## Features

### Login Page
- Clean sign-in screen with a "Continue with Google" button
- No libraries needed — pure HTML/CSS for the HTML version, Streamlit widgets for the Python version
- Clicking the button takes you straight into the dashboard

### Dashboard / Landing Page
- **4 stat cards** — total students, average score, average attendance, average self-study hours
- **Filters** — health, stress level, tuition, performance category, and minimum exam score
- **Charts:**
  - Exam score distribution (bar)
  - Stress level breakdown (doughnut)
  - Attendance vs exam score (scatter)
  - Gaming hours vs average score (bar)
- **Student table** — all fields with color-coded badges for health, stress, and performance

---

## How to run

### HTML version (no setup needed)
Just open `student_analytics.html` in any browser. No server required.

### Streamlit version
```bash
pip install -r requirements.txt
streamlit run app.py
```
Then open `http://localhost:8501` in your browser.

---

## How to set up real Google Sign-In

The current "Continue with Google" button is a UI-only simulation. To make it actually authenticate with Google, follow these steps:

**Step 1 — Go to Google Cloud Console**  
Visit [console.cloud.google.com](https://console.cloud.google.com) and sign in.

**Step 2 — Create a project**  
Click "New Project", give it a name, and hit Create.

**Step 3 — Enable the API**  
Go to `APIs & Services > Library`, search for "Google Identity", and enable it.

**Step 4 — Create OAuth credentials**  
Go to `APIs & Services > Credentials > Create Credentials > OAuth Client ID`.  
Choose "Web application" as the type.  
Add your domain to "Authorised JavaScript origins" (e.g. `http://localhost:8501` for local dev).

**Step 5 — Copy the Client ID**  
You'll get a string that looks like `xxxx.apps.googleusercontent.com`. That's your passkey/client ID.

**Step 6 — Add it to the app**  
For the HTML version, add the Google Identity Services script and pass your client ID:
```html
<script src="https://accounts.google.com/gsi/client" async></script>
<div id="g_id_onload"
  data-client_id="YOUR_CLIENT_ID_HERE"
  data-callback="handleCredentialResponse">
</div>
```

For Streamlit, use the `streamlit-google-auth` package or handle the token via a callback function.

---
