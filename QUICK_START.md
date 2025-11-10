# Quick Start Guide

## 🚀 Start in 3 Steps

### Step 1: Start ngrok (for AI calling)
```bash
ngrok http 8000
```
Keep this terminal open. Note the URL (e.g., `https://your-unique-id.ngrok-free.app`)

### Step 2: Start Django Server
```bash
cd Heart-Disease-Prediction-System
python manage.py runserver
```

### Step 3: Open Browser
Visit: **http://localhost:8000**

## ✅ System Check

Run this to verify everything is working:
```bash
python Heart-Disease-Prediction-System/system_check.py
```

## 🎯 Test Features

### 1. Login
- **Patient**: Use existing account or register new
- **Doctor**: Use existing doctor account
- **Admin**: Use admin credentials

### 2. Predict Heart Disease
1. Login as patient
2. Click "Predict Disease"
3. Enter health parameters
4. Get instant AI prediction

### 3. Analyze ECG
1. Login as patient
2. Click "ECG Analysis"
3. Upload ECG image
4. Get AI analysis results

### 4. Find Doctors & Book
1. Login as patient
2. Click "Find Doctors"
3. See doctors on Google Maps
4. Search nearby hospitals
5. Click "Book Appointment"
6. Choose AI Agent or Manual Call

### 5. Test AI Calling
1. Ensure ngrok is running
2. Click "Let AI Agent Call & Book"
3. Answer your configured test phone
4. Have a conversation with the AI!

## 📊 What You'll See

### Patient Dashboard
- Predict heart disease
- Upload ECG for analysis
- Find nearby doctors
- Book appointments
- View appointment history
- View prediction history

### Doctor Dashboard
- View patient predictions
- Manage profile
- View appointment requests

### Admin Dashboard
- Manage doctors
- Manage patients
- View all predictions
- View feedback

## 🤖 AI Calling Demo

When you test AI calling:

```
📞 Your phone rings...

AI: "Hello, this is an automated appointment booking assistant 
     calling on behalf of [Your Name]. I'm calling to schedule 
     a cardiac consultation appointment. Am I speaking with the 
     appointment desk?"

You: "Yes, what's the patient's name?"

AI: "The patient's name is [Your Name]. They recently had an ECG 
     analysis showing concerning cardiac results and need a 
     consultation as soon as possible."

You: "What's their contact number?"

AI: "The patient's contact number is [PHONE_NUMBER]. They're 
     available for morning appointments if possible."

You: "We have an opening tomorrow at 10 AM."

AI: "Perfect! That works well. I'll confirm those details with 
     the patient. Thank you for your assistance!"
```

## 🔧 Troubleshooting

### Django won't start
```bash
python manage.py migrate
python manage.py runserver
```

### ngrok URL changed
Update `settings.py`:
```python
BASE_URL = 'https://your-unique-id.ngrok-free.app'
```

### AI calling not working
1. Check ngrok is running
2. Check BASE_URL in settings.py
3. Check .env has all required credentials
4. Run system_check.py

### Can't login
Create superuser:
```bash
python manage.py createsuperuser
```

## 📱 URLs

- **App**: http://localhost:8000
- **Admin**: http://localhost:8000/admin
- **ngrok Dashboard**: http://127.0.0.1:4040
- **Voice API Console**: Check your provider's dashboard

## 🎉 You're Ready!

The system is fully operational. Start exploring and testing all the features!

For detailed information, see:
- `SYSTEM_STATUS.md` - Complete system status
- `SETUP_GUIDE.md` - Detailed setup instructions
- `system_check.py` - Run diagnostics
