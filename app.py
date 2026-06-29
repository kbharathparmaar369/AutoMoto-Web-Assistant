from groq.types.chat import chat_completion_content_part_text_param
import streamlit as st
import logging
import os

from speech_handler import listen_from_mic,text_to_speech

from config import(
    ASSISTANT_NAME,ASSISTANT_OWNER,
    PAGE_TITLE,LOG_DIR
)

from ai_handler import get_ai_response

#Logging setup
#Reuse te same log file ai_hnadler writes to
os.makedirs(LOG_DIR,exist_ok=True)
logger=logging.getLogger(__name__)

#page config

st.set_page_config(
    page_title=PAGE_TITLE,
    layout="wide"
)

#session state initialization

# this is made to survive the rerun the streamlit , so the history can be saved for that session

def init_session():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history=[]
    if "total_queries" not in st.session_state:
        st.session_state.total_queries=0


#Handle the new question

def handle_query(user_input: str):
    """
    Takes the user's typed question , send
    it to the ai , and store the both question 
    and answer in memory.

    """
    if not user_input or not user_input.strip():
        return
    
    user_input=user_input.strip()

    # STEP 1 : save the user question
    st.session_state.chat_history.append({
        "role":"user",
        "content" : user_input
    })

    #step 2: send to the groq ai and wait for the response
    # we pass chat_history MINUS the message we just added
    #because that message becomes the new "current question"

    with st.spinner(f"{ASSISTANT_NAME} is thinking"):
        response=get_ai_response(
            user_message=user_input,
            chat_history=st.session_state.chat_history[:-1],
            language="English"
        )
    
    #step 3 : save the AI reply
    st.session_state.chat_history.append({
        "role":"assistant",
        "content":response
    })

    st.session_state.total_queries +=1
    logger.info(f"Query #{st.session_state.total_queries}: '{user_input[:50]}'")

def handle_voice_input():
    """
    Triggered when the mic button is pressed.
    """
    with st.spinner("Listening... speak now"):
        text, status=listen_from_mic()
    
    if status!="success":
        st.warning(status)
        return
    
    st.info(f"you said: \"{text}\"")
    handle_query(text)

#Display all the past messages

def render_chat():
    """
    Loops through chat_history and print every message,
    This run every time the page returns ,this is why the 
    the chat_history needs to be in the session_state otherwise
    we have nothing to loop.
    """
    if not st.session_state.chat_history:
        st.write("No message yet. Ask AutoMoto something below.")
        return
    
    for i,entry in enumerate(st.session_state.chat_history):
        if entry["role"]=="user":
            st.write(f"**you**: {entry['content']}")
        else:
            st.write(f"**{ASSISTANT_NAME}**: {entry['content']}")

        is_last_message=(i== len(st.session_state.chat_history)-1)
        if is_last_message:
            render_audio_player(entry["content"])
    
def render_audio_player(text: str):
    """
    Generate and display audio controls for a given text.
    called only for th latest AI response to avoid
    regenerating audio for the entire chat history even rerun.
    """

    filepath, status=text_to_speech(text, lang_code="en")

    if status!="success":
        st.caption(f"Audio unavailable : {status}")
        return

    # this is the palyable audio widget
    st.audio(filepath, format="audio/mp3")

    # show the download button - reads the files as raw bytes
    with open(filepath,"rb") as audio_file:
        audio_bytes=audio_file.read()
    
    st.download_button(
        label="Download audio",
        data=audio_bytes,
        file_name="automoto_response.mp3",
        mime="audio/mp3"
    )
        
# MAIN LOGIC OF THE APP

def main():
    init_session()
    st.title(f"{ASSISTANT_NAME} - AI Assistant")
    st.caption(f"Total quetion asked: {st.session_state.total_queries}")
    st.divider()

    #show the conversation so far

    render_chat()
    st.divider()

    #Input box + button

    col1,col2,col3=st.columns([4,1,1])

    with col1:
        user_text=st.text_input(
            "Ask AutoMoto something",
            label_visibility="collapsed",
            placeholder="Type your question here..."
        )
    
    with col2:
        send_clicked=st.button("Send")
    
    with col3:
        mic_clicked=st.clicked("speak")
    
    if send_clicked and user_text:
        handle_query(user_text)
        st.rerun()
    
    if mic_clicked:
        handle_voice_input()
        st.rerun()

if __name__ =="__main__":
    main()
   
