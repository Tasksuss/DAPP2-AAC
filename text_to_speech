from gtts import gTTS
import os

text = "Hello! Welcome to this text-to-speech demo using gTTS in Python."

# set language
language = 'en'

# Create gTTS object
tts = gTTS(text=text, lang=language, slow=False)
tts.save("output.mp3")

if os.name == "nt":  # Windows
    os.system("start output.mp3")
elif os.name == "posix":  # macOS & Linux
    os.system("afplay output.mp3")  # macOS
    # os.system("mpg321 output.mp3")  # Linux (if mpg321 is installed)

print("Speech conversion complete!")
