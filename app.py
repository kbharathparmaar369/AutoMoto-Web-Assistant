from config import DEFAULT_LANGUAGE
from groq.types.chat import chat_completion_content_part_text_param
import streamlit as st
import logging
import os
from streamlit_mic_recorder import mic_recorder

from speech_handler import listen_from_mic, text_to_speech, recognize_audio

from config import(
    ASSISTANT_NAME,ASSISTANT_OWNER,SUPPORTED_LANGUAGES,DEFAULT_LANGUAGE,
    PAGE_TITLE,LOG_DIR
)
from ai_handler import get_ai_response, test_connection, transcribe_audio

#Logging setup
#Reuse te same log file ai_hnadler writes to
os.makedirs(LOG_DIR,exist_ok=True)
logger=logging.getLogger(__name__)

#page config

st.set_page_config(
    page_title=PAGE_TITLE,
    layout="wide",
    initial_sidebar_state="expanded"
)

# custom css
st.markdown("""<style>
    .stApp{
        background: linear-gradient(135deg, #0a0a1a 0%, #071524 100%);
    }
    [data-testid="stSidebar"]{
        background-color: linear-gradient(180deg, #050f1a 0%, #071524 100%);
        border-right: 1px solid rgba(0,212,255,0.2);
        }
    .user-msg{
        background: rgba(0,212,255,0.1);
        border: 1px solid rgba(0,212,255,0.25);
        border-radius: 12px 4px 12px;
        padding: 14px 18px;
        margin: 10px 0;
        color: #c8e8f5;
        font-size: 15x;
    
    }

    .bot-msg{
        background: rgba(225,201,64,0.06);
        border: 1px solid rgba(225,201,64,0.3);
        border-radius: 12px 4px 12px;
        padding:14px 18px;
        color: #fff; 
        font-size: 15px;
        line-height: 1.6;
    }

    .msg-label{
    
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
    }
    .user-label { color: rgba(0, 212, 255, 0.7); }
    .bot-label  { color: rgba(255, 201, 64, 0.7); }
    .main-title {
        font-size: 32px;
        font-weight: 900;
        letter-spacing: 3px;
        background: linear-gradient(135deg, #ffffff, #00d4ff, #ffc940);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 4px;
    }
    .stTextInput input {
        background: rgba(0, 212, 255, 0.05) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 8px !important;
        color: #c8e8f5 !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #00d4ff22, #00d4ff11);
        border: 1px solid rgba(0, 212, 255, 0.4);
        color: #00d4ff;
        border-radius: 8px;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.2s;
    }
    .stButton button:hover {
        background: rgba(0, 212, 255, 0.2);
        border-color: rgba(0, 212, 255, 0.8);
    }
    hr { border-color: rgba(0, 212, 255, 0.15) !important; }
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    header    { visibility: hidden; }

    }

     </style>""", unsafe_allow_html=True)

#session state initialization

# this is made to survive the rerun the streamlit , so the history can be saved for that session

def init_session():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history=[]
    if "language" not in st.session_state:
        st.session_state.language=DEFAULT_LANGUAGE
    if "total_queries" not in st.session_state:
        st.session_state.total_queries=0
    if "api_status" not in st.session_state:
        st.session_state.api_status="None"
    if "last_audio" not in st.session_state:
        st.session_state.last_audio = None


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

def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
<div style="text-align:center; margin-bottom:24px;">
    <div style='font-size:40px'>🤖</div>
    <div style='font-size:18px;font-weight:700; color:#00d4ff; letter-spacing:3px;'>{ASSISTANT_NAME}</div>
    <div style='font-size: 11px; color:#4a7a99; letter-spacing:2px; margin-top:4px;'>AI WEB ASSISTANT</div>
</div>
""",unsafe_allow_html=True)

        st.divider()

        st.markdown("**🌏 Language**")
        selected_language=st.selectbox(
            label="select language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.language),
            label_visibility="collapsed",
            
            
        )
        st.session_state.language=selected_language
        st.divider()

        st.markdown("** System status **")
        if st.button("Test API Connection"):
            with st.spinner("Testing..."):
                st.session_state.api_status=test_connection()
        
        status_text="🟢 ONLINE" if st.session_state.api_status is True else "🔴 OFFLINE"

        st.caption(f"API : {status_text}")

        st.divider()

        st.markdown("**Session Stats**")
        st.metric("Total Queries",st.session_state.total_queries)
        st.metric("Messages" , len(st.session_state.chat_history))

        st.divider()

        if st.button("clear chat"):
            st.session_state.chat_history=[]
            st.session_state.total_queries=0
            st.rerun()
        
        st.markdown(f"""
