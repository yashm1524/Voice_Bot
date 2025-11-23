import os
from openai import OpenAI
from dotenv import load_dotenv
import requests

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an intelligent customer support voice bot for a banking institution. 
Your goal is to assist users with their queries efficiently and politely.
Keep your responses concise and conversational, suitable for voice output.
When providing account information, be clear and professional.
If you don't have specific information, guide users on how to get help.
"""

def query_database(user_text: str) -> dict:
    """
    Query the database for FAQs and Account information.
    Returns a dict with 'type' and 'data' if found, None otherwise.
    """
    try:
        from database import SessionLocal, FAQ, Account
        db = SessionLocal()
        text_lower = user_text.lower()
        
        # Check for Account-related queries
        if any(keyword in text_lower for keyword in ["account", "balance", "my account", "account details", "account info"]):
            # For demo purposes, we'll return the first account
            # In production, you'd authenticate and get the specific user's account
            account = db.query(Account).first()
            if account:
                db.close()
                return {
                    "type": "account",
                    "data": {
                        "username": account.username,
                        "account_number": account.account_number,
                        "email": account.email,
                        "phone": account.phone,
                        "balance": account.balance,
                        "account_type": account.account_type,
                        "status": account.status
                    }
                }
        
        # Check for FAQ queries - Use fuzzy matching
        faqs = db.query(FAQ).all()
        best_match = None
        best_score = 0
        
        for faq in faqs:
            # Simple word matching score
            faq_words = set(faq.question.lower().split())
            user_words = set(text_lower.split())
            common_words = faq_words.intersection(user_words)
            score = len(common_words)
            
            if score > best_score and score >= 2:  # At least 2 words match
                best_score = score
                best_match = faq
        
        if best_match:
            db.close()
            return {
                "type": "faq",
                "data": {
                    "question": best_match.question,
                    "answer": best_match.answer
                }
            }
        
        db.close()
        return None
        
    except Exception as e:
        print(f"Database Query Error: {e}")
        return None


def query_ollama(system_prompt: str, user_text: str) -> str:
    """
    Attempts to generate a response using a local Ollama instance.
    """
    try:
        # First check if Ollama is running with a quick timeout
        try:
            requests.get("http://localhost:11434", timeout=1)
        except requests.exceptions.ConnectionError:
            print("DEBUG: Ollama not running (connection refused). Skipping.")
            return None
        except Exception:
            pass

        # Try standard models: llama3, mistral, llama2
        models = ["llama3", "mistral", "llama2"]
        
        for model in models:
            try:
                url = "http://localhost:11434/api/chat"
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_text}
                    ],
                    "stream": False
                }
                print(f"DEBUG: Trying Ollama with model {model}...")
                response = requests.post(url, json=payload, timeout=5) # Reduced timeout
                if response.status_code == 200:
                    return response.json().get("message", {}).get("content", "")
            except Exception:
                continue
                
        return None
    except Exception as e:
        print(f"Ollama Connection Error: {e}")
        return None


def generate_response(user_text: str) -> str:
    """
    Generates a response using GPT with database integration, Ollama and rule-based fallbacks.
    Priority: Database -> GPT -> Ollama -> Rule-based
    """
    
    # 1. Check Database First (FAQs and Account Info)
    db_result = query_database(user_text)
    
    if db_result:
        if db_result["type"] == "account":
            # Format account information nicely
            acc = db_result["data"]
            response = f"Here are your account details: Account holder {acc['username']}, "
            response += f"Account number {acc['account_number']}, "
            response += f"Account type {acc['account_type']}, "
            response += f"Current balance ${acc['balance']:,.2f}, "
            response += f"Status {acc['status']}. "
            response += f"Your registered email is {acc['email']} and phone is {acc['phone']}."
            
            # Use GPT to make it more conversational if available
            if os.getenv("OPENAI_API_KEY"):
                try:
                    gpt_response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful banking assistant. Rephrase the following account information in a friendly, conversational way suitable for voice output. Keep it concise."},
                            {"role": "user", "content": response}
                        ]
                    )
                    return gpt_response.choices[0].message.content
                except Exception as e:
                    print(f"GPT formatting error: {e}")
                    return response
            return response
            
        elif db_result["type"] == "faq":
            # Return FAQ answer directly
            return db_result["data"]["answer"]
    
    # 2. Try OpenAI GPT (with database context)
    if os.getenv("OPENAI_API_KEY"):
        try:
            # Provide context about available data
            enhanced_prompt = SYSTEM_PROMPT + """
            
You have access to a database with:
- Customer account information (balance, account number, contact details)
- Frequently asked questions about banking services

If the user asks about their account or common banking questions, provide helpful responses.
"""
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", 
                messages=[
                    {"role": "system", "content": enhanced_prompt},
                    {"role": "user", "content": user_text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI NLU Error: {e}")
    
    # 3. Try Ollama (Local Fallback)
    print("DEBUG: Attempting Local LLM (Ollama)...")
    ollama_response = query_ollama(SYSTEM_PROMPT, user_text)
    if ollama_response:
        return ollama_response

    # 4. Rule-based Fallback
    print("DEBUG: Using rule-based fallback.")
    text_lower = user_text.lower()
    
    if any(word in text_lower for word in ["hello", "hi", "hey"]):
        return "Hello! I'm your banking voice assistant. How can I help you today?"
    elif "help" in text_lower:
        return "I can help you with account details, FAQs, balance inquiries, and general banking questions. What would you like to know?"
    elif "name" in text_lower:
        return "I am your intelligent banking voice assistant, powered by AI."
    elif any(word in text_lower for word in ["bye", "goodbye", "see you"]):
        return "Goodbye! Thank you for using our service. Have a great day!"
    elif "thank" in text_lower:
        return "You're welcome! Is there anything else I can help you with?"
    else:
        return f"I heard you say: {user_text}. I'm here to help with account information and banking questions. Could you please rephrase your question?"
