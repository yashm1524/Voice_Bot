from database import SessionLocal, FAQ, Account, engine, Base

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    # Clear existing data for fresh seed
    db.query(FAQ).delete()
    db.query(Account).delete()
    db.commit()
    
    # Seed FAQs - Comprehensive customer service questions
    faqs = [
        # General Information
        {"question": "What are your operating hours", "answer": "We are available 24/7 to assist you with all your banking needs."},
        {"question": "How can I contact customer support", "answer": "You can reach us via phone at 1-800-BANK-HELP, email at support@bank.com, or through this voice bot anytime."},
        {"question": "What is your name", "answer": "I am your intelligent voice assistant, here to help you with your banking needs."},
        {"question": "What services do you offer", "answer": "We offer checking accounts, savings accounts, loans, credit cards, investment services, and 24/7 customer support."},
        
        # Account Related
        {"question": "How do I open a new account", "answer": "You can open a new account online through our website, mobile app, or by visiting any of our branch locations with a valid ID."},
        {"question": "How do I close my account", "answer": "To close your account, please visit a branch or call our customer service at 1-800-BANK-HELP. Make sure to withdraw or transfer all funds first."},
        {"question": "What are the account fees", "answer": "We offer fee-free checking accounts with a minimum balance of $500. Savings accounts have no monthly fees. Please check our website for detailed fee schedules."},
        {"question": "How do I check my account balance", "answer": "You can check your balance through our mobile app, online banking, ATM, or by asking me directly."},
        
        # Security & Password
        {"question": "How do I reset my password", "answer": "You can reset your password by clicking 'Forgot Password' on the login page, or by calling customer service at 1-800-BANK-HELP for assistance."},
        {"question": "Is my information secure", "answer": "Yes, we use bank-level 256-bit encryption and multi-factor authentication to protect your information. Your security is our top priority."},
        {"question": "What should I do if my card is lost or stolen", "answer": "Please call us immediately at 1-800-BANK-HELP to report your lost or stolen card. We'll deactivate it and send you a replacement within 3-5 business days."},
        
        # Transactions
        {"question": "How long do transfers take", "answer": "Internal transfers are instant. External transfers typically take 1-3 business days. Wire transfers are completed within 24 hours."},
        {"question": "What are the transfer limits", "answer": "Daily transfer limits are $5,000 for standard accounts and $25,000 for premium accounts. You can request limit increases through customer service."},
        {"question": "How do I dispute a transaction", "answer": "You can dispute a transaction through the mobile app, online banking, or by calling customer service. We'll investigate and respond within 10 business days."},
        
        # Loans & Credit
        {"question": "How do I apply for a loan", "answer": "You can apply for a loan online through our website or mobile app. You'll need to provide income verification and credit information."},
        {"question": "What are your interest rates", "answer": "Interest rates vary by product. Current rates: Savings 2.5% APY, Personal Loans from 5.99% APR, Mortgages from 6.25% APR. Check our website for current rates."},
        
        # Mobile & Online Banking
        {"question": "How do I download the mobile app", "answer": "Our mobile app is available on the App Store for iOS and Google Play Store for Android. Search for 'Bank Voice Bot' and download it for free."},
        {"question": "Can I deposit checks through the app", "answer": "Yes, you can deposit checks using mobile check deposit in our app. Just take a photo of the front and back of your check."},
        
        # Additional Services
        {"question": "Do you offer investment services", "answer": "Yes, we offer investment accounts, retirement planning, and financial advisory services. Contact our investment team at 1-800-INVEST-NOW."},
        {"question": "How do I set up direct deposit", "answer": "Provide your employer with your account number and our routing number 123456789. Direct deposits typically process within 1-2 pay cycles."},
    ]
    
    for faq in faqs:
        db.add(FAQ(question=faq["question"], answer=faq["answer"]))
    print(f"Seeded {len(faqs)} FAQs.")
    
    # Seed Accounts - Multiple realistic customer accounts
    accounts = [
        {
            "username": "john_doe",
            "account_number": "ACC-2024-001",
            "email": "john.doe@email.com",
            "phone": "+1-555-0101",
            "balance": 15420.75,
            "account_type": "Checking",
            "status": "Active"
        },
        {
            "username": "jane_smith",
            "account_number": "ACC-2024-002",
            "email": "jane.smith@email.com",
            "phone": "+1-555-0102",
            "balance": 8750.50,
            "account_type": "Savings",
            "status": "Active"
        },
        {
            "username": "mike_johnson",
            "account_number": "ACC-2024-003",
            "email": "mike.j@email.com",
            "phone": "+1-555-0103",
            "balance": 3200.00,
            "account_type": "Checking",
            "status": "Active"
        },
        {
            "username": "sarah_williams",
            "account_number": "ACC-2024-004",
            "email": "sarah.w@email.com",
            "phone": "+1-555-0104",
            "balance": 52100.25,
            "account_type": "Premium Savings",
            "status": "Active"
        },
        {
            "username": "david_brown",
            "account_number": "ACC-2024-005",
            "email": "david.brown@email.com",
            "phone": "+1-555-0105",
            "balance": 1050.80,
            "account_type": "Student Checking",
            "status": "Active"
        },
        {
            "username": "emily_davis",
            "account_number": "ACC-2024-006",
            "email": "emily.d@email.com",
            "phone": "+1-555-0106",
            "balance": 28900.00,
            "account_type": "Business Checking",
            "status": "Active"
        },
        {
            "username": "test_user",
            "account_number": "ACC-TEST-999",
            "email": "test@test.com",
            "phone": "+1-555-9999",
            "balance": 10000.00,
            "account_type": "Checking",
            "status": "Active"
        }
    ]
    
    for acc in accounts:
        db.add(Account(
            username=acc["username"],
            account_number=acc["account_number"],
            email=acc["email"],
            phone=acc["phone"],
            balance=acc["balance"],
            account_type=acc["account_type"],
            status=acc["status"]
        ))
    print(f"Seeded {len(accounts)} Accounts.")

    db.commit()
    db.close()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_data()
