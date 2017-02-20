import speech_recognition as sr
import pickle
from ctypes import *
import time

r = sr.Recognizer()
r.energy_threshold = 4000
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

units = ['nul', 'een', 'twee', 'drie', 'vier', 'vijf',
'zes', 'zeven', 'acht', 'negen', 'tien', 'elf', 'twaalf',
'dertien', 'veertien', 'vijftien',  'zestien', 'zeventien', 'achttien',
'negentien', 'twintig', 'dertig', 'veertig', 'vijftig', 'zestig', 'zeventig',
'tachtig', 'negentig', 'duizend', 'miljoen', 'miljard']

def py_error_handler(filename, line, function, err, fmt):
	pass

def recognizeAnswer(answer):
	print("What is your answer?")

	with sr.Microphone(chunk_size=8192) as source:                # use the default microphone as the audio source
		audio = r.listen(source)                   # listen for the first phrase and extract it into audio data
	try:
		startTime = time.time()
		phrase = r.recognize_google(audio, language='nl-NL')
		print time.time() - startTime
		print("You said " + phrase)                # recognize speech using Google Speech Recognition
		return containsAnswer(phrase, answer)

	except LookupError:                            # speech is unintelligible
		print("Could not understand audio")
	except sr.UnknownValueError:
		print("Could not understand audio")

	return False


def containsAnswer(phrase, answer):
	if (str(answer) in phrase):
		return True

	for numberSynonym in wordToNumDict[str(answer)]:
		if (numberSynonym in phrase):
			return True

	for unit in units:
		if unit in phrase:
			print("Incorrect answer")
	return False


if __name__ == "__main__":
	with open('wordToNumDict.pickle', 'rb') as handle:
		wordToNumDict = pickle.load(handle)

	# Set error handler
	c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
	asound = cdll.LoadLibrary('libasound.so')
	asound.snd_lib_error_set_handler(c_error_handler)

	answer = raw_input("Answer: ")
	while True:
		if(recognizeAnswer(answer)):
			print("Correct answer")
			break
