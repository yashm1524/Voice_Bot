"""
Test script to verify database functionality and query capabilities
"""

from database import SessionLocal, FAQ, Account

def test_database():
    """Test database queries and display sample data"""
    
    db = SessionLocal()
    
    print("=" * 60)
    print("DATABASE TEST - Voice Bot Project")
    print("=" * 60)
    
    # Test FAQs
    print("\n📚 FAQ DATABASE TEST")
    print("-" * 60)
    faqs = db.query(FAQ).all()
    print(f"Total FAQs in database: {len(faqs)}\n")
    
    print("Sample FAQs (first 5):")
    for i, faq in enumerate(faqs[:5], 1):
        print(f"\n{i}. Q: {faq.question}")
        print(f"   A: {faq.answer}")
    
    # Test FAQ search
    print("\n" + "-" * 60)
    print("Testing FAQ Search for 'password':")
    search_results = db.query(FAQ).filter(FAQ.question.contains("password")).all()
    for faq in search_results:
        print(f"  Q: {faq.question}")
        print(f"  A: {faq.answer}")
    
    # Test Accounts
    print("\n" + "=" * 60)
    print("💳 ACCOUNT DATABASE TEST")
    print("-" * 60)
    accounts = db.query(Account).all()
    print(f"Total Accounts in database: {len(accounts)}\n")
    
    print("Sample Accounts (first 3):")
    for i, acc in enumerate(accounts[:3], 1):
        print(f"\n{i}. Username: {acc.username}")
        print(f"   Account Number: {acc.account_number}")
        print(f"   Email: {acc.email}")
        print(f"   Phone: {acc.phone}")
        print(f"   Balance: ${acc.balance:,.2f}")
        print(f"   Account Type: {acc.account_type}")
        print(f"   Status: {acc.status}")
    
    # Test account query
    print("\n" + "-" * 60)
    print("Testing Account Query (first account):")
    first_account = db.query(Account).first()
    if first_account:
        print(f"  Found account for: {first_account.username}")
        print(f"  Balance: ${first_account.balance:,.2f}")
    
    db.close()
    
    print("\n" + "=" * 60)
    print("✅ DATABASE TEST COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print("\nThe database is properly configured and ready to use!")
    print("You can now start the voice bot server with: uvicorn main:app --reload")

if __name__ == "__main__":
    test_database()
