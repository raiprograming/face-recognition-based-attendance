import cv2
import os
import time
import numpy as np

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
face_id = input('\n enter user id end press <return> ==>  ')

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
count = 0

while(True):

    ret, img = cam.read() 
    kernel=np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
    sharpened=cv2.filter2D(img,-1,kernel)
    #cv2.imshow('shrped',sharpened)
    #cv2.destroyAllWindows()

    gray = cv2.cvtColor(sharpened, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.25, 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(sharpened, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1

        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/r." + str(face_id) + '.' + str(count) + ".png", gray[y:y+h,x:x+w])

    cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 10:
         # Take 30 face sample and stop video
        break
    time.sleep(1)

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
