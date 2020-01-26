from config import config
import requests
import asyncio
import wave
import json

def get_token():
	subscription_key = config["SPEECH"]["AZURE_API_KEY"]
	endpoint = "{}/issueToken".format(config["SPEECH"]["AZURE_AUTH_URI"])
	response = requests.post(endpoint, headers={
		'Ocp-Apim-Subscription-Key': subscription_key
	})
	token = response.text
	return str(token)

def s2t(wav_file, lan="en-US"):	
	token = get_token()	
	subscription_key = config["SPEECH"]["AZURE_API_KEY"]
	endpoint = "{}?language={}".format(config["SPEECH"]["AZURE_API_URI_STT"], lan)	
	with open(wav_file, 'rb') as fd:
		contents = fd.read()
	response = requests.post(endpoint, data=contents,headers={
		"Ocp-Apim-Subscription-Key": subscription_key, 
		"Authorization": "Bearer {}".format(token), 
		"Content-type": "audio/wav; codecs=audio/pcm; samplerate=16000",
		"Accept": "application/json"
	})
	response_dict = response.json()
	is_success = response.status_code == 200 and response_dict["RecognitionStatus"] == "Success"	
	return response_dict["DisplayText"] if is_success  else None


	
