# SMS & WhatsApp Notifications Guide

## 🎉 New Feature Added!

After the AI calling agent completes a call, the system now automatically sends:
- ✅ **SMS notification** with appointment details
- ✅ **WhatsApp message** with appointment details

Both are sent to the `TEST_PHONE_NUMBER` in your `.env` file.

## 📱 What Gets Sent

### SMS Message
```
🏥 Appointment Booking Confirmation

Hospital: [Hospital Name]
Address: [Hospital Address]
Phone: [Hospital Phone]

Date: To be confirmed by hospital
Time: To be confirmed by hospital

Status: AI call completed - Awaiting hospital confirmation

Please call the hospital to confirm your appointment.

- Heart Disease Prediction System
```

### WhatsApp Message
Same content but with WhatsApp formatting (bold text, emojis).

## 🔧 Setup

### SMS (Already Works!)
SMS will work automatically with your existing Twilio credentials. No additional setup needed!

### WhatsApp (Requires Sandbox Setup)

1. **Go to Your WhatsApp API Sandbox**:
   Check your voice/SMS provider's WhatsApp sandbox documentation

2. **Join the Sandbox**:
   - You'll see a WhatsApp number
   - You'll see a join code
   - Send that message to the WhatsApp number from your phone

3. **Test**:
   - Once you send the join code, you're connected!
   - WhatsApp notifications will now work automatically

## 🧪 How to Test

### Test SMS
1. Make sure your SMS API credentials are valid
2. Click "Book Appointment" → "Let AI Agent Call & Book"
3. The AI will call (or try to call)
4. When the call completes, you'll receive an SMS

### Test WhatsApp
1. Complete WhatsApp sandbox setup (see above)
2. Click "Book Appointment" → "Let AI Agent Call & Book"
3. When the call completes, you'll receive both SMS and WhatsApp

## 📊 What Happens

### Call Flow
```
1. User clicks "Let AI Agent Call & Book"
   ↓
2. AI calls hospital (or test number)
   ↓
3. Call completes (status: 'completed')
   ↓
4. System automatically sends:
   - SMS to TEST_PHONE_NUMBER
   - WhatsApp to TEST_PHONE_NUMBER
   ↓
5. Patient receives both notifications!
```

### Notification Details Include
- ✅ Hospital name
- ✅ Hospital address
- ✅ Hospital phone number
- ✅ Call duration
- ✅ Status message
- ✅ Next steps

## 🔍 Debugging

### Check Django Console
After a call completes, you'll see:
```
============================================================
📞 CALL STATUS UPDATE
============================================================
Call SID: CA123...
Status: completed
Duration: 45 seconds

✅ Call completed! Sending notifications...

📱 Sending appointment notifications to [TEST_PHONE_NUMBER]
   Hospital: [Hospital Name]

✅ SMS sent successfully! SID: SM123...
✅ WhatsApp sent successfully! SID: SM456...
```

### Common Issues

**SMS not sending:**
- Check SMS API credentials are valid
- Check TEST_PHONE_NUMBER is in E.164 format (e.g., +1234567890)
- Check your SMS provider account has credit

**WhatsApp not sending:**
- Check you've joined the WhatsApp sandbox
- Check the error message in console
- WhatsApp requires sandbox setup (see above)

## 💡 Production Notes

### For Production Use:

1. **SMS**: Works out of the box with paid SMS provider account

2. **WhatsApp**: 
   - Sandbox is for testing only
   - For production, you need:
     - WhatsApp Business API approval
     - Facebook Business Manager account
     - WhatsApp Business Profile
   - Check your provider's WhatsApp Business API documentation

3. **Phone Numbers**:
   - In production, use actual patient phone numbers
   - Remove TEST_PHONE_NUMBER override
   - Store phone numbers in database

## 🎯 Features

- ✅ Automatic SMS after call completes
- ✅ Automatic WhatsApp after call completes
- ✅ Rich formatting with emojis
- ✅ All appointment details included
- ✅ Error handling and logging
- ✅ Works with test phone number
- ✅ Easy to extend for more notifications

## 📝 Customization

To customize the message content, edit:
- `Heart-Disease-Prediction-System/health/ai_calling_agent.py`
- Functions: `send_sms_confirmation()` and `send_whatsapp_confirmation()`

## 🚀 Next Steps

1. Configure your SMS/Voice API credentials (if needed)
2. Test SMS notifications
3. Setup WhatsApp sandbox
4. Test WhatsApp notifications
5. Enjoy automated notifications!

---

**Last Updated**: November 10, 2025
**Status**: ✅ READY TO USE
