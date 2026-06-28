from groq import __name
import speech_recognition as sr
import logging

from config import SR_TIMEOUT, SR_PHRASE_TIME_LIMIT, SR_ENERGY

logger=logging.getLogger(__name__)

def listen_from_mic() -> tuple[str,str]:
    """
    tuple is used here because the the UI will need 
    to know what is the exact reason of the issue
    suppose no words , mic issue ,so like that we can
    get the exact issue of the problem.
    """
    recognizer=sr.Recognizer()
    recognizer.energy_threshold=SR_ENERGY
    recognizer.dynamic_energy_threshold=True

    try:
        with sr.Microphone() as source:
            logger.info("Adjusting for ambiance noise..")
            recognizer.adjust_for_ambient_noise(source,duration=1)

            logger.info("Listening for the voice input..")
            audio=recognizer.listen(\
                source,
                timeout=SR_TIMEOUT,
                phrase_time_limit=SR_PHRASE_TIME_LIMIT
                )

            #This sound sends audio to the google sever and waits

            text=recognizer.recognize_google(audio)
            logger.info(f"Voice recognized : '{text}'")
            return text, "success"

    except sr.WaitTimeoutError:
        logger.warning("Voice input time out -no speech detected.")
        return "","No speech detected . please try again.."

    except sr.UnknownValueError:
        logger.warning("Voice input - could not understand..")
        return "","could not understand what you said  so plese try again"
    
    except sr.RequestError as e:
        logger.error(f"Speech API request error: {e}")
        return "","The service is unavailable.. please try again"

    except OSError as e:
        # This fires when no microphone is found on the system
        logger.error(f"Microphone access error: {e}")
        return "", "No microphone detected. Please check your audio settings."

    except Exception as e:
        logger.error(f"Unexpected voice input error: {e}")
        return "", f"Unexpected error: {e}"
