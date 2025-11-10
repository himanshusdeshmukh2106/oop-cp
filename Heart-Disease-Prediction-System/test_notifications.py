#!/usr/bin/env python
"""
Test SMS and WhatsApp Notifications
Tests the notification system with your actual phone number
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_desease.settings')

import django
django.setup()

from health.ai_calling_agent import AICallingAgent

def test_notifications():
    """Test SMS and WhatsApp notifications"""
    
    print("="*70)
    print("TESTING SMS & WHATSAPP NOTIFICATIONS")
    print("="*70)
    print()
    
    # Initialize agent
    agent = AICallingAgent()
    
    # Get test phone number from environment
    test_phone = os.getenv('TEST_PHONE_NUMBER', '+918087980346')
    
    # For WhatsApp, use the sandbox number
    whatsapp_sandbox = '+917385864727'
    
    print(f"📱 Test Phone (SMS): {test_phone}")
    print(f"📱 WhatsApp Sandbox: {whatsapp_sandbox}")
    print()
    
    # Test appointment details
    appointment_details = {
        'hospital_name': 'Ruby Hall Clinic',
        'hospital_address': 'Grant Road, Pune, Maharashtra 411001',
        'hospital_phone': '+912026121212',
        'date': 'November 11, 2025',
        'time': '10:00 AM',
        'status': 'Test notification - Please confirm',
        'call_duration': '45 seconds'
    }
    
    # Test SMS
    print("📧 Testing SMS...")
    print("-" * 70)
    sms_result = agent.send_sms_confirmation(test_phone, appointment_details)
    
    if sms_result:
        print(f"✅ SMS sent successfully!")
        print(f"   SID: {sms_result}")
    else:
        print(f"❌ SMS failed to send")
    
    print()
    
    # Test WhatsApp
    print("💬 Testing WhatsApp...")
    print("-" * 70)
    print(f"   Note: Make sure you've joined the WhatsApp sandbox")
    print(f"   Send 'join <code>' to {whatsapp_sandbox}")
    print()
    
    whatsapp_result = agent.send_whatsapp_confirmation(test_phone, appointment_details)
    
    if whatsapp_result:
        print(f"✅ WhatsApp sent successfully!")
        print(f"   SID: {whatsapp_result}")
    else:
        print(f"❌ WhatsApp failed to send")
        print(f"   This is normal if you haven't joined the sandbox yet")
    
    print()
    print("="*70)
    print("TEST COMPLETE")
    print("="*70)
    print()
    
    if sms_result or whatsapp_result:
        print("✅ At least one notification sent successfully!")
        print()
        print("Check your phone for:")
        if sms_result:
            print(f"  - SMS on {test_phone}")
        if whatsapp_result:
            print(f"  - WhatsApp on {test_phone}")
    else:
        print("❌ No notifications sent")
        print()
        print("Possible issues:")
        print("  1. Twilio credentials invalid")
        print("  2. Phone number not verified (trial account)")
        print("  3. WhatsApp sandbox not joined")
        print()
        print("To fix:")
        print("  1. Check Twilio credentials in .env")
        print("  2. Verify phone number at: https://console.twilio.com/")
        print("  3. Join WhatsApp sandbox at: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn")

if __name__ == '__main__':
    test_notifications()
