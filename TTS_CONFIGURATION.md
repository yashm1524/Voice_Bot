# TTS Configuration Guide

This guide explains how to configure different Text-to-Speech (TTS) providers for the voice bot.

## Overview

The voice bot supports multiple TTS providers with automatic fallback:
1. **Azure Text-to-Speech** (Highest quality neural voices)
2. **Google Cloud Text-to-Speech** (High quality neural voices)
3. **OpenAI TTS** (Fast and natural)
4. **gTTS** (Free fallback, always available)

## Configuration

### 1. OpenAI TTS (Recommended - Easiest Setup)

**Pros:**
- Easy to set up (same API key as GPT)
- Natural-sounding voices
- Fast response times
- Multiple voice options

**Setup:**
1. Get your OpenAI API key from https://platform.openai.com/api-keys
2. Add to `.env` file:
   ```env
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
   ```

**Voice Options:**
- `alloy` - Neutral and balanced
- `echo` - Male voice
- `fable` - British accent
- `onyx` - Deep male voice
- `nova` - Female voice
- `shimmer` - Soft female voice

To change voice, edit `services/tts.py` line with `voice="alloy"`.

---

### 2. Google Cloud Text-to-Speech (High Quality)

**Pros:**
- Excellent neural voices (Neural2)
- Wide language support
- Very natural sounding
- Free tier: 1 million characters/month

**Setup:**

1. **Create Google Cloud Project**
   - Go to https://console.cloud.google.com/
   - Create a new project or select existing one

2. **Enable Text-to-Speech API**
   - Navigate to "APIs & Services" > "Library"
   - Search for "Cloud Text-to-Speech API"
   - Click "Enable"

3. **Create Service Account**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in details and create
   - Click on the created service account
   - Go to "Keys" tab > "Add Key" > "Create new key"
   - Choose JSON format and download

4. **Configure Environment**
   - Save the JSON file to a secure location
   - Add to `.env` file:
     ```env
     GOOGLE_APPLICATION_CREDENTIALS=C:/path/to/your/credentials.json
     ```

5. **Install Python Package**
   ```bash
   pip install google-cloud-texttospeech
   ```

**Available Voices:**
- `en-US-Neural2-F` - Female (default in code)
- `en-US-Neural2-M` - Male
- `en-US-Neural2-A` - Neutral
- Many more at https://cloud.google.com/text-to-speech/docs/voices

---

### 3. Microsoft Azure Text-to-Speech (Premium Quality)

**Pros:**
- Premium neural voices
- Excellent prosody and emotion
- SSML support for fine control
- Free tier: 500,000 characters/month

**Setup:**

