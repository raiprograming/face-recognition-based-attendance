import tkinter as tk
import cv2
import os
import time
import pymysql
import numpy as np
list1=[]
def takePhoto():
    cam=cv2.VideoCapture(0)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml') 
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX

    names = ['None', 'shivam',"kunal",'unknown',"Anna","tushar"] 
    count=1
    cam = cv2.VideoCapture(0)
    l1.config(text="enter space for capture and esc for exit",width=40,height=5,fg="red",bg="black")
    cam.set(3, 450) # set video width
    cam.set(4, 450) # set video height
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    global list1
    while True:
        ret,img=cam.read()
        cv2.resize(img,(280,280))
        kernel=np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
        sharpened=cv2.filter2D(img,-1,kernel)
        sharpened=cv2.filter2D(img,-1,kernel)
        gray = cv2.cvtColor(sharpened,cv2.COLOR_BGR2GRAY)
    
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.05,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
            )

        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            cv2.imshow('video',img)
        k = cv2.waitKey(33)
        if k==27:
            print(list1)
            cv2.destroyAllWindows()
            cam.release()
            break 
    
        if k==32:
            list1.clear()
            l1.config(text="frame captured",width=40,height=5,fg="red",bg="black",font=("Courier",18))

            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                confidence = recognizer.predict(cv2.resize(gray[y:y+h,x:x+w],(280,280)))

                #rno="r"+str(id)
                #print(rno)
                #list1.append(id)
                print(confidence)
                cv2.putText(img, str(confidence[0]), (x+5,y-5), font, 1, (0,0,255), 2)
                

        # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence[1] <50):
                    #print("got it")
                    list1.append(confidence[0])
                    print(list1)
                    #id = names[confidence[0]]
                    #cv2.putText(img, str(id), (x+5,y-5), font, 1, (0,0,255), 2)
                    #cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
                else:
                    id = "unknown" 
    
            cv2.imshow('camera',img) 
            time.sleep(1)
        else:
            pass
def addData():
    global db    
    global cursor
    db=pymysql.connect("localhost","shivam","rai123","attendence")
    cursor=db.cursor()
    l1.config(text="looged in",width=40,height=5,fg="red",bg="black",font=("Courier",12))
def takeAttendence():
    j=[0,0,0,0,0,0]
    for i in list1:
        j[i]=1
    sql="insert into algorithm values(curdate(),1,1,1,1,1)"
    cursor.execute("insert into algorithm values(CURRENT_TIMESTAMP(),%s,%s,%s,%s,%s)"%(j[1],j[2],j[3],j[4],j[5]))
    db.commit()
    l1.config(text="attendence taken",width=30,height=5,fg="red",bg="black",font=("Courier",21))
master = tk.Tk()
master.geometry("800x500")
global l1
l1= tk.Label(master,text="start the attendence",width=40,height=5,fg="red",bg="black",font=("Courier",10,'bold'))
l1.grid(row=0,column=1)
tk.Label(master, text="enter subject",height=1,width=25).grid(row=6)

e1 = tk.Entry(master,width=20)

e1.grid(row=6, column=1)
button = tk.Button(master, text="login",fg="red",command=addData,font=("Courier",15,'bold'))
button.grid(row=10,column=1)
button2=tk.Button(master,text="capture photo",fg="red",command=takePhoto,font=("Courier",15,'bold'))
button2.grid(row=12,column=1)
b3=tk.Button(master,text="add attendence",command=takeAttendence,font=("Courier",15,'bold'))
b3.grid(row=15,column=1)
print(list1)
master.mainloop()


