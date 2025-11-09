# Testing vs Production - Phone Number Behavior

## 🧪 TESTING MODE (Development)

### .env Configuration
```env
TEST_PHONE_NUMBER = '+918087980346'  # ← YOUR phone (ENABLED)
```

### What Happens

```
Your Code:
┌──────────────────────────────────────────────────────────┐
│ agent.initiate_appointment_call(                         │
│     hospital_phone="+911234567890",  ← Hospital A        │
│     patient_data={...},                                  │
│     appointment_details={...}                            │
│ )                                                        │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
ai_calling_agent.py:
┌──────────────────────────────────────────────────────────┐
│ # Line 62-64                                             │
│ test_number = os.getenv('TEST_PHONE_NUMBER')            │
│ if test_number:                                          │
│     hospital_phone = test_number  # ← OVERRIDE!          │
│                                                          │
│ hospital_phone is now: "+918087980346"                  │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
Twilio API:
┌──────────────────────────────────────────────────────────┐
│ call = client.calls.create(                              │
│     to="+918087980346",      ← YOUR phone (not hospital) │
│     from_="+19063656394",    ← Your Twilio number        │
│     twiml="<Response>...</Response>"                     │
│ )                                                        │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
Result:
┌──────────────────────────────────────────────────────────┐
│ 📱 YOUR PHONE RINGS!                                     │
│                                                          │
│ Caller ID: +19063656394                                 │
│ Message: "Hello, this is an automated appointment..."   │
│                                                          │
│ Hospital A (+911234567890) NEVER receives the call      │
└──────────────────────────────────────────────────────────┘
```

### Multiple Calls Example

```python
# Call 1: Hospital A
agent.initiate_appointment_call(hospital_phone="+911111111111", ...)
# → YOUR phone rings: +918087980346

# Call 2: Hospital B
agent.initiate_appointment_call(hospital_phone="+912222222222", ...)
# → YOUR phone rings: +918087980346

# Call 3: Hospital C
agent.initiate_appointment_call(hospital_phone="+913333333333", ...)
# → YOUR phone rings: +918087980346
```

**ALL calls go to YOUR phone!**

---

## 🚀 PRODUCTION MODE (Live)

### .env Configuration
```env
# TEST_PHONE_NUMBER = '+918087980346'  # ← Commented out (DISABLED)
```

### What Happens

```
Your Code:
┌──────────────────────────────────────────────────────────┐
│ agent.initiate_appointment_call(                         │
│     hospital_phone="+911234567890",  ← Hospital A        │
│     patient_data={...},                                  │
│     appointment_details={...}                            │
│ )                                                        │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
ai_calling_agent.py:
┌──────────────────────────────────────────────────────────┐
│ # Line 62-64                                             │
│ test_number = os.getenv('TEST_PHONE_NUMBER')            │
│ if test_number:  # ← False (not set)                    │
│     hospital_phone = test_number                         │
│                                                          │
│ hospital_phone stays: "+911234567890"  ← Original value │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
Twilio API:
┌──────────────────────────────────────────────────────────┐
│ call = client.calls.create(                              │
│     to="+911234567890",      ← Hospital A (real number)  │
│     from_="+19063656394",    ← Your Twilio number        │
│     twiml="<Response>...</Response>"                     │
│ )                                                        │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
Result:
┌──────────────────────────────────────────────────────────┐
│ 🏥 HOSPITAL A PHONE RINGS!                               │
│                                                          │
│ Caller ID: +19063656394                                 │
│ Message: "Hello, this is an automated appointment..."   │
│                                                          │
│ Your phone (+918087980346) does NOT ring                │
└──────────────────────────────────────────────────────────┘
```

### Multiple Calls Example

```python
# Call 1: Hospital A
agent.initiate_appointment_call(hospital_phone="+911111111111", ...)
# → Hospital A rings: +911111111111

# Call 2: Hospital B
agent.initiate_appointment_call(hospital_phone="+912222222222", ...)
# → Hospital B rings: +912222222222

# Call 3: Hospital C
agent.initiate_appointment_call(hospital_phone="+913333333333", ...)
# → Hospital C rings: +913333333333
```

**Each hospital gets their own call!**

---

## 📊 Side-by-Side Comparison

| Aspect | Testing Mode | Production Mode |
|--------|-------------|-----------------|
| **TEST_PHONE_NUMBER** | Set (e.g., +918087980346) | Commented out |
| **Who receives calls?** | YOUR phone | Real hospitals |
| **Hospital A call goes to** | +918087980346 (you) | +911111111111 (Hospital A) |
| **Hospital B call goes to** | +918087980346 (you) | +912222222222 (Hospital B) |
| **Hospital C call goes to** | +918087980346 (you) | +913333333333 (Hospital C) |
| **Safe for testing?** | ✅ Yes | ❌ No (calls real hospitals) |
| **Ready for production?** | ❌ No | ✅ Yes |

---

## 🔄 Switching Between Modes

### Enable Testing Mode

```bash
# Edit .env file
nano .env

# Make sure this line is UNCOMMENTED:
TEST_PHONE_NUMBER = '+918087980346'
```

