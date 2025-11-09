"""
Simple Twilio Call Test Script
Based on official Twilio documentation pattern
"""

# Download the helper library from https://www.twilio.com/docs/python/install
import os
import sys
from pathlib import Path
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from parent directory
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"✓ Loaded .env from: {env_path}")
else:
    load_dotenv()  # Try current directory
    print("⚠ Using .env from current directory")

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
print("\n" + "="*60)
print("TWILIO AI CALLING AGENT - SIMPLE TEST")
print("="*60)

try:
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    phone_number = os.environ["TWILIO_PHONE_NUMBER"]
    test_number = os.environ.get("TEST_PHONE_NUMBER", "+918087980346")
    
    print(f"Account SID: {account_sid[:10]}...")
    print(f"Phone Number: {phone_number}")
    print(f"Test Number: {test_number}")
    print("="*60)
    
    client = Client(account_sid, auth_token)
    
    print("\n📞 Initiating call...")
    
    # Make the call (using Twilio's demo TwiML URL)
    call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",  # Twilio's demo TwiML
        to=test_number,
        from_=phone_number,
    )
    
    print("\n✓ Call initiated successfully!")
    print("="*60)
    print(f"Call SID: {call.sid}")
    print(f"Status: {call.status}")
    print(f"To: {call.to}")
    print(f"From: {phone_number}")
    print("="*60)
    print("\n📱 Your phone should ring shortly!")
    print("   Caller ID will show:", phone_number)
    print("   You'll hear: 'Ahoy, World! This is a test call...'")
    print("\n✓ Test completed successfully!")
    
except KeyError as e:
    print(f"\n✗ Error: Missing environment variable {e}")
    print("\nPlease check your .env file has:")
    print("  - TWILIO_ACCOUNT_SID")
    print("  - TWILIO_AUTH_TOKEN")
    print("  - TWILIO_PHONE_NUMBER")
    print("  - TEST_PHONE_NUMBER (optional)")
    sys.exit(1)
    
except Exception as e:
    print(f"\n✗ Error: {str(e)}")
    print("\nPossible issues:")
    print("  - Check your Twilio credentials are correct")
    print("  - Verify phone numbers are in E.164 format (+918087980346)")
    print("  - Ensure your Twilio account has credits")
    print("  - Check Twilio console: https://console.twilio.com/us1/monitor/logs/calls")
    sys.exit(1)
