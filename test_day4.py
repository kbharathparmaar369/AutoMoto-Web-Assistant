

import os
from speech_handler import text_to_speech

print("=" * 55)
print("  AutoMoto DAY 12 — TEXT-TO-SPEECH TEST")
print("=" * 55)

# ── Test 1: Basic English TTS ──────────────────────────────
print("\n[TEST 1] English text-to-speech...")
filepath, status = text_to_speech(
    "Hello Bharath, this is AutoMoto speaking.",
    lang_code="en"
)
if status == "success":
    size = os.path.getsize(filepath)
    print(f"   SUCCESS — {filepath} created ({size} bytes)")
else:
    print(f"   FAILED — {status}")

# ── Test 2: Hindi TTS ───────────────────────────────────────
print("\n[TEST 2] Hindi text-to-speech...")
filepath_hi, status_hi = text_to_speech(
    "नमस्ते भरत, मैं AutoMoto हूं।",
    lang_code="hi"
)
if status_hi == "success":
    size = os.path.getsize(filepath_hi)
    print(f"   SUCCESS — Hindi audio created ({size} bytes)")
else:
    print(f"   FAILED — {status_hi}")

# ── Test 3: Empty text handling ─────────────────────────────
print("\n[TEST 3] Empty text edge case...")
filepath_empty, status_empty = text_to_speech("", lang_code="en")
if status_empty != "success":
    print(f"   Correctly rejected empty text: '{status_empty}'")
else:
    print(f"   Should have failed but didn't")

# ── Test 4: Long text truncation ────────────────────────────
print("\n[TEST 4] Long text (testing 500-char cap)...")
long_text = "This is a test sentence. " * 50   # Way over 500 chars
filepath_long, status_long = text_to_speech(long_text, lang_code="en")
if status_long == "success":
    size = os.path.getsize(filepath_long)
    print(f"   SUCCESS — Long text handled, audio created ({size} bytes)")
else:
    print(f"   FAILED — {status_long}")

print("\n" + "=" * 55)
print("  DAY 12 TEST COMPLETE")
print("  Play the generated speech.mp3 file to verify audio quality")
print("=" * 55)