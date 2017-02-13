import speech_recognition as sr
import pickle
r = sr.Recognizer()
r.energy_threshold = 4000

def recognizeAnswer(answer):
	with sr.Microphone(chunk_size=8192) as source:                # use the default microphone as the audio source
		audio = r.listen(source)                   # listen for the first phrase and extract it into audio data
	try:
		print("what is your answer?")
		phrase = r.recognize_google(audio, language='nl-NL')
		if(containsAnswer(phrase, answer)):
			return True
		else:
			return False

	    # print("You said " + phrase)                # recognize speech using Google Speech Recognition
	except LookupError:                            # speech is unintelligible
		print("Could not understand audio")
		return False


def containsAnswer(phrase, answer):
	if (str(answer) in phrase):
		return True
	for numberSynonym in wordToNumDict[str(answer)]:
		if (numberSynonym in phrase):
			return True
	return False

if __name__ == "__main__":
	with open('wordToNumDict.pickle', 'rb') as handle:
		wordToNumDict = pickle.load(handle)

	answer = raw_input("Answer: ")
	while True:
		if(recognizeAnswer(answer)):
			break