# 🎯 Simple Setup Guide

## Just 5 Commands to Get Started!

---

## 🔧 Terminal 1: Backend (3 Commands)

```bash
# Command 1: Go to backend folder
cd backend

# Command 2: Activate virtual environment
venv\Scripts\activate

# Command 3: Start the backend server
uvicorn main:app --reload --port 8000
```

✅ **Backend running on:** http://localhost:8000

**Keep this terminal open!**

---

## 🎨 Terminal 2: Frontend (2 Commands)

Open a **NEW** terminal window and run:

```bash
# Command 1: Go to frontend folder
cd frontend

# Command 2: Start the frontend server
npm run dev
```

✅ **Frontend running on:** http://localhost:5173

**Keep this terminal open too!**

---

## 🎉 You're Done!

Open your browser and visit: **http://localhost:5173**

Click the microphone button and start talking to your AI voice bot! 🎤

---

## 💬 Try These Queries

- "What is my account balance?"
- "How do I reset my password?"
- "What are your operating hours?"
- "Hello, how can you help me?"

---

## 🐛 Quick Troubleshooting

### Backend Issues:

**"Module not found"**
```bash
pip install -r requirements.txt
```

**Database error**
```bash
Remove-Item voicebot.db -ErrorAction SilentlyContinue
python seed_db.py
```

### Frontend Issues:

**"npm not found"**
- Install Node.js from https://nodejs.org/

**Dependencies missing**
```bash
npm install
```

**Port already in use**
```bash
npm run dev -- --port 5174
```

---

## 📚 More Information

- **QUICK_START.md** - Detailed setup guide
- **README.md** - Full documentation
- **TTS_CONFIGURATION.md** - Premium TTS setup
- **PROJECT_SUMMARY.md** - Feature overview

---

**That's it! Just 3 + 2 = 5 commands and you're ready to go! 🚀**
