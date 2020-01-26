from config import config
from stt import s2t
from tts import t2s, list_of_voices
from cv import analize_image, determine_region, analize_people
import cv2
from sys import platform
from util import take_picture_win
from cam import CamThread
from misc import joke_of_the_day, get_tamu_bus_next_stop
import tempfile
from playsound import playsound
from collections import Counter
import speech_recognition as sr  
import re  

class Robot:
   def __init__(self, name="Otis", voice="en-US-JessaRUS"):
      voices = list_of_voices()
      self.name = name
      self.voice = voices[voice]
      self.camera = CamThread(0)      
      self.camera.start()


   def listen(self, input="./speech.wav"):                    
         print("Listening....")
         def callback(recognizer, audio):            
            try:
               print("I listen something!!")
               with open(input, "wb") as f:
                  f.write(audio.get_wav_data())
               lan = self.voice["Locale"]
               msg = s2t(input,lan)
               print("Message received: {}".format(msg))
               if msg and isinstance(msg, str):
                  msg = msg.lower()
                  if any(map(lambda  x: x in msg,["picture", "photo"])):                     
                     self._analize_photo("description")
                  elif any(map(lambda  x: x in msg,["person", "persons", "people"])):                     
                     self._analize_photo("persons")
                  elif any(map(lambda  x: x in msg,["hi", "hello"])):
                     self._hi()
                  elif "joke" in msg:
                     self._joke()      
                  elif any(map(lambda  x: x in msg,["route", "bus"])):                  
                     temp = re.findall(r'\d+', msg) 
                     res = list(map(int, temp)) 
                     if len(res) > 0:
                        msg =get_tamu_bus_next_stop(res[0])
                        self.say(msg)
            except Exception as ex:
               print("Oops! Didn't catch that {}".format(str(ex)))
         r = sr.Recognizer()
         r.listen_in_background(sr.Microphone(), callback)
         import time
         while True: time.sleep(0.1)# liste in background for ever      

   
   def say(self, message):
      if platform == "win32":
         audio_file = t2s(message, self.voice)
         playsound(audio_file)

   def _joke(self):
      joke = joke_of_the_day()
      self.say(joke)

   def _hi(self):
      self.say("Howdy!!!!...I'm {},..and I'm excited to be here at the hackaton 2020".format(self.name))

   @classmethod
   def _make_image_description(cls,img_arr, objects, captions):
      str_message = ""
      if len(captions) > 0 or len(objects) > 0:
         if len(captions) > 0:
            str_message = "This is what I could see around: ....."      
            for cap in captions:
               str_message += "{} \n".format(cap["text"])         
         if len(objects) > 0:
            str_message += "now...The objects I found were: ....."
            for obj in objects:
               x, y = obj["rectangle"]["x"],obj["rectangle"]["y"] 
               region = determine_region(img_arr, (x, y))
               str_message += "{} at {} location .....".format(obj["object"], region)
         str_message += "... However,.... you know I'm a robot"         
      else:
         str_message += "sorry,...nothing to say" 
      return str_message

# {'faceId': 'cf11c465-aa7a-4da9-b53d-0ef571ad7dd6', 'faceRectangle': {'top': 285, 'left': 446, 'width': 78, 'height': 78}, 
# 'faceAttributes': {'gender': 'male', 'age': 37.0, 'emotion': {'anger': 0.0, 'contempt': 0.0, 'disgust': 0.0, 'fear': 0.0, 'happiness': 0.0, 'neutral': 0.998, 'sadness': 0.001, 'surprise': 0.0}, 'accessories': [{'type': 'glasses', 'confidence': 1.0}], 'hair': {'bald': 0.12, 'invisible': False, 'hairColor': [{'color': 'black', 'confidence': 1.0}, {'color': 'other', 'confidence': 0.62}, {'color': 'gray', 'confidence': 0.57}, {'color': 'brown', 'confidence': 0.42}, {'color': 'blond', 'confidence': 0.07}, {'color': 'red', 'confidence': 0.02}]}}}    
# Male

   @classmethod
   def _make_people_description(cls,img_arr, people):
      str_message=""
      if len(people) > 0:
         str_message = "there {} {} {}".format("are" if len(people) > 1 else "is",len(people),
         "people" if len(people) > 1 else "person")
         for i, person in enumerate(people):            
            gender = person["faceAttributes"]["gender"]
            age = person["faceAttributes"]["age"]
            x = person["faceRectangle"]["left"]
            y = person["faceRectangle"]["top"]
            hair = person["faceAttributes"]["hair"]["hairColor"][0]["color"]
            loc = determine_region(img_arr, (x,y))[0]            
            str_message +="....The person number {}..located at the {} side ... is a {}... of around {} years old .... hair color {}...".format(i+1,loc,gender, age, hair )

      return str_message

   def _analize_photo(self, opt):
      if platform == "win32":         
         img_arr = self.camera.frame
         with tempfile.NamedTemporaryFile(suffix=".jpg") as temp:
            file_name = temp.name         
         cv2.imwrite(file_name, img_arr)
         if opt == "description":
            objects, captions = analize_image(file_name)
            self.say(self._make_image_description(img_arr, objects, captions))      
         elif opt == "persons":
            people = analize_people(file_name)            
            self.say(self._make_people_description(img_arr,people))      






    
    
    





