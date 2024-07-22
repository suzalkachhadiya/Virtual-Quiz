import cv2
import csv
import cvzone
from cvzone.HandTrackingModule import HandDetector


cap=cv2.VideoCapture(0)
cap.set(3,1080)
cap.set(4,480)
detector=HandDetector(detectionCon=0.8)

class MCQ:
    def __init__(self,data):
        self.que=data[0]
        self.choice_1=data[1]
        self.choice_2=data[2]
        self.choice_3=data[3]
        self.choice_4=data[4]
        self.ans=int(data[5])

        self.user_ans=None

    def update(self,cursor,b_box):
        for x,bb in enumerate(b_box):
            x1,y1,x2,y2=bb
            if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                self.user_ans=x+1
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,256,0),cv2.FILLED)

# import Data
file_path="Data\MCQs.csv"
with open(file_path,newline="\n") as f:
    reader=csv.reader(f)
    data=list(reader)[1:]

# create object for each MCQ
mcqList=[]
for que in data:
    mcqList.append(MCQ(que))

print(mcqList)

que_num=0
q_total=len(data)

while True:
    success, img =cap.read()
    img=cv2.flip(img,1)
    

    hands, img=detector.findHands(img,flipType=False)

    mcq=mcqList[3]

    img, b_box=cvzone.putTextRect(img,mcq.que,[100,100],2,2,offset=50,border=4)
    img, b_box_1=cvzone.putTextRect(img,mcq.choice_1,[100,250],2,2,offset=50,border=4)
    img, b_box_2=cvzone.putTextRect(img,mcq.choice_2,[400,250],2,2,offset=50,border=4)
    img, b_box_3=cvzone.putTextRect(img,mcq.choice_3,[100,400],2,2,offset=50,border=4)
    img, b_box_4=cvzone.putTextRect(img,mcq.choice_4,[400,400],2,2,offset=50,border=4)

    if hands:
        lmList=hands[0]["lmList"]
        cursor=lmList[8][:2]

        length,_,img=detector.findDistance(lmList[8][:2],lmList[12][:2],img)
        # print(length)

        if length<50:
            mcq.update(cursor,[b_box_1,b_box_2,b_box_3,b_box_4])
            print(mcq.user_ans)
            if mcq.user_ans is not None:
                pass
            

    cv2.imshow("img",img)
    cv2.waitKey(1)
