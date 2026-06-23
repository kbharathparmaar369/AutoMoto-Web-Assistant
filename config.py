import os

ASSISTANT_NAME="AutoMoto"
ASSISTANT_OWNER="Bharath Parmar"

GROQ_MODEL="llama-3.3-70b-versatile"
MAX_TOKENS=2048
TEMPERATURE=0.7

SYSTEM_PROMPT = f"""You are {ASSISTANT_NAME}, an intelligent personal AI assistant 
created by {ASSISTANT_OWNER}. You are inspired by JARVIS from Iron Man — helpful, 
articulate, slightly witty, and always professional.

Guidelines:
- Always address the user as {ASSISTANT_OWNER}
- Keep responses clear and concise
- Always respond in the language the user writes or speaks in
- Never say you are LLaMA or mention Groq/Meta — you are {ASSISTANT_NAME}
- If asked who made you, say you were built by {ASSISTANT_OWNER}
"""

SUPPORTED_LANGUAGES={
    "English"   : ("en", "en-US"),
    "Hindi"     : ("hi", "hi-IN"),
    "Tamil"     : ("ta", "ta-IN"),
    "Telugu"    : ("te", "te-IN"),
    "French"    : ("fr", "fr-FR"),
    "Spanish"   : ("es", "es-ES"),
    "German"    : ("de", "de-DE"),
    "Japanese"  : ("ja", "ja-JP"),
}

DEFAULT_LANGUAGE="English"

PAGE_TITLE=f"{ASSISTANT_NAME} - AI Web Assistant"
LAYOUT="wide"

#speech Recognition settings

SR_TIMEOUT=5
SR_PHRASE_TIME_LIMIT=10
SR_ENERGY_ENERGY=300

#AUDIO OUTPUT SETTINGS

AUDIO_FILE="speech.mp3"
AUDIO_SLOW=False

#Logging

LOG_DIR="logs"
LOG_FILE=os.path.join(LOG_DIR,"application.log")
