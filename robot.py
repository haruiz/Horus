from config import config
from stt import s2t
from tts import t2s, list_of_voices
from cv import analize_image, determine_region
import cv2
from sys import platform
from util import take_picture_win
from playsound import playsound
from collections import Counter

class Robot:
   def __init__(self, name="Scrappy", voice="en-US-JessaRUS"):
      voices = list_of_voices()
      self.name = name
      self.voice = voices[voice]      

   def listen(self, input="./speech.wav"):
      lan = self.voice["Locale"]
      message = s2t(input, lan).lower()
      if "take a picture" in message:
         self._take_photo()
      
   
   def say(self, message):
      if platform == "win32":
         audio_file = t2s(message, self.voice)
         playsound(audio_file)

   def hi(self):
      self.say("Howdy!!!!...I'm {},..and I'm excited to be here at the hackaton 2020".format(self.name))

   @classmethod
   def _make_speak(cls,img_arr, objects, captions):
      str_message = "This is what I could see around: ....."
      # description
      for cap in captions:
         str_message += "{} \n".format(cap["text"])
      # objects
      str_message += "now...The objects I found were: ....."
      for obj in objects:
         x, y = obj["rectangle"]["x"],obj["rectangle"]["y"] 
         region = determine_region(img_arr, (x, y))
         str_message += "{} at {} location .....".format(obj["object"], region)
      str_message += "... However,.... you know I'm a robot"
      return str_message

   def _take_photo(self):
      if platform == "win32":
         img_file, img_arr = take_picture_win() # take a picture in window         
         objects, captions = analize_image(img_file)
         self.say(self._make_speak(img_arr, objects, captions))      
                  

if __name__ == "__main__":
    bot = Robot(voice="en-US-BenjaminRUS")
    bot.listen()
    
    
    





