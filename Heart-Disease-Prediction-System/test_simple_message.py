#!/usr/bin/env python
"""
Simple test for SMS and WhatsApp
"""

from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv('.env')

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
test_phone = os.getenv('TEST_PHONE_NUMBER')

print("="*70)
print("SIMPLE MESSAGE TEST")
print("="*70)
print(f"From (SMS): {twilio_phone}")
print(f"From (WhatsApp): whatsapp:+14155238886")
print(f"To: {test_phone}")
print()

client = Client(account_sid, auth_token)

# Test SMS
print("📧 Sending SMS...")
try:
    sms = client.messages.create(
        from_=twilio_phone,
        body='📱 Test SMS from Heart Disease Prediction System!',
        to=test_phone
    )
    print(f"✅ SMS sent! SID: {sms.sid}")
    print(f"   Status: {sms.status}")
except Exception as e:
    print(f"❌ SMS failed: {e}")

print()

# Test WhatsApp
print("💬 Sending WhatsApp...")
try:
    whatsapp = client.messages.create(
        from_='whatsapp:+14155238886',
        body='💬 Test WhatsApp from Heart Disease Prediction System!',
        to=f'whatsapp:{test_phone}'
    )
    print(f"✅ WhatsApp sent! SID: {whatsapp.sid}")
    print(f"   Status: {whatsapp.status}")
except Exception as e:
    print(f"❌ WhatsApp failed: {e}")

print()
print("="*70)
print("Check your phone for messages!")
print("="*70)
