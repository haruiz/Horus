import requests
from config import config
import json
import os
import tempfile

def get_token():
	subscription_key = config["SPEECH"]["AZURE_API_KEY"]
	endpoint = "{}/issueToken".format(config["SPEECH"]["AZURE_AUTH_URI"])
	response = requests.post(endpoint, headers={
		'Ocp-Apim-Subscription-Key': subscription_key
	})
	token = response.text
	return str(token)

def t2s(message, voice):
   token = get_token()	
   subscription_key = config["SPEECH"]["AZURE_API_KEY"]
   endpoint = "{}/v1".format(config["SPEECH"]["AZURE_API_URI_TTS"])
   print(voice["Gender"])
   message = '''
		<speak version='1.0' xml:lang='en-US'>
			<voice xml:lang='{}' xml:gender='{}' name='{}'>
				{}
			</voice>
		</speak>
   '''.format(voice["Locale"],  voice["Gender"], voice["ShortName"],message)
   response = requests.post(endpoint, data=message,headers={
		"Ocp-Apim-Subscription-Key": subscription_key, 
		"Authorization": "Bearer {}".format(token), 
		"Content-type": "application/ssml+xml",
		"X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm"
	})
   if response.status_code == 200:
      with tempfile.NamedTemporaryFile(suffix=".wav") as temp:
            file_name = temp.name
      with open(file_name, 'wb') as audio:
         audio.write(response.content)
         print("\nStatus code: " + str(response.status_code) +
               "\nYour TTS is ready for playback.\n")      
      return file_name   
   else:
      print("\nStatus code: " + str(response.status_code) +
            "\nSomething went wrong. Check your subscription key and headers.\n")
      return None

def list_of_voices():
   out_file = "voices.json"
   if not os.path.isfile(out_file):
      token = get_token()	
      subscription_key = config["SPEECH"]["AZURE_API_KEY"]
      endpoint = "{}/voices/list".format(config["SPEECH"]["AZURE_API_URI_TTS"])
      response = requests.get(endpoint,headers={		
         "Authorization": "Bearer {}".format(token)
      })   
      with open('voices.json', 'w') as outfile:
         outfile.write(json.dumps(response.json(), sort_keys=True, indent=4))   
   with open(out_file) as json_file: voices = json.load(json_file)   
   voices = {voice["ShortName"]:voice for voice in voices}
   return voices


