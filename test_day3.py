from speech_handler import listen_from_mic

print("="*50)
print("Day 3 Testing - Microphone Input")
print("="*50)

import speech_recognition as sr

try:
    mic_test=sr.Microphone.list_microphone_names()
    print(f"Found {len(mic_test)} audio device(s)")
    
    for i, name in enumerate(mic_test):
        print(f"    {i}:{name}")

except Exception as e:
    print(f"Could not list the microphones: '{e}'")


print("\n Live voice capture test....")
print("Speak something...")
text,status=listen_from_mic()

print("\n Results:")
print(f"Text: {text}")
print(f"Status: {status}")

print("Second capture (test repeatability)..")
print("Speak someting else now ...")
text2,status2=listen_from_mic()
if status2=="success":
    print(f"Text: {text2}")
    print(f"Status: {status2}")

print("="*50)
print("TESTING COMPELTED SUCCESSFULLY..")
print("="*50)