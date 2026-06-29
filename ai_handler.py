import os
import logging
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

from config import(
    GROQ_MODEL,SYSTEM_PROMPT,
    MAX_TOKENS,TEMPERATURE,
    LOG_FILE,LOG_DIR
)

#Logging Setup
os.makedirs(LOG_DIR,exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE,encoding="utf-8"),  
        logging.StreamHandler()
    ]
)

logger=logging.getLogger(__name__)

#load API key

load_dotenv()

# Try .env first (local development), fall back to
# Streamlit Cloud secrets (production deployment)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    try:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    except Exception:
        GROQ_API_KEY = None

if not GROQ_API_KEY:
    raise EnvironmentError(
        "Groq api key not found in .env file or Streamlit secrets"
    )

#initialeze Groq client

client=Groq(api_key=GROQ_API_KEY)

def get_ai_response(
    user_message: str,
    chat_history: list,
    language: str ="English"
) -> str:
    """
    Send a message to Groq and get a response.

    Args:
        user_message:  The user's question or command
        chat_history:  List of {"role": ..., "content": ...} dicts
        language:      Selected language name

    Returns:
        AI response string, or error message
    """
    if not user_message or not user_message.strip():
        return "Please say or type something , Bharath."
    
    try:
        logger.info(f"Query[{language}]:'{user_message[:80]}'")

        #Message comes in the chagpt format
        message=[{"role":"system","content":SYSTEM_PROMPT}]

        #add previous conversation for content
        for entry in chat_history:
            role="user" if entry["role"] =="user" else "assistant"
            message.append({"role":role,"content":entry["content"]})

        #add language instruction
        language_note=(
            f"[Respond in {language}]" if language !="English" else ""    
        )

        full_message=f"{language_note}{user_message}".strip()
        message.append({"role":"user","content":full_message})

        #calling the groq api
        response=client.chat.completions.create(
            model=GROQ_MODEL,
            messages=message,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )
        
        ai_text=response.choices[0].message.content.strip()
        logger.info(f"Response[{language}]:'{ai_text[:80]}'")
        return ai_text
    except Exception as e:
        logger.error(f"Groq api error : {e}")

        error_str=str(e).lower()
        if "rate" in error_str or "429" in error_str:
            return(
                "Bro i have hit my rate limit, can u wait for some time.."
            )
        elif "api" in error_str and "key" in error_str:
            return(
                "There is an issue with my api , can you check the api.."
            )
        else:
            return(
                "I came across an error , can you check you internet connection !"
            )

def test_connection() -> bool:
    """
        Quick test to verify the Groq API key is valid.

    Returns:
        True if connection works, False otherwise

    """

    try:
        response=client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role":"user","content":"Say AutoMoto online."}
            ],
            max_tokens=20
        )
        logger.info("GROQ API CONNECTION TEST : SUCCESS")
        return True
    except Exception as e:
        logger.error(f"Groq API connection test failed : {e}")
        return False

def transcribe_audio(audio_bytes: bytes) -> tuple[str, str]:
    """
    Transcribe raw audio bytes using Groq's Whisper API.
    """
    if not audio_bytes:
        return "", "No audio data received"
    
    try:
        # Send raw bytes directly to Groq Whisper
        response = client.audio.transcriptions.create(
            file=("speech.wav", audio_bytes),
            model="whisper-large-v3",
            response_format="text"
        )
        text = response.strip()
        logger.info(f"Whisper transcription success: '{text[:80]}'")
        return text, "success"
    except Exception as e:
        logger.error(f"Groq Whisper transcription failed: {e}")
        return "", f"Speech translation failed: {e}"