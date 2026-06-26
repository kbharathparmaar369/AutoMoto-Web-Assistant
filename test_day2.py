import sys

print("="*50)
print("GROQ CONNECTION TESTING")
print("="*50)

print("\n IMORTING ai_handler...")

#TEST 1 : IMPORTING THE ai_handler
try:
    from ai_handler import get_ai_response, test_connection
    print("imported successfully")

except Exception as e:
    print(f"ERROR importing ai_handler :{e}")
    sys.exit(1)

#Test 2 : Connection test
print("\nGROQ API CONNETION TESTING")
ok=test_connection()
if ok:
    print("GROQ API CONNECTED SUCCESSFULLY")
else:
    print("Connection failed - check you API key in .env")
    sys.exit(1)

#Test 3 : basic response

print("\nASKING SOME BASIC QUESTIONS..")
response=get_ai_response(
    user_message="who are you ? one scentecne only.",
    chat_history=[],
    language="English"
)

print("\nAI RESPONSE :")
print(f" {response}")

#Testing Response in Hindi

print("\n Asking in Hindi mode")
response_hindi=get_ai_response(
    user_message="what is your name ?",
    chat_history=[],
    language="Hindi"
)
print(f"Response : '{response_hindi}'")

#CONVERSATION MEMORY TEST

print("\n CONVERSATION MEMORY TEST")
history=[
    {"role":"user","content":"My name is Bharath"},
    {"role":"assistant","content":"Nice to meet you , Bharath !"},
]
response_ctx=get_ai_response(
    user_message="what is you name ?",
    chat_history=history,
    language="English"
)
print(f"response : '{response_ctx}'")
if "bharath" in response_ctx.lower():
    print("context memory working correctly..")
else:
    print("Name was not recalled- check the context handler")

#CODING TEST

print("\n Testing coding ability..")
response_code=get_ai_response(
    user_message="write a simple code to print hello bharath",
    chat_history=[],
    language="English"

)
print(f"Response : '{response_code}'")

print("="*50)
print("Testing was completed...")
print("AI brain is successfully working...")
print("="*50)