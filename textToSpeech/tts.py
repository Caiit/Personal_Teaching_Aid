from gtts import gTTS
import os


def generateSpeech(sentence, name):
	language = "nl"
	tts = gTTS(text=sentence, lang=language)
	name = name + ".mp3"
	tts.save(name)
	os.system("mpg123 " + name)


if __name__ == '__main__':
	# Greet the user 
	generateSpeech("Hallo! Leuk dat je er bent. Vandaag gaan wij lekker rekenen!", "begin")
	# Correct answer 
	generateSpeech("Dat is goed!", "goed")
	# Wrong answer 
	generateSpeech("Dat is fout!", "fout")
	# Goodbye 
	generateSpeech("Goed gewerkt vandaag! Tot de volgende keer", "dag")