### Enable Production Mode

```bash
# Edit .env file
nano .env

# COMMENT OUT this line:
# TEST_PHONE_NUMBER = '+918087980346'
```

---

## 🎯 Real-World Scenarios

### Scenario 1: Testing Your Code

```env
# .env
TEST_PHONE_NUMBER = '+918087980346'
```

```python
# Test with 5 different hospitals
for hospital in hospitals:
    agent.initiate_appointment_call(
        hospital_phone=hospital['phone'],
        patient_data={'name': 'Test Patient', ...},
        appointment_details={'reason': 'Test'}
    )

# Result: YOUR phone rings 5 times
# No hospitals are bothered
```

---

### Scenario 2: Demo to Your Team

```env
# .env
TEST_PHONE_NUMBER = '+919876543210'  # Colleague's phone
```

```python
# Demo the system
agent.initiate_appointment_call(
    hospital_phone="+911234567890",
    patient_data={'name': 'Demo Patient', ...},
    appointment_details={'reason': 'Demo'}
)

# Result: Colleague's phone rings
# They can hear the AI message
```

---

### Scenario 3: Production Launch

```env
# .env
# TEST_PHONE_NUMBER = '+918087980346'  ← COMMENTED OUT!
```

```python
# Real patient booking
agent.initiate_appointment_call(
    hospital_phone="+911234567890",  # Real hospital
    patient_data={'name': 'John Doe', ...},
    appointment_details={'reason': 'Cardiac consultation'}
)

# Result: Hospital phone rings
# Real appointment booking happens
```

---

## ⚠️ Important Safety Notes

### 1. Always Test First!

```bash
# Before production, test with YOUR phone
TEST_PHONE_NUMBER = '+918087980346'
python make_call.py

# Verify:
# ✓ Your phone rings
# ✓ Message is correct
# ✓ Voice quality is good
```

### 2. Double-Check Before Production

```bash
# Checklist before going live:
# [ ] TEST_PHONE_NUMBER is commented out
# [ ] Tested with real phone number (not hospital)
# [ ] Message sounds professional
# [ ] Twilio account has credits
```

### 3. Use Staging Environment

```bash
# Good practice:
# 1. Development: TEST_PHONE_NUMBER = your phone
# 2. Staging: TEST_PHONE_NUMBER = test phone
# 3. Production: TEST_PHONE_NUMBER commented out
```

---

## 🧪 Testing Checklist

### Before Each Test

- [ ] `TEST_PHONE_NUMBER` is set to YOUR phone
- [ ] Your phone can receive calls
- [ ] Twilio account has credits
- [ ] `.env` file is loaded

### Run Test

```bash
cd Heart-Disease-Prediction-System
python make_call.py
```

### Verify

- [ ] Your phone rang
- [ ] Caller ID showed Twilio number
- [ ] Message was clear
- [ ] No errors in console

---

## 🚀 Production Checklist

### Before Going Live

- [ ] `TEST_PHONE_NUMBER` is commented out
- [ ] Tested with non-hospital number first
- [ ] Message is professional
- [ ] Error handling is in place
- [ ] Twilio account has sufficient credits
- [ ] Backup plan if calls fail

### Deploy

```bash
# 1. Update .env
# TEST_PHONE_NUMBER = '+918087980346'  ← Comment out

# 2. Restart server
python manage.py runserver

# 3. Monitor first few calls
# Check Twilio console: https://console.twilio.com/us1/monitor/logs/calls
```

---

## 💡 Pro Tips

### Tip 1: Use Different Test Numbers

```env
# Development
TEST_PHONE_NUMBER = '+918087980346'  # Your phone

# Staging
# TEST_PHONE_NUMBER = '+919876543210'  # Test phone

# Production
# TEST_PHONE_NUMBER = '+918087980346'  # Commented out
```

### Tip 2: Keep Multiple .env Files

```bash
# Create environment-specific files
cp .env .env.development
cp .env .env.staging
cp .env .env.production

# Use the right one
cp .env.development .env  # For testing
cp .env.production .env   # For production
```

### Tip 3: Add Logging

```python
# In ai_calling_agent.py
import logging

logger = logging.getLogger(__name__)

def initiate_appointment_call(self, hospital_phone, ...):
    test_number = os.getenv('TEST_PHONE_NUMBER')
    if test_number:
        logger.warning(f"TEST MODE: Redirecting call from {hospital_phone} to {test_number}")
        hospital_phone = test_number
    else:
        logger.info(f"PRODUCTION MODE: Calling {hospital_phone}")
    
    # ... rest of code
```

---

## 🎉 Summary

### Testing Mode (Safe)
```env
TEST_PHONE_NUMBER = '+918087980346'  # ← Set
```
- ✅ All calls go to YOUR phone
- ✅ Safe for testing
- ✅ No hospitals bothered
- ❌ Not for production

### Production Mode (Live)
```env
# TEST_PHONE_NUMBER = '+918087980346'  # ← Commented out
```
- ✅ Calls go to real hospitals
- ✅ Ready for production
- ❌ Not for testing
- ⚠️ Use with caution

**Always test first, then go live!** 🚀
