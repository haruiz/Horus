import cv2
import tempfile

def take_picture_win():
   cam = cv2.VideoCapture(0)
   file_name = None
   img = None,
   w_name = "image"
   cv2.namedWindow(w_name, cv2.WINDOW_NORMAL)
   while True:
      ret, frame = cam.read()
      if not ret:
         break
      cv2.imshow(w_name, frame)
      k = cv2.waitKey(1)
      if k%256 == 32:
         # SPACE pressed
         with tempfile.NamedTemporaryFile(suffix=".jpg") as temp:
            file_name = temp.name
         img = frame
         cv2.imwrite(file_name, frame)
         break
   cam.release()
   cv2.destroyAllWindows()
   return file_name, img

def take_picture_raspi():
   raise NotImplementedError
