from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from services.stt import transcribe_audio
from services.nlu import generate_response
from services.tts import text_to_speech
from database import SessionLocal, Interaction
import shutil
import os
import uuid
import time

app = FastAPI(title="Voice Bot API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CORS Configuration
origins = [
    "https://voice-bot-frontend.onrender.com",
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for audio playback
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Voice Bot API is running"}

@app.post("/api/process-audio")
async def process_audio(file: UploadFile = File(...), db: Session = Depends(get_db)):
    start_time = time.time()
    
    # Save uploaded file
    temp_filename = f"temp_{uuid.uuid4()}.wav"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # DEBUG: Check file header
    with open(temp_filename, "rb") as f:
        header = f.read(16)
        print(f"DEBUG: File header bytes: {header}")
        if header.startswith(b'RIFF'):
            print("DEBUG: Format is WAV (RIFF)")
        elif header.startswith(b'\x1a\x45\xdf\xa3'):
            print("DEBUG: Format is WebM/MKV")
        else:
            print(f"DEBUG: Unknown format: {header.hex()}")

    try:
        # 1. Speech to Text
        user_text = transcribe_audio(temp_filename)
        
        # 2. NLU & Response Generation
        bot_response_text = generate_response(user_text)
        
        # 3. Text to Speech
        audio_path = text_to_speech(bot_response_text)
        
        # Return relative path for frontend to access
        if audio_path:
            audio_url = f"/static/audio/{os.path.basename(audio_path)}"
        else:
            audio_url = None
        
        # Log to DB
        duration_ms = (time.time() - start_time) * 1000
        interaction = Interaction(
            user_text=user_text,
            bot_response=bot_response_text,
            response_time_ms=duration_ms
        )
        db.add(interaction)
        db.commit()
        
        return {
            "user_text": user_text,
            "bot_response": bot_response_text,
            "audio_url": audio_url
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"CRITICAL ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str

@app.post("/api/process-text")
async def process_text(request: TextRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    user_text = request.text
    
    try:
        # 1. NLU & Response Generation
        bot_response_text = generate_response(user_text)
        
        # 2. Text to Speech
        audio_path = text_to_speech(bot_response_text)
        
        # Return relative path for frontend to access
        if audio_path:
            audio_url = f"/static/audio/{os.path.basename(audio_path)}"
        else:
            audio_url = None
        
        # Log to DB
        duration_ms = (time.time() - start_time) * 1000
        interaction = Interaction(
            user_text=user_text,
            bot_response=bot_response_text,
            response_time_ms=duration_ms
        )
        db.add(interaction)
        db.commit()
        
        return {
            "user_text": user_text,
            "bot_response": bot_response_text,
            "audio_url": audio_url
        }
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    total_queries = db.query(Interaction).count()
    interactions = db.query(Interaction).all()
    avg_time = sum([i.response_time_ms for i in interactions]) / total_queries if total_queries > 0 else 0
    
    return {
        "queries": total_queries,
        "avgResponseTime": round(avg_time)
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/faqs")
async def get_faqs(db: Session = Depends(get_db)):
    """Get all FAQs from the database"""
    from database import FAQ
    faqs = db.query(FAQ).all()
    return {
        "count": len(faqs),
        "faqs": [{"id": faq.id, "question": faq.question, "answer": faq.answer} for faq in faqs]
    }

@app.get("/api/faqs/{faq_id}")
async def get_faq(faq_id: int, db: Session = Depends(get_db)):
    """Get a specific FAQ by ID"""
    from database import FAQ
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return {"id": faq.id, "question": faq.question, "answer": faq.answer}

@app.get("/api/accounts")
async def get_accounts(db: Session = Depends(get_db)):
    """Get all accounts from the database (for demo purposes)"""
    from database import Account
    accounts = db.query(Account).all()
    return {
        "count": len(accounts),
        "accounts": [
            {
                "id": acc.id,
                "username": acc.username,
                "account_number": acc.account_number,
                "email": acc.email,
                "phone": acc.phone,
                "balance": acc.balance,
                "account_type": acc.account_type,
                "status": acc.status
            } for acc in accounts
        ]
    }

@app.get("/api/accounts/{account_id}")
async def get_account(account_id: int, db: Session = Depends(get_db)):
    """Get a specific account by ID"""
    from database import Account
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {
        "id": account.id,
        "username": account.username,
        "account_number": account.account_number,
        "email": account.email,
        "phone": account.phone,
        "balance": account.balance,
        "account_type": account.account_type,
        "status": account.status
    }

@app.get("/api/search/faq")
async def search_faq(q: str, db: Session = Depends(get_db)):
    """Search FAQs by keyword"""
    from database import FAQ
    faqs = db.query(FAQ).filter(FAQ.question.contains(q) | FAQ.answer.contains(q)).all()
    return {
        "query": q,
        "count": len(faqs),
        "results": [{"id": faq.id, "question": faq.question, "answer": faq.answer} for faq in faqs]
    }

