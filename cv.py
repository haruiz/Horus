import requests
from config import config
import numpy as np
import math
import cv2

def analize_image(img_file):
   subscription_key = config["VISION"]["AZURE_API_KEY"]
   endpoint = config["VISION"]["AZURE_API_URI"]
   endpoint = "{}/v2.1/analyze?visualFeatures=Objects,Categories,Description,Color".format(endpoint)   
   with open(img_file, "rb") as fr:
       content = fr.read()   
   response = requests.post(endpoint, data=content, headers={
      "Ocp-Apim-Subscription-Key": subscription_key,
      "Content-Type": "application/octet-stream"
   })   
   response_dict = response.json()   
   objects = response_dict["objects"]
   captions = response_dict["description"]["captions"]
   return objects, captions if response.status_code == 200 else None

def analize_people(img_file):
   subscription_key = config["FACE"]["AZURE_API_KEY"]
   endpoint = config["FACE"]["AZURE_API_URI"]
   endpoint = "{}/face/v1.0/detect?returnFaceAttributes=age,gender,emotion,hair,accessories".format(endpoint)   
   with open(img_file, "rb") as fr:
       content = fr.read()   
   response = requests.post(endpoint, data=content, headers={
      "Ocp-Apim-Subscription-Key": subscription_key,
      "Content-Type": "application/octet-stream"
   })   
   response_dict = response.json() 
   return response_dict

def show_objects(img_file, objects):
   img = cv2.imread(img_file)
   for obj in objects:
      if obj["confidence"] > 0.5:
         x, y = obj["rectangle"]["x"], obj["rectangle"]["y"]
         w, h = obj["rectangle"]["w"], obj["rectangle"]["h"]
         cv2.rectangle(img,(x,y),(x+w, y+h), (255,0,255), 2)
         cv2.putText(img, obj["object"], (x + 20,y + 20),  cv2.FONT_HERSHEY_PLAIN,2, (255,0,255))
   cv2.imshow("img", img)
   cv2.waitKey(0)

def determine_region(img, pt):
   img = img if isinstance(img, np.ndarray) else cv2.imread(img)
   h, w , _ = np.shape(img)   
   n = 3
   roi_width, roi_names =  math.ceil(w / n), ["left", "center", "right"]
   return [ roi_names[i] for i in range(n) if (i * roi_width + roi_width >= pt[0] > i * roi_width)]
         
