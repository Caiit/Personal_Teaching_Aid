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

	while(exception):
		with sr.Microphone(chunk_size=8192) as source: # use the default microphone as the audio source
			print('What is your answer?')
			r.adjust_for_ambient_noise(source, duration=1)
			audio = r.listen(source)
		try:
			response  = r.recognize_google(audio, language='nl-NL')
			print('You said ' + response)
			return response
		except LookupError:                            # speech is unintelligible
			print('Could not understand audio')
		except sr.UnknownValueError:
			print('Could not understand audio')
	return None

def hesitationInResponse(response):
	indicators = ['geen idee']
	if (('weet' in response) and ('niet' in response)):
		print('Weet je het antwoord niet?')
		return True
	for s in indicators:
		if (s in response):
			print('Weet je het antwoord niet?')
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

def correct(answer, w2n, n):
	response = getResponse()
	if hesitationInResponse(response):
		print('You hesitated')
	elif not answerInResponse(answer, response, w2n):
		print('Your answer is a number, but incorrect')
	else:
		print('Your answer is correct')
		return True
	return False

if __name__ == '__main__':
	startTime = time.time()

	fileDir = os.path.dirname(os.path.realpath(__file__))
	with open(os.path.join(fileDir, "wordToNumDict.pickle"), "rb") as handle:
		w2n = pickle.load(handle)
	correct(2, w2n, 2)

	print time.time() - startTime
