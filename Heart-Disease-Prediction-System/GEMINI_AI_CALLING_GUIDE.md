# Gemini AI-Powered Calling Agent

## Overview

The AI calling agent now uses **Google Gemini 2.5 Flash** for intelligent, natural conversations with hospital staff. The AI can understand questions, provide relevant information, and adapt responses based on the conversation context.

## Features

### 🤖 Intelligent Conversation
- **Natural Language Understanding**: Understands various ways hospital staff might respond
- **Context-Aware Responses**: Remembers conversation history and responds appropriately
- **Question Handling**: Can answer questions about patient details, urgency, medical history
- **Adaptive Dialogue**: Adjusts conversation flow based on staff responses

### 💬 What the AI Can Do

1. **Introduce itself professionally**
   - Identifies as an automated booking assistant
   - States the purpose clearly
   - Asks to speak with appointment desk

2. **Provide patient information when asked**
   - Patient name and contact number
   - Reason for visit (cardiac consultation)
   - Medical urgency (ECG results)
   - Preferred appointment times

3. **Handle common questions**
   - "What's the patient's name?" → Provides name
   - "Why do they need an appointment?" → Explains ECG results
   - "Is this urgent?" → Mentions concerning cardiac results
   - "Can the patient call directly?" → Provides contact number
   - "What dates work?" → Mentions "as soon as possible"

4. **Adapt to responses**
   - If transferred, politely waits
   - If asked to call back, thanks and ends call
   - If given appointment, confirms details
   - If no answer, tries again later

## How It Works

### Architecture

```
Patient clicks "Book Appointment"
    ↓
Django initiates Twilio call
    ↓
Twilio calls hospital
    ↓
AI speaks initial greeting
    ↓
Hospital staff responds (speech-to-text)
    ↓
Gemini AI generates intelligent response
    ↓
Response converted to speech (text-to-speech)
    ↓
Conversation continues until complete
```

### Conversation Flow

```
AI: "Hello, this is an automated appointment booking assistant 
     calling on behalf of [Patient Name]. I'm calling to schedule 
     a cardiac consultation appointment. Am I speaking with the 
     appointment desk?"

Staff: "Yes, this is the appointment desk."

AI: [Gemini generates response based on context]
    "Great! I need to book an appointment for [Patient Name]. 
     The patient recently had an ECG analysis showing concerning 
     cardiac results. What dates are available?"

Staff: "What's the patient's contact number?"

AI: [Gemini understands question and provides info]
    "The patient's contact number is [Phone]. They're available 
     for morning appointments if possible."

... conversation continues naturally ...
```

## Configuration

### Required Environment Variables

```bash
# Gemini AI (for intelligent conversation)
GEMINI_API_KEY='AIzaSy...'

# Twilio (for phone calls)
TWILIO_ACCOUNT_SID='AC...'
TWILIO_AUTH_TOKEN='...'
TWILIO_PHONE_NUMBER='+1...'

# Testing (optional - calls go here during development)
TEST_PHONE_NUMBER='+91...'
```

### Gemini Model

Currently using: `gemini-2.0-flash-exp`
- Fast response times (< 1 second)
- Natural conversation abilities
- Context understanding
- Cost-effective

## Testing

### Test the AI Calling

1. **Set test phone number** in `.env`:
   ```bash
   TEST_PHONE_NUMBER='+918087980346'
   ```

2. **Make a test booking**:
   - Go to Find Doctors page
   - Click "Book Appointment" on any hospital
   - Choose "Let AI Agent Call & Book"
   - Your test phone will ring

3. **Have a conversation**:
   - Answer the call
   - Respond naturally to the AI
   - Ask questions like:
     - "What's the patient's name?"
     - "Why do they need an appointment?"
     - "Can they call directly?"
   - The AI will respond intelligently

### Example Test Conversation

```
AI: "Hello, this is an automated appointment booking assistant..."

You: "Yes, this is the appointment desk."

AI: "Great! I need to book an appointment for John Doe. The patient 
     recently had an ECG analysis showing concerning cardiac results. 
     What dates are available?"

You: "What's the patient's contact number?"

AI: "The patient's contact number is +918087980346. They're available 
     for morning appointments if possible."

You: "We have an opening tomorrow at 10 AM."

AI: "Perfect! I'll confirm those details with the patient. They will 
     call back to verify if needed. Thank you for your assistance!"
```

## Debugging

### Check Django Console

The system logs all AI interactions:

```
DEBUG: AI Call Handler - Stage: conversation, CallSid: CA123...
DEBUG: Speech Result: What's the patient's name?
DEBUG: Gemini AI generating response...
DEBUG: Generated TwiML: <Response><Say>The patient's name is...</Say>...
```

### Check Twilio Console

1. Go to: https://console.twilio.com/
2. Click "Monitor" → "Logs" → "Calls"
3. Find your call by phone number
4. View call details, recordings, and transcripts

### Common Issues

**Issue**: AI doesn't respond intelligently
- **Fix**: Check `GEMINI_API_KEY` is set correctly
- **Fix**: Ensure `google-generativeai` is installed

**Issue**: Call connects but no speech
- **Fix**: Check Twilio phone number is verified
- **Fix**: Ensure speech recognition is enabled in Twilio

**Issue**: AI repeats same response
- **Fix**: Check conversation history is being stored
- **Fix**: Verify call_sid is being passed correctly

## Cost Estimation

### Gemini AI
- **Model**: gemini-2.0-flash-exp
- **Cost**: ~$0.00001 per request
- **Per Call**: ~$0.0001 (10 exchanges)

### Twilio
- **Outbound Call**: ~$0.013/minute
- **Speech Recognition**: ~$0.02/minute
- **Text-to-Speech**: ~$0.04/minute
- **Per Call**: ~$0.15 (2-minute call)

**Total per call**: ~$0.15

## Production Deployment

### Before Going Live

1. **Remove TEST_PHONE_NUMBER** from `.env`
2. **Verify Twilio account** is upgraded (not trial)
3. **Test with real hospital numbers** (with permission)
4. **Set up call recording** for quality assurance
5. **Monitor costs** in Twilio console

### Best Practices

- Always identify as automated system
- Provide patient contact for callback
- Keep conversations concise (< 2 minutes)
- Record calls for quality assurance
- Have fallback to manual calling
- Monitor AI responses for accuracy

## Future Enhancements

- [ ] Multi-language support (Hindi, regional languages)
- [ ] Appointment confirmation via SMS
- [ ] Integration with hospital booking systems
- [ ] Voice emotion detection
- [ ] Automatic rescheduling
- [ ] Call analytics dashboard

## Support

For issues or questions:
1. Check Django console logs
2. Check Twilio call logs
3. Review Gemini API usage
4. Test with `TEST_PHONE_NUMBER` first