<div style='text-align:center; margin-top:20px; font-size:11px; color:#2a4a5a;'>
    Built by {ASSISTANT_OWNER} · Powered by Groq
</div>
""", unsafe_allow_html=True)
            

#Display all the past messages

def render_chat():
    """
    Loops through chat_history and print every message,
    This run every time the page returns ,this is why the 
    the chat_history needs to be in the session_state otherwise
    we have nothing to loop.
    """
    if not st.session_state.chat_history:
        st.markdown(f"""
        <div style='text-align:center; padding:60px 20px; color:#2a4a5a;'>
            <div style='font-size:48px; margin-bottom:16px;'>🤖</div>
            <div style='font-size:18px;color:#4a7a99; letter-spacing:2px;'>
                {ASSISTANT_NAME}  IS ONLINE
            </div>
            <div style='font-size:13px; margin-top:8px;color:#2a4a5a;'>
                Type a message or use the mic to start
            </div>
        </div>
        """,unsafe_allow_html=True)
        return

    for i,entry in enumerate(st.session_state.chat_history):
        if entry["role"]=="user":
            st.markdown(f"""
                <div classs='msg-label user-label'> YOU -{ASSISTANT_NAME} </div>
                <div class='user-msg'> {entry['content']} </div>
            """,unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='msg-label bot-label'>{ASSISTANT_NAME}</div>
            <div class='bot-msg'>{entry['content']}</div>
            """, unsafe_allow_html=True)

        is_last_message=(i== len(st.session_state.chat_history)-1)
        if is_last_message:
            render_audio_player(entry["content"])
    
def render_audio_player(text: str):
    """
    Generate and display audio controls for a given text.
    called only for th latest AI response to avoid
    regenerating audio for the entire chat history even rerun.
    """

    lang_code=SUPPORTED_LANGUAGES[st.session_state.language][0]
    filepath, status=text_to_speech(text, lang_code=lang_code)

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

def handle_query(user_input: str):
    if not user_input or not user_input.strip():
        return

    user_input=user_input.strip()
    st.session_state.chat_history.append({"role":"user", "content": user_input})

    with st.spinner(f"{ASSISTANT_NAME} IS THINKING..."):
        response=get_ai_response(
            user_message=user_input,
            chat_history=st.session_state.chat_history[:-1],
            language=st.session_state.language
        )  

    st.session_state.chat_history.append({
        "role":"assistant",
        "content":response
    })    
    st.session_state.total_queries +=1
    logger.info(f"query #{st.session_state.total_queries}:{user_input[:50]}")

def handle_voice_input() -> bool:
    with st.spinner("listening..."):
        text,status=listen_from_mic()
    if status !="success":
        st.warning(status)
        return False
    
    st.info(f"you said :\"{text}\"")
    handle_query(text)
    return True

def handle_voice_input_bytes(audio_bytes: bytes) -> bool:
    with st.spinner("Processing voice input..."):
        text, status = transcribe_audio(audio_bytes)
    if status != "success":
        st.warning(status)
        return False
    
    st.info(f"you said :\"{text}\"")
    handle_query(text)
    return True
    
# MAIN LOGIC OF THE APP

def main():
    init_session()
    render_sidebar()

    col1,col2=st.columns([3,1])

    with col1:
        st.markdown(f"""
<div class='main-title'>{ASSISTANT_NAME}</div>
<div style='color:#4a7a99; font-size:13px; letter-spacing:2px; margin-bottom:20px;'>
    MULTILINGUAL AI WEB ASSISTANT
</div>
""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
<div style='text-align:right; padding-top:10px; font-size:12px; color:#2a4a5a;'>
    Language: <span style='color:#00d4ff'>{st.session_state.language}</span>
</div>
""", unsafe_allow_html=True)
    st.divider()
    render_chat()
    st.divider()
    
    col_input,col_send,col_mic=st.columns([4,1,1])

    with col_input:
        user_text=st.text_input(
            "Ask AutoMoto something",
            label_visibility="collapsed",
            placeholder=f"Ask {ASSISTANT_NAME} anything, {ASSISTANT_OWNER}...",
            key="text_input",
        )
    
    with col_send:
        send_clicked=st.button("🚀",use_container_width=True)

    with col_mic:
        audio = mic_recorder(
            start_prompt="🎙️",
            stop_prompt="⏹️",
            just_once=True,
            use_container_width=True,
            key="mic_recorder"
        )

    # Handle button clicks
    
    if send_clicked and user_text:
        handle_query(user_text)
        st.rerun()

    # Handle browser voice input
    if audio and audio["bytes"] != st.session_state.get("last_audio"):
        st.session_state.last_audio = audio["bytes"]
        if handle_voice_input_bytes(audio["bytes"]):
            st.rerun()

if __name__ =="__main__":
    main()
   
