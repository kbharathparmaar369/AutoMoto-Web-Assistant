# 🤖 AutoMoto — Multilingual AI Web Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11.9-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A multilingual, voice-enabled AI web assistant powered by Groq's LLaMA 3.3 70B.**  
Type or speak your question — get a real AI answer back in text and audio, in 8 languages.

### 🌐 [Live Demo →](https://automoto-web-assistant.streamlit.app)

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Deployment](#-deployment) • [Architecture](#-architecture) • [Tech Stack](#-tech-stack)

</div>

---

## 📌 Overview

AutoMoto Web Assistant is a Streamlit-based AI chatbot that goes beyond simple Q&A. It accepts both typed and spoken input, sends every query to Groq's LLaMA 3.3 70B model for a genuine AI-generated response, and speaks that response back in the user's chosen language using Google Text-to-Speech.

The app is deployed live on Streamlit Community Cloud — no installation needed to try it, just open the [live demo link](https://automoto-web-assistant.streamlit.app).

This is **Project 2** of a two-part AI assistant system. [Project 1 →](https://github.com/kbharathparmaar369/AutoMoto-CLI-Voice-Assistant) is a rule-based CLI voice assistant with OS integration.

---

## ✨ Features

### 🧠 Real AI Conversations
- Powered by Groq's `llama-3.3-70b-versatile` — fast, high-quality responses
- Maintains conversation context — remembers what you said earlier in the session
- Custom system prompt gives AutoMoto a consistent personality
- Handles general knowledge, coding help, explanations, and casual conversation

### 🌐 Multilingual Support
- 8 languages: English, Hindi, Tamil, Telugu, French, Spanish, German, Japanese
- AI responds directly in the selected language
- Text-to-speech output matches the selected language

### 🎤 Dual Input Modes
- Type your question in the text box
- Or click the mic button and speak — voice is transcribed and processed identically
- *(Voice input requires a local microphone — see [Deployment](#-deployment) for live demo limitations)*

### 🔊 Audio Output
- Every AI response is converted to speech via gTTS
- Playable directly in the browser
- Downloadable as an MP3 file

### 💬 Chat Interface
- Scrolling chat history with styled message bubbles
- Session stats: total queries, message count
- One-click chat reset

### 📋 Production Logging
- Every query and response logged with timestamps to `logs/application.log`
- API connection status check built into the sidebar

---

## 📹 Demo

> 🎬 **[Watch the demo video here](#)** ← *(add your YouTube/Loom link)*
>
> 🌐 **[Try the live app here](https://automoto-web-assistant.streamlit.app)**

```
┌─────────────────────────────────────────────────────┐
│           🤖 AutoMoto — AI Web Assistant             │
├──────────────┬──────────────────────────────────────┤
│  SIDEBAR     │   MAIN CHAT AREA                     │
│              │                                      │
│  🌐 Language │   YOU — BHARATH                      │
│  [Hindi  ▼]  │   प्रकाश संश्लेषण क्या है?                │
│              │                                      │
│  ⚡ Status   │   AUTOMOTO                            │
│  ✅ Connected│   प्रकाश संश्लेषण वह प्रक्रिया है...         │
│              │   ▶️ [Play Audio]  ⬇️ [Download]      │
│  📊 Stats    │                                      │
│  Queries: 4  │   [Type your question...] [Send][🎤] │
│              │                                      │
│  🗑️ Clear    │                                      │
└──────────────┴──────────────────────────────────────┘
```

---

## 🛠️ Installation

### Prerequisites
- Windows 10 or 11
- Python 3.11.9
- Working microphone
- Free Groq API key ([console.groq.com](https://console.groq.com))

### Step 1 — Clone the Repository
```bash
git clone https://github.com/kbharathparmaar369/AutoMoto-Web-Assistant.git
cd AutoMoto-Web-Assistant
```

### Step 2 — Create Virtual Environment
```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

> ⚠️ **PyAudio on Windows** — if it fails to install:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### Step 4 — Add Your Groq API Key
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_key_here
```

### Step 5 — Run the App
```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`

---

## ☁️ Deployment

This app is deployed on **Streamlit Community Cloud** (free tier). Here's how it's set up, in case you want to deploy your own fork.

### Live URL
```
https://automoto-web-assistant.streamlit.app
```

### How It Was Deployed

1. **Pushed to GitHub** — Streamlit Cloud deploys directly from a connected GitHub repo
2. **Added `packages.txt`** — specifies Linux system dependencies needed for PyAudio:
   ```
   portaudio19-dev
   ```
3. **Removed Windows-only packages** from `requirements.txt` (`pywin32`, `comtypes`) since Streamlit Cloud runs on Linux
4. **Added Streamlit Secrets** — the Groq API key is stored securely in Streamlit Cloud's dashboard (Settings → Secrets), not in any committed file:
   ```toml
   GROQ_API_KEY = "your_key_here"
   ```
5. **Dual-source key loading** in `ai_handler.py` — checks `.env` first for local development, falls back to `st.secrets` for cloud deployment, so the same code runs in both environments:
   ```python
   GROQ_API_KEY = os.getenv("GROQ_API_KEY")
   if not GROQ_API_KEY:
       GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
   ```

### Known Limitation on the Live Deployment

The 🎤 **voice input** button will not work on the live deployed version. Streamlit Cloud runs on a remote Linux server with no physical microphone attached, so `sr.Microphone()` cannot find an input device. The app handles this gracefully — it shows *"No microphone detected"* instead of crashing — but voice input only works when running the app **locally** on a machine with a real microphone.

**Text input, AI responses, multilingual output, and audio playback/download all work fully on the live deployment.**

---

## 🏗️ Architecture

```
User Input
   │
   ├── Typed text ──────────────────┐
   │                                │
   └── Voice ──→ speech_handler.py  │
                 (SpeechRecognition │
                  + Google Speech   │
                  API)              │
                       │            │
                       └────────────┤
                                    ▼
                              app.py
                       (Streamlit session state,
                        chat history management)
                                    │
                                    ▼
                            ai_handler.py
                    (Groq API — LLaMA 3.3 70B,
                     system prompt, context history)
                                    │
                                    ▼
                            AI Response Text
                                    │
                       ┌────────────┴────────────┐
                       ▼                          ▼
                Displayed in chat          speech_handler.py
                  (chat bubble)              (gTTS conversion)
                                                   │
                                                   ▼
                                        st.audio() + download_button
                                                   │
                                                   ▼
                                          logs/application.log
```

---

## 📁 Project Structure

```
AutoMoto-Web-Assistant/
│
├── app.py                ← Streamlit UI, session state, main entry point
├── ai_handler.py         ← Groq API integration, conversation context
├── speech_handler.py     ← Voice input (mic) + voice output (gTTS)
├── config.py             ← All settings: languages, prompts, model config
│
├── logs/                 ← Auto-created at runtime
│   └── application.log
│
├── requirements.txt      ← Locked dependency versions (Linux-compatible)
├── packages.txt          ← Linux system dependencies for Streamlit Cloud
├── .env                  ← Groq API key for local dev (not committed)
└── README.md
```

---

## 📦 Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| **Python** | 3.11.9 | Core language |
| **Streamlit** | 1.35.0 | Web UI framework |
| **Groq SDK** | 0.9.0 | LLaMA 3.3 70B API access |
| **SpeechRecognition** | 3.10.4 | Voice input → text |
| **PyAudio** | 0.2.14 | Microphone audio stream |
| **gTTS** | 2.5.1 | Multilingual text-to-speech |
| **python-dotenv** | 1.0.1 | Secure API key loading |

---

## 📊 Test Results

```
=======================================================
  AutoMoto WEB ASSISTANT — FINAL TEST SUITE
=======================================================
  [1] Groq API Connection           1/1  ✅
  [2] AI Text Responses             3/3  ✅
  [3] Conversation Memory           1/1  ✅
  [4] Text-to-Speech                3/3  ✅
  [5] Logging                       2/2  ✅
=======================================================
  RESULTS: 10/10 passed
  🎉 ALL TESTS PASSED
=======================================================
```

---

## 🌍 Supported Languages

| Language | Text Response | Voice Input | Audio Output |
|---|---|---|---|
| English | ✅ | ✅ | ✅ |
| Hindi | ✅ | ✅ | ✅ |
| Tamil | ✅ | ✅ | ✅ |
| Telugu | ✅ | ✅ | ✅ |
| French | ✅ | ✅ | ✅ |
| Spanish | ✅ | ✅ | ✅ |
| German | ✅ | ✅ | ✅ |
| Japanese | ✅ | ✅ | ✅ |

---

## 🔧 Configuration Reference

All settings live in `config.py`:

```python
ASSISTANT_NAME  = "AutoMoto"
ASSISTANT_OWNER = "Bharath"

GROQ_MODEL   = "llama-3.3-70b-versatile"
MAX_TOKENS   = 1024
TEMPERATURE  = 0.7

DEFAULT_LANGUAGE = "English"
```

---

## 🚀 Related Project

This is **Project 2** of a two-part AI assistant system.

**[Project 1 — AutoMoto CLI Voice Assistant →](https://github.com/kbharathparmaar369/AutoMoto-CLI-Voice-Assistant)**
- Rule-based command processor
- Offline TTS via pyttsx3
- OS integration: apps, music, screenshots
- 30+ voice commands

---

## ⚡ Known Limitations

- **Voice input on the live demo** — requires a local microphone, so it's only available when running the app locally (see [Deployment](#-deployment))
- Voice and audio responses use request-response APIs rather than streaming, introducing a few seconds of latency per turn. A production version could integrate streaming TTS (e.g. ElevenLabs Flash v2.5) for near real-time audio
- gTTS requires an internet connection — no offline fallback
- Groq free tier is rate-limited to 30 requests/minute, sufficient for personal use and demos

---

## 👨‍💻 Author

**Bharath Kumar**
Engineering Student

[![GitHub](https://img.shields.io/badge/GitHub-kbharathparmaar369-181717?style=flat&logo=github)](https://github.com/kbharathparmaar369)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/kbharathparmaar369)

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
  <sub>Built with ❤️ and Python by Bharath · Powered by Groq</sub>
</div>
