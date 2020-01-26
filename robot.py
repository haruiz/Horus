from config import config
from stt import s2t
from tts import t2s, list_of_voices
from cv import analize_image, determine_region
import cv2
from sys import platform
from util import take_picture_win
from cam import CamThread
from misc import joke_of_the_day
import tempfile
from playsound import playsound
from collections import Counter
import speech_recognition as sr    

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
                     self._analize_photo()
                  if any(map(lambda  x: x in msg,["person", "persons"])):                     
                     pass
                  elif "hi" in msg:
                     self._hi()
                  elif "joke" in msg:
                     self._joke()                  
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
   def _describe_image(cls,img_arr, objects, captions):
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

   def _analize_photo(self):
      if platform == "win32":
         #img_file, img_arr = take_picture_win() # take a picture in window         
         img_arr = self.camera.frame
         with tempfile.NamedTemporaryFile(suffix=".jpg") as temp:
            file_name = temp.name         
         cv2.imwrite(file_name, img_arr)
         objects, captions = analize_image(file_name)
         self.say(self._describe_image(img_arr, objects, captions))      



    
    
    





