import pickle
import speech_recognition as sr
import os
import time

units = ['nul', 'twee', 'drie', 'vier', 'vijf',
'zes', 'zeven', 'acht', 'negen', 'tien', 'elf', 'twaalf',
'dertien', 'veertien', 'vijftien',  'zestien', 'zeventien', 'achttien',
'negentien', 'twintig', 'dertig', 'veertig', 'vijftig', 'zestig', 'zeventig',
'tachtig', 'negentig', 'duizend', 'miljoen', 'miljard', '0' '1', '2', '3', '4',
'5', '6', '7', '8', '9']

def getResponse():
	r = sr.Recognizer()
	exception = True

	while exception:
		# Use the default microphone as the audio source
		with sr.Microphone(chunk_size=8192) as source:
			r.adjust_for_ambient_noise(source, duration=0.5)
			try:
				audio = r.listen(source, timeout=5)
			except sr.WaitTimeoutError:
				return "Ik kon je niet verstaan"
		try:
			response  = r.recognize_google(audio, language='nl-NL')
			return response
		# Speech is unintelligible
		except LookupError:
			return "Ik heb je niet begrepen"
		except sr.UnknownValueError:
			return "Ik heb je niet begrepen"
	return None

def hesitationInResponse(response):
	indicators = ['geen idee']
	if (('weet' in response) and ('niet' in response)):
		return True
	for s in indicators:
		if (s in response):
			return True
	return False

def numberInResponse(response):
	for unit in units:
		if unit in response:
			return True
	return False

def answerInResponse(answer, response, w2n):
	containsAnswer = False
	answer = str(answer)
	if answer in response:
		containsAnswer = True
		response = response.replace(answer,'')
	else:
		for synonym in w2n[answer]:
			if synonym in response:
				containsAnswer = True
				response = response.replace(synonym,'')
	if (containsAnswer):
		if not numberInResponse(response):
			return True
	return False

def correct(answer, response, w2n, n):
	if hesitationInResponse(response):
		return False, "Je twijfelde"
	elif not answerInResponse(answer, response, w2n):
		return False, "Je antwoord is fout"
	else:
		return True, "Je antwoord is goed"

if __name__ == '__main__':
	startTime = time.time()

	fileDir = os.path.dirname(os.path.realpath(__file__))
	with open(os.path.join(fileDir, "wordToNumDict.pickle"), "rb") as handle:
		w2n = pickle.load(handle)
	response = getResponse()
	correct(2, response, w2n, 2)

	print time.time() - startTime
