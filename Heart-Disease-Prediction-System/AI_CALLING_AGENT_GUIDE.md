# AI Calling Agent - Complete Guide

## Which AI Technology Is Used?

The AI calling agent uses **Twilio's built-in AI capabilities**:

### Current Implementation (Basic AI)
1. **Amazon Polly** - Text-to-Speech engine
   - Voice: `Polly.Joanna` (natural female voice)
   - Converts text scripts to natural-sounding speech
   
2. **Twilio Speech Recognition** - Speech-to-Text
   - Converts spoken responses to text
   - Automatic speech timeout detection
   
3. **Rule-Based Conversation Flow** - Programmed logic
   - Predefined conversation stages
   - Structured appointment booking flow
   
4. **Machine Detection** - Answering machine detection
   - Detects if call is answered by human or voicemail

### What It's NOT Using
- ❌ ChatGPT or GPT models
- ❌ Advanced Large Language Models (LLMs)
- ❌ Natural Language Understanding (NLU)
- ❌ Dynamic conversation generation

### Upgrade Options (Advanced AI)
To make it more intelligent, you could integrate:

1. **OpenAI GPT-4** - Dynamic, context-aware responses
2. **Google Dialogflow** - Natural conversation understanding
3. **Azure Cognitive Services** - Advanced speech processing
4. **Anthropic Claude** - Conversational AI

---

## Code Verification

### ✅ Your Code is CORRECT

Your implementation follows Twilio's official patterns:

```python
# Official Twilio Pattern (from docs)
call = client.calls.create(
    twiml="<Response><Say>Ahoy, World</Say></Response>",
    to="+14155551212",
    from_="+15017122661",
)

# Your Implementation (matches official pattern)
call = self.client.calls.create(
    twiml=twiml,
    to=hospital_phone,
    from_=self.phone_number,
    status_callback=callback_url,
    record=True,
    machine_detection='DetectMessageEnd',
)
```

### Key Differences (All Valid)
1. **TwiML**: You use dynamic TwiML generation (better for complex calls)
2. **Callbacks**: You added status callbacks (good for tracking)
3. **Recording**: You enabled call recording (good for quality assurance)
4. **Machine Detection**: You detect answering machines (smart!)

---

## Testing Your Implementation

### Test 1: Simple Call (Verify Twilio Works)
```bash
cd Heart-Disease-Prediction-System
python make_call.py
```

This will:
- Make a simple "Ahoy, World" call to your test number
- Verify your Twilio credentials work
- Confirm phone numbers are correct

### Test 2: Full Test Suite
```bash
python test_appointment_call.py
```

This runs 3 tests:
1. Simple call test
2. Appointment booking call
3. SMS confirmation

### Test 3: From Django App
```python
from health.ai_calling_agent import create_simple_booking_call

result = create_simple_booking_call(
    hospital_phone="+918087980346",
    patient_name="John Doe",
    patient_contact="+918087980346",
    reason="Cardiac consultation - ECG abnormal"
)

print(result)
```

---

## Environment Variables Required

Make sure your `.env` file has:

```env
# Twilio Credentials (from twilio.com/console)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890

# Test number (your phone for testing)
TEST_PHONE_NUMBER=+918087980346
```

---

## Phone Number Format (IMPORTANT!)

All phone numbers MUST be in **E.164 format**:

✅ Correct:
- `+918087980346` (India)
- `+14155551212` (USA)
- `+442071234567` (UK)

❌ Wrong:
- `8087980346` (missing country code)
- `+91 808 798 0346` (spaces not allowed)
- `08087980346` (leading zero)

---

## How It Works

### Step 1: Initiate Call
```python
agent = AICallingAgent()
call_sid = agent.initiate_appointment_call(
    hospital_phone="+911234567890",
    patient_data={'name': 'John', 'contact': '+918087980346'},
    appointment_details={'reason': 'Cardiac consultation'}
)
```

### Step 2: Twilio Makes Call
- Dials the hospital number
- Plays AI-generated message using Amazon Polly
- Records the conversation

### Step 3: AI Speaks
```
"Hello, this is an automated appointment booking assistant 
calling on behalf of John Doe. I'm calling to schedule a 
cardiac consultation appointment. The patient recently had 
an ECG analysis showing concerning results..."
```

### Step 4: Confirmation SMS
```python
agent.send_sms_confirmation(
    patient_phone="+918087980346",
    appointment_details={...}
)
```

---

## Conversation Flow

```
┌─────────────────────────────────────┐
│  1. Call Initiated                  │
│     - Dial hospital number          │
│     - Detect if human/machine       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  2. Greeting Stage                  │
│     - "Hello, this is..."           │
│     - Wait for response             │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  3. Provide Details                 │
│     - Patient name                  │
│     - Reason for visit              │
│     - Preferred date/time           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  4. Confirm Appointment             │
│     - Thank you message             │
│     - Hang up                       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  5. Send SMS to Patient             │
│     - Confirmation details          │
│     - Hospital contact              │
└─────────────────────────────────────┘
```

---

## Upgrading to Advanced AI

### Option 1: Add OpenAI GPT
```python
import openai

def generate_dynamic_response(conversation_history):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a medical appointment booking assistant"},
            {"role": "user", "content": conversation_history}
        ]
    )
    return response.choices[0].message.content
```

### Option 2: Add Google Dialogflow
```python
from google.cloud import dialogflow

def detect_intent(text, session_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    
    text_input = dialogflow.TextInput(text=text, language_code='en')
    query_input = dialogflow.QueryInput(text=text_input)
    
    response = session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result
```

---

## Troubleshooting

### Error: "Unable to create record"
- Check your Twilio account has credits
- Verify phone numbers are in E.164 format
- Ensure your Twilio number can make calls to your country

### Error: "Invalid credentials"
- Double-check TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
- Make sure there are no extra spaces in .env file
- Verify credentials at twilio.com/console

### Call Not Received
- Check TEST_PHONE_NUMBER is correct
- Verify your phone can receive calls
- Check Twilio call logs at twilio.com/console/voice/logs

### TwiML Error
- Validate TwiML syntax
- Check voice name is correct (Polly.Joanna)
- Ensure language code is valid (en-US)

---

## Cost Estimation

Twilio pricing (approximate):
- Outbound call: $0.013/min (India)
- SMS: $0.0075/message
- Recording: $0.0025/min

Example: 100 appointments/month
- Calls (2 min avg): 100 × 2 × $0.013 = $2.60
- SMS: 100 × $0.0075 = $0.75
- Recording: 100 × 2 × $0.0025 = $0.50
- **Total: ~$4/month**

---

## Next Steps

1. **Test the basic call**: Run `python make_call.py`
2. **Test full suite**: Run `python test_appointment_call.py`
3. **Integrate with Django**: Use in your views
4. **Monitor calls**: Check Twilio console for logs
5. **Upgrade AI**: Add GPT-4 or Dialogflow if needed

---

## Summary

✅ Your code is correct and follows Twilio's official patterns
✅ Uses Twilio's built-in AI (Polly TTS + Speech Recognition)
✅ Not using ChatGPT/LLMs (but you can add them)
✅ Ready for testing and production use

The implementation is solid for basic appointment booking. For more intelligent conversations, consider adding OpenAI GPT or Google Dialogflow.
