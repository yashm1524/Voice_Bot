# 🚀 Deployment Guide

Since this project uses a Python backend with a local database and audio files, we will use a **Split Deployment** strategy:

1.  **Backend (FastAPI)** → Deployed on **Render** (Free Web Service)
2.  **Frontend (React)** → Deployed on **Vercel** (Free Static Hosting)

---

## 📦 Phase 1: Deploy Backend to Render

1.  **Push your latest code to GitHub** (we just made changes!).
2.  Go to [dashboard.render.com](https://dashboard.render.com/) and sign up/login.
3.  Click **New +** and select **Web Service**.
4.  Connect your GitHub repository (`Voice_Bot`).
5.  **Configure the service:**
    *   **Name:** `voice-bot-backend`
    *   **Region:** Closest to you (e.g., Singapore, Frankfurt, Ohio)
    *   **Root Directory:** `backend` (Important!)
    *   **Runtime:** Python 3
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`
    *   **Instance Type:** Free
6.  **Environment Variables:**
    *   Click "Advanced" or "Environment" tab.
    *   Add `OPENAI_API_KEY` -> `sk-...` (Your key)
    *   Add `PYTHON_VERSION` -> `3.9.0` (Optional, but good for stability)
7.  Click **Create Web Service**.

**Wait for it to deploy.** Once live, copy the URL (e.g., `https://voice-bot-backend.onrender.com`).
*Note: The free tier spins down after inactivity, so the first request might take 50 seconds.*

---

## 🌐 Phase 2: Deploy Frontend to Vercel

1.  Go to [vercel.com](https://vercel.com/) and sign up/login.
2.  Click **Add New...** -> **Project**.
3.  Import your GitHub repository (`Voice_Bot`).
4.  **Configure the project:**
    *   **Framework Preset:** Vite (should detect automatically)
    *   **Root Directory:** Click "Edit" and select `frontend`.
5.  **Environment Variables:**
    *   Add `VITE_API_URL` -> Paste your Render Backend URL (e.g., `https://voice-bot-backend.onrender.com`)
    *   **Important:** Do NOT add a trailing slash `/` at the end.
6.  Click **Deploy**.

---

## 🎉 Done!

Visit your Vercel URL (e.g., `https://voice-bot.vercel.app`).
It should connect to your Render backend and work perfectly!
