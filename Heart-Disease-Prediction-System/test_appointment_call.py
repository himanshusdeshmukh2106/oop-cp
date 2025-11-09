"""
Test the AI Calling Agent for Appointment Booking
"""

import os
import sys
from dotenv import load_dotenv

# Add the project to path
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
load_dotenv()

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_desease.settings')
import django
django.setup()

from health.ai_calling_agent import AICallingAgent

def test_simple_call():
    """Test 1: Simple 'Ahoy World' call"""
    print("=" * 60)
    print("TEST 1: Simple Twilio Call")
    print("=" * 60)
    
    from twilio.rest import Client
    
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    phone_number = os.getenv('TWILIO_PHONE_NUMBER')
    test_number = os.getenv('TEST_PHONE_NUMBER')
    
    client = Client(account_sid, auth_token)
    
    try:
        call = client.calls.create(
            twiml="<Response><Say>Hello! This is a test call from your Heart Disease Prediction System. The AI calling agent is working correctly.</Say></Response>",
            to=test_number,
            from_=phone_number,
        )
        
        print(f"✓ Call initiated successfully!")
        print(f"  Call SID: {call.sid}")
        print(f"  Status: {call.status}")
        print(f"  To: {call.to}")
        print(f"  From: {call.from_}")
        return True
    except Exception as e:
        print(f"✗ Call failed: {str(e)}")
        return False

def test_appointment_booking():
    """Test 2: Full appointment booking call"""
    print("\n" + "=" * 60)
    print("TEST 2: Appointment Booking Call")
    print("=" * 60)
    
    agent = AICallingAgent()
    
    # Test patient data
    patient_data = {
        'name': 'John Doe',
        'contact': '+918087980346',
        'age': 45,
    }
    
    appointment_details = {
        'reason': 'Cardiac consultation - ECG shows abnormal results',
        'date': 'As soon as possible',
        'time': 'Morning preferred',
        'hospital_name': 'Test Hospital',
    }
    
    try:
        call_sid = agent.initiate_appointment_call(
            hospital_phone='+918087980346',  # Will use TEST_PHONE_NUMBER
            patient_data=patient_data,
            appointment_details=appointment_details
        )
        
        print(f"✓ Appointment booking call initiated!")
        print(f"  Call SID: {call_sid}")
        print(f"  Patient: {patient_data['name']}")
        print(f"  Reason: {appointment_details['reason']}")
        return True
    except Exception as e:
        print(f"✗ Appointment call failed: {str(e)}")
        return False

def test_sms_confirmation():
    """Test 3: SMS confirmation"""
    print("\n" + "=" * 60)
    print("TEST 3: SMS Confirmation")
    print("=" * 60)
    
    agent = AICallingAgent()
    
    appointment_details = {
        'hospital_name': 'City Cardiac Center',
        'date': 'November 12, 2025',
        'time': '10:00 AM',
        'hospital_phone': '+911234567890',
    }
    
    try:
        message_sid = agent.send_sms_confirmation(
            patient_phone=os.getenv('TEST_PHONE_NUMBER'),
            appointment_details=appointment_details
        )
        
        if message_sid:
            print(f"✓ SMS sent successfully!")
            print(f"  Message SID: {message_sid}")
            return True
        else:
            print(f"✗ SMS failed to send")
            return False
    except Exception as e:
        print(f"✗ SMS failed: {str(e)}")
        return False

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("TWILIO AI CALLING AGENT TEST SUITE")
    print("=" * 60)
    print(f"Account SID: {os.getenv('TWILIO_ACCOUNT_SID')}")
    print(f"Phone Number: {os.getenv('TWILIO_PHONE_NUMBER')}")
    print(f"Test Number: {os.getenv('TEST_PHONE_NUMBER')}")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Simple Call", test_simple_call()))
    results.append(("Appointment Booking", test_appointment_booking()))
    results.append(("SMS Confirmation", test_sms_confirmation()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)
