from gtts import gTTS
import os

text = "Hallo douwe, hoeveel koeien zie jij?"
language = "nl"
tts = gTTS(text=text, lang=language)
tts.save("speech.mp3")
os.system("mpg123 speech.mp3")
