# Enable Full AI Conversation (Gemini Integration)

## Current Status

✅ **Basic Calling Works**: The AI can call and leave a message with patient details
❌ **Interactive Conversation**: Requires public URL (not available in local development)

## Why Interactive Conversation Doesn't Work Locally

Twilio needs to send speech recognition results back to your server. This requires:
- A **public URL** that Twilio can reach
- Your local `localhost:8000` is not accessible from the internet

## Solution: Use ngrok (Free & Easy)

### Step 1: Install ngrok

**Windows:**
```bash
# Download from: https://ngrok.com/download
# Or use chocolatey:
choco install ngrok
```

**Mac/Linux:**
```bash
brew install ngrok
# Or download from: https://ngrok.com/download
```

### Step 2: Start ngrok

```bash
# In a new terminal, run:
ngrok http 8000
```

You'll see output like:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

### Step 3: Update Django Settings

Add to `Heart-Disease-Prediction-System/health_desease/settings.py`:

```python
# Add at the bottom of settings.py
BASE_URL = 'https://abc123.ngrok.io'  # Replace with your ngrok URL
```

### Step 4: Update Allowed Hosts

In `settings.py`, update:

```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'abc123.ngrok.io']  # Add your ngrok domain
```

### Step 5: Restart Django Server

```bash
python manage.py runserver
```

### Step 6: Test AI Conversation

1. Go to Find Doctors page
2. Click "Book Appointment" → "Let AI Agent Call & Book"
3. Answer your test phone
4. **Have a conversation!** The AI will now:
   - Listen to your responses
   - Use Gemini to generate intelligent replies
   - Answer questions naturally
   - Adapt to the conversation

## Example Conversation with Full AI

```
AI: "Hello, this is an automated appointment booking assistant 
     calling on behalf of John Doe. I'm calling to schedule a 
     cardiac consultation appointment. Am I speaking with the 
     appointment desk?"

You: "Yes, this is the appointment desk. What's the patient's name?"

AI: [Gemini generates response]
    "The patient's name is John Doe. They recently had an ECG 
     analysis showing concerning cardiac results and need a 
     consultation as soon as possible."

You: "What's their contact number?"

AI: [Gemini generates response]
    "The patient's contact number is +918087980346. They're 
     available for morning appointments if possible."

You: "We have an opening tomorrow at 10 AM."

AI: [Gemini generates response]
    "Perfect! That works well. I'll confirm those details with 
     the patient. Thank you for your assistance!"
```

## Without ngrok (Current Behavior)

The AI will call and leave a complete message:

```
AI: "Hello, this is an automated appointment booking assistant 
     calling on behalf of John Doe. I'm calling to schedule a 
     cardiac consultation appointment. The patient recently had 
     an ECG analysis showing concerning cardiac results. The 
     patient's contact number is +918087980346. Please call back 
     at your earliest convenience to schedule the appointment. 
     Thank you for your time and assistance. Goodbye."
```

This still works and provides all necessary information!

## Alternative: Deploy to Production

For production use without ngrok:

### Option 1: Render.com (Free)
```bash
# Already configured in render.yaml
git push origin main
# Deploy on Render.com
```

### Option 2: Heroku
```bash
heroku create your-app-name
git push heroku main
```

### Option 3: Railway.app
```bash
railway init
railway up
```

Once deployed, update `BASE_URL` in settings to your production URL.

## Troubleshooting

### ngrok URL Changes
- Free ngrok URLs change each time you restart
- Update `BASE_URL` in settings.py each time
- Or upgrade to ngrok paid plan for static URL

### Call Still Not Interactive
1. Check ngrok is running: `ngrok http 8000`
2. Check `BASE_URL` matches ngrok URL exactly
3. Check `ALLOWED_HOSTS` includes ngrok domain
4. Restart Django server after changes
5. Check Django console for errors

### Gemini Not Responding
1. Check `GEMINI_API_KEY` in .env
2. Check `google-generativeai` is installed
3. Check Django console for Gemini errors
4. Verify API key at: https://makersuite.google.com/app/apikey

## Cost Comparison

### With ngrok (Interactive AI)
- **Twilio**: ~$0.15 per 2-minute call
- **Gemini**: ~$0.0001 per call
- **ngrok**: Free (or $8/month for static URL)

### Without ngrok (Message Only)
- **Twilio**: ~$0.05 per 30-second message
- **Gemini**: Not used
- **ngrok**: Not needed

## Recommendation

**For Development/Testing**: 
- Use current setup (message-only) - it works fine!
- Or use ngrok for testing interactive AI

**For Production**:
- Deploy to Render/Heroku/Railway
- Enable full interactive AI conversation
- Much better user experience

## Next Steps

1. ✅ Test current setup (message-only) - works now!
2. 🔄 Install ngrok if you want interactive AI
3. 🚀 Deploy to production for best experience
