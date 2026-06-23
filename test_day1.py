import os
from dotenv import load_dotenv

print("="*50)
print("Day 1 Testing")
print("="*50)

print("day1 testing importing config.py...")
try:
    from config import ASSISTANT_NAME,ASSISTANT_OWNER,GROQ_MODEL
    print(f"config loaded")
    print(f"Assistant name: {ASSISTANT_NAME}")
    print(f"owner : {ASSISTANT_OWNER}")
    print(f"Model : {GROQ_MODEL}")
except Exception as e:
    print(f"Error: {e}")

print("LOADING .env file and checking groq API key ...")
load_dotenv()

key=os.getenv("GROQ_API_KEY")

if key and "paste_your" not in key:
    print("Groq key found ")
else:
    print("Groq key not found")

print("checking the log files")
print(f"  {'[OK]' if os.path.exists('logs') else 'not present'} logs/ folder exists")

print("DAY 1 TESTING COMPLETE")