# Setup Guide

## Quick Setup

1. **Copy `.env.example` to `.env`**
   ```bash
   cp .env.example .env
   ```

2. **Add your API keys to `.env`**:
   - Get Gemini API key from: https://makersuite.google.com/app/apikey
   - Get Google Maps API key from: https://console.cloud.google.com/google/maps-apis
   - Get Twilio credentials from: https://console.twilio.com/

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start server**:
   ```bash
   python manage.py runserver
   ```

## Features

- ✅ Heart disease prediction with ML models
- ✅ ECG image analysis
- ✅ Google Maps hospital finder
- ✅ AI-powered appointment booking with Gemini
- ✅ Interactive voice conversations

## Documentation

- `GEMINI_AI_CALLING_GUIDE.md` - AI calling agent documentation
- `ENABLE_AI_CONVERSATION.md` - Setup ngrok for interactive AI
- `.env.example` - Environment variables template

## Support

For issues, check the documentation files or create an issue on GitHub.
