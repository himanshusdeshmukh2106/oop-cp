#!/usr/bin/env python
"""
Comprehensive System Check for Heart Disease Prediction System
Verifies all components are properly configured and functional
"""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_desease.settings')

import django
django.setup()

from django.conf import settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

print("="*70)
print("HEART DISEASE PREDICTION SYSTEM - COMPREHENSIVE CHECK")
print("="*70)
print()

# 1. Environment Variables Check
print("📋 1. ENVIRONMENT VARIABLES")
print("-" * 70)

env_vars = {
    'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
    'GOOGLE_MAPS_API_KEY': os.getenv('GOOGLE_MAPS_API_KEY'),
    'TWILIO_ACCOUNT_SID': os.getenv('TWILIO_ACCOUNT_SID'),
    'TWILIO_AUTH_TOKEN': os.getenv('TWILIO_AUTH_TOKEN'),
    'TWILIO_PHONE_NUMBER': os.getenv('TWILIO_PHONE_NUMBER'),
    'TEST_PHONE_NUMBER': os.getenv('TEST_PHONE_NUMBER'),
}

all_env_ok = True
for key, value in env_vars.items():
    if value:
        masked = value[:10] + '...' if len(value) > 10 else value
        print(f"   ✅ {key}: {masked}")
    else:
        print(f"   ❌ {key}: NOT SET")
        all_env_ok = False

print()

# 2. Required Packages Check
print("📦 2. REQUIRED PACKAGES")
print("-" * 70)

packages = {
    'django': 'Django',
    'sklearn': 'scikit-learn',
    'pandas': 'pandas',
    'numpy': 'numpy',
    'PIL': 'Pillow',
    'twilio': 'twilio',
    'google.generativeai': 'google-generativeai',
    'dotenv': 'python-dotenv',
}

all_packages_ok = True
for module, package in packages.items():
    try:
        __import__(module)
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ❌ {package} - NOT INSTALLED")
        all_packages_ok = False

print()

# 3. ML Models Check
print("🤖 3. MACHINE LEARNING MODELS")
print("-" * 70)

models_dir = Path(__file__).parent / 'trained_models'
required_models = [
    'logistic_regression.pkl',
    'random_forest.pkl',
    'decision_tree.pkl',
    'knn.pkl',
    'naive_bayes.pkl',
    'scaler.pkl',
]

all_models_ok = True
for model in required_models:
    model_path = models_dir / model
    if model_path.exists():
        size = model_path.stat().st_size / 1024  # KB
        print(f"   ✅ {model} ({size:.1f} KB)")
    else:
        print(f"   ❌ {model} - NOT FOUND")
        all_models_ok = False

print()

# 4. ECG Models Check
print("📊 4. ECG ANALYSIS MODELS")
print("-" * 70)

ecg_models = [
    'ecg_cnn_model.h5',
    'ecg_resnet_model.h5',
]

all_ecg_ok = True
for model in ecg_models:
    model_path = models_dir / model
    if model_path.exists():
        size = model_path.stat().st_size / (1024 * 1024)  # MB
        print(f"   ✅ {model} ({size:.1f} MB)")
    else:
        print(f"   ❌ {model} - NOT FOUND")
        all_ecg_ok = False

print()

# 5. Database Check
print("💾 5. DATABASE")
print("-" * 70)

try:
    from health.models import Patient, Doctor, Appointment
    
    patient_count = Patient.objects.count()
    doctor_count = Doctor.objects.count()
    appointment_count = Appointment.objects.count()
    
    print(f"   ✅ Database connected")
    print(f"   📊 Patients: {patient_count}")
    print(f"   📊 Doctors: {doctor_count}")
    print(f"   📊 Appointments: {appointment_count}")
    db_ok = True
except Exception as e:
    print(f"   ❌ Database error: {str(e)}")
    db_ok = False

print()

# 6. AI Calling Agent Check
print("🤖 6. AI CALLING AGENT")
print("-" * 70)

try:
    from health.ai_calling_agent import AICallingAgent
    
    agent = AICallingAgent()
    
    if agent.client:
        print(f"   ✅ Twilio client initialized")
    else:
        print(f"   ❌ Twilio client not configured")
    
    if agent.gemini_model:
        print(f"   ✅ Gemini AI initialized")
    else:
        print(f"   ❌ Gemini AI not configured")
    
    ai_ok = agent.client is not None and agent.gemini_model is not None
except Exception as e:
    print(f"   ❌ AI Calling Agent error: {str(e)}")
    ai_ok = False

print()

# 7. Settings Check
print("⚙️  7. DJANGO SETTINGS")
print("-" * 70)

print(f"   DEBUG: {settings.DEBUG}")
print(f"   BASE_URL: {getattr(settings, 'BASE_URL', 'NOT SET')}")
print(f"   GOOGLE_MAPS_API_KEY: {'SET' if getattr(settings, 'GOOGLE_MAPS_API_KEY', '') else 'NOT SET'}")

print()

# 8. Templates Check
print("📄 8. TEMPLATES")
print("-" * 70)

templates_dir = Path(__file__).parent / 'health' / 'templates'
required_templates = [
    'find_doctors.html',
    'book_appointment.html',
    'my_appointments.html',
    'upload_ecg.html',
    'ecg_result.html',
]

all_templates_ok = True
for template in required_templates:
    template_path = templates_dir / template
    if template_path.exists():
        print(f"   ✅ {template}")
    else:
        print(f"   ❌ {template} - NOT FOUND")
        all_templates_ok = False

print()

# Final Summary
print("="*70)
print("SUMMARY")
print("="*70)

checks = {
    'Environment Variables': all_env_ok,
    'Required Packages': all_packages_ok,
    'ML Models': all_models_ok,
    'ECG Models': all_ecg_ok,
    'Database': db_ok,
    'AI Calling Agent': ai_ok,
    'Templates': all_templates_ok,
}

all_ok = all(checks.values())

for check, status in checks.items():
    icon = "✅" if status else "❌"
    print(f"{icon} {check}")

print()

if all_ok:
    print("🎉 ALL SYSTEMS OPERATIONAL!")
    print()
    print("You can now:")
    print("  1. Run: python manage.py runserver")
    print("  2. Visit: http://localhost:8000")
    print("  3. Test AI calling with ngrok running")
    sys.exit(0)
else:
    print("⚠️  SOME SYSTEMS NEED ATTENTION")
    print()
    print("Please fix the issues marked with ❌ above")
    sys.exit(1)
