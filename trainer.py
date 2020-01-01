import cv2
import numpy as np
from PIL import Image
import os

# Path for face image database
path = 'dataset'

recognizer = cv2.face.LBPHFaceRecognizer_create()
#detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

dim=(3000,4000)
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')
        #cv2.resize(PIL_img,(100,50),fx=0.5,fy=0.5)# convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        #faces = detector.detectMultiScale(img_numpy)
        #for (x,y,w,h) in faces:
        faceSamples.append(cv2.resize(img_numpy,(280,280)))
        ids.append(id)
    return faceSamples,ids
    
  

print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces,ids = getImagesAndLabels(path)
print(faces)
print(ids)
print(np.array(ids))
recognizer.train(faces, np.array(ids))

# Save the model into trainer/trainer.yml
recognizer.save('trainer/trainer.yml') 
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))