1. **Create Azure Account**
   - Go to https://azure.microsoft.com/
   - Sign up for free account (requires credit card but won't charge without upgrade)

2. **Create Speech Resource**
   - Go to Azure Portal: https://portal.azure.com/
   - Click "Create a resource"
   - Search for "Speech"
   - Click "Create" on "Speech Services"
   - Fill in:
     - Subscription: Your subscription
     - Resource group: Create new or use existing
     - Region: Choose closest (e.g., "East US")
     - Name: Your resource name
     - Pricing tier: Free F0 (for testing)
   - Click "Review + create" then "Create"

3. **Get API Keys**
   - Go to your Speech resource
   - Click "Keys and Endpoint" in left menu
   - Copy "KEY 1" and "Location/Region"

4. **Configure Environment**
   Add to `.env` file:
   ```env
   AZURE_SPEECH_KEY=your_key_here
   AZURE_SPEECH_REGION=eastus
   ```

5. **Install Python Package**
   ```bash
   pip install azure-cognitiveservices-speech
   ```

**Available Voices:**
- `en-US-JennyNeural` - Female, friendly (default in code)
- `en-US-GuyNeural` - Male, professional
- `en-US-AriaNeural` - Female, news anchor style
- `en-US-DavisNeural` - Male, conversational
- Many more at https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support

---

### 4. gTTS (Free Fallback)

**Pros:**
- Completely free
- No API keys needed
- Always available
- No setup required

**Cons:**
- Lower quality than neural voices
- Robotic sound
- Limited customization

**Setup:**
Already included in requirements.txt, no configuration needed!

---

## Testing TTS Services

### Test OpenAI TTS
```python
from services.tts import text_to_speech_openai
result = text_to_speech_openai("Hello, this is a test of OpenAI TTS")
print(f"Audio saved to: {result}")
```

### Test Google Cloud TTS
```python
from services.tts import text_to_speech_google_cloud
result = text_to_speech_google_cloud("Hello, this is a test of Google Cloud TTS")
print(f"Audio saved to: {result}")
```

### Test Azure TTS
```python
from services.tts import text_to_speech_azure
result = text_to_speech_azure("Hello, this is a test of Azure TTS")
print(f"Audio saved to: {result}")
```

### Test Auto Mode (tries all available services)
```python
from services.tts import text_to_speech
result = text_to_speech("Hello, this is a test with automatic fallback")
print(f"Audio saved to: {result}")
```

---

## Service Priority

When using `text_to_speech(text, preferred_service="auto")`, the system tries services in this order:

1. **Azure TTS** (if `AZURE_SPEECH_KEY` is set)
2. **Google Cloud TTS** (if `GOOGLE_APPLICATION_CREDENTIALS` is set)
3. **OpenAI TTS** (if `OPENAI_API_KEY` is set)
4. **gTTS** (always available as final fallback)

---

## Forcing a Specific Service

You can force a specific TTS service in `main.py`:

```python
# In main.py, find the text_to_speech call and modify:

# Force OpenAI
audio_path = text_to_speech(bot_response_text, preferred_service="openai")

# Force Google Cloud
audio_path = text_to_speech(bot_response_text, preferred_service="google")

# Force Azure
audio_path = text_to_speech(bot_response_text, preferred_service="azure")

# Force gTTS
audio_path = text_to_speech(bot_response_text, preferred_service="gtts")

# Auto (default - tries all available)
audio_path = text_to_speech(bot_response_text, preferred_service="auto")
```

---

## Cost Comparison

| Service | Free Tier | Paid Pricing | Quality |
|---------|-----------|--------------|---------|
| **gTTS** | Unlimited | Free | Basic |
| **OpenAI** | None | $15/1M chars | High |
| **Google Cloud** | 1M chars/month | $4/1M chars | Very High |
| **Azure** | 500K chars/month | $16/1M chars | Premium |

**Recommendation for Development:** Use OpenAI (if you already have API key) or gTTS (free)

**Recommendation for Production:** Use Azure or Google Cloud for best quality

---

## Troubleshooting

### OpenAI TTS not working
- Check API key is valid
- Ensure you have credits in your OpenAI account
- Check error messages in console

### Google Cloud TTS not working
- Verify credentials file path is correct
- Ensure Text-to-Speech API is enabled in GCP
- Check service account has proper permissions
- Install package: `pip install google-cloud-texttospeech`

### Azure TTS not working
- Verify API key and region are correct
- Check Azure resource is active
- Ensure you haven't exceeded free tier limits
- Install package: `pip install azure-cognitiveservices-speech`

### All services failing
- gTTS should always work as fallback
- Check internet connection
- Check console for specific error messages

---

## Example .env File

```env
# OpenAI (for GPT, Whisper, and TTS)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# Google Cloud TTS (optional)
GOOGLE_APPLICATION_CREDENTIALS=C:/path/to/google-credentials.json

# Azure TTS (optional)
AZURE_SPEECH_KEY=your_azure_key_here
AZURE_SPEECH_REGION=eastus
```

---

## Voice Quality Comparison

Listen to samples from each service to choose your preference:

1. **Azure**: Most natural, best for professional applications
2. **Google Cloud**: Very natural, excellent for customer service
3. **OpenAI**: Natural and fast, good balance
4. **gTTS**: Robotic but functional, good for testing

---

## Next Steps

1. Choose your preferred TTS service
2. Follow the setup instructions above
3. Test the service using the test code
4. Update `main.py` if you want to force a specific service
5. Deploy and enjoy high-quality voice responses!
