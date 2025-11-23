# 🚀 Quick Start Guide

## Get Your Voice Bot Running in 5 Minutes!

---

## 🔧 Backend Setup (3 Commands)

Open a terminal and run these commands:

```bash
# 1. Navigate to backend directory
cd backend

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Start the backend server
uvicorn main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

✅ **Backend is now running!** Keep this terminal open.

---

## 🎨 Frontend Setup (2 Commands)

Open a **new terminal** and run these commands:

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Start the frontend development server
npm run dev
```

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

✅ **Frontend is now running!** 

**Open your browser and visit:** http://localhost:5173

---

## 🎤 Test the Voice Bot

1. Click the **microphone button** in the web interface
2. Allow microphone permissions when prompted
3. Speak one of these test queries:
   - "What is my account balance?"
   - "How do I reset my password?"
   - "What are your operating hours?"
   - "Hello, how can you help me?"

4. Wait for the bot to respond with voice output!

---

## 📱 Sample Queries to Try

### Account Queries:
- "What is my account balance?"
- "Show me my account details"
- "What's my account number?"

### FAQ Queries:
- "What are your operating hours?"
- "How do I reset my password?"
- "What services do you offer?"
- "How do I open a new account?"
- "What are the transfer limits?"
- "Is my information secure?"
- "How long do transfers take?"

### General Queries:
- "Hello"
- "Help me"
- "What is your name?"
- "Thank you"
- "Goodbye"

---

## 🐛 Troubleshooting

### Backend Issues:

**Issue: "Module not found" error**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue: Database error**
```bash
# Solution: Re-seed the database
Remove-Item voicebot.db -ErrorAction SilentlyContinue
python seed_db.py
```

### Frontend Issues:

**Issue: "npm: command not found"**
```bash
# Solution: Install Node.js from https://nodejs.org/
```

**Issue: Dependencies not installed**
```bash
# Solution: Install dependencies
npm install
```

**Issue: Port 5173 already in use**
```bash
# Solution: Kill the process or use a different port
npm run dev -- --port 5174
```

### Voice Bot Issues:

**Issue: Microphone not working**
- Check browser permissions (allow microphone access)
- Use HTTPS or localhost (required for microphone API)
- Try a different browser (Chrome recommended)

**Issue: No voice output**
- Check browser audio permissions
- Check system volume
- Look for audio files in `backend/static/audio/`
- Check console for TTS errors

**Issue: "Could not understand audio"**
- Speak clearly and closer to microphone
- Reduce background noise
- Check microphone is working in other apps
- Try adding OpenAI API key for better STT

---

## 🔑 Environment Variables (Optional but Recommended)

Create a `.env` file in the `backend` directory:

```env
# For best experience, add your OpenAI API key
OPENAI_API_KEY=sk-proj-your-key-here

# Optional: For premium TTS (see TTS_CONFIGURATION.md)
# GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
# AZURE_SPEECH_KEY=your-azure-key
# AZURE_SPEECH_REGION=eastus
```

**Without OpenAI API key**: The bot will use:
- Google Speech Recognition for STT (free)
- Rule-based + database responses for NLU
- gTTS for voice output (free)

**With OpenAI API key**: The bot will use:
- OpenAI Whisper for STT (better accuracy)
- GPT-3.5-turbo for NLU (smarter responses)
- OpenAI TTS for voice output (natural voice)

---

## 📊 Testing API Endpoints

While the backend is running, test these endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Get all FAQs
curl http://localhost:8000/api/faqs

# Search FAQs
curl "http://localhost:8000/api/search/faq?q=password"

# Get all accounts
curl http://localhost:8000/api/accounts

# Get stats
curl http://localhost:8000/api/stats
```

Or visit the **interactive API documentation**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🎯 Summary

### Backend (3 commands):
```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

### Frontend (2 commands):
```bash
cd frontend
npm run dev
```

### Then:
- Open http://localhost:5173 in your browser
- Click microphone and start talking!

---

## 📚 Next Steps

1. ✅ **Read the README.md** for full documentation
2. ✅ **Check TTS_CONFIGURATION.md** to set up premium TTS providers
3. ✅ **Review PROJECT_SUMMARY.md** to understand all features
4. ✅ **Explore the API** at http://localhost:8000/docs

---

## 🎉 You're All Set!

Your intelligent voice bot is now running with:
- ✅ 20 FAQs ready to answer
- ✅ 7 sample accounts in database
- ✅ GPT-powered responses (if API key configured)
- ✅ Multiple TTS providers with fallback
- ✅ Full REST API for data access
- ✅ Beautiful React frontend

**Enjoy your AI-powered customer service voice bot! 🤖🎤**
