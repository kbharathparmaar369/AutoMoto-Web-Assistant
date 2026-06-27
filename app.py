import streamlit as st
import logging
import os

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
    
    for entry in st.session_state.chat_history:
        if entry["role"]=="user":
            st.write(f"**you**: {entry['content']}")
        else:
            st.write(f"**{ASSISTANT_NAME}**: {entry['content']}")


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

    user_text=st.text_input("Ask AutoMoto something :")

    if st.button("Send"):
        handle_query(user_text)
        st.rerun() # forces the page to redraw with the new message

if __name__ =="__main__":
    main()
   
