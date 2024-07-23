import cv2
import csv
import time
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

        self.back="Back"
        self.user_ans=None

    def update(self,cursor,b_box):
        count=0
        for x,bb in enumerate(b_box):
            x1,y1,x2,y2=bb
            count+=1
            if count==(len(b_box)) and x1<cursor[0]<x2 and y1<cursor[1]<y2:
                self.user_ans=-1
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,256,0),cv2.FILLED)

            elif x1<cursor[0]<x2 and y1<cursor[1]<y2:
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

que_num=0
que_total=len(data)

while True:
    success, img =cap.read()
    img=cv2.flip(img,1)
    # print("x")
    hands, img=detector.findHands(img,flipType=False)

    if que_num<que_total:
        mcq=mcqList[que_num]

        img, b_box=cvzone.putTextRect(img,mcq.que,[200,100],2,2,colorT=(45, 45, 45), colorR=(240, 234, 180),offset=40)
        img, b_box_1=cvzone.putTextRect(img,mcq.choice_1,[200,250],2,2,colorT=(45, 45, 45), colorR=(240, 234, 180),offset=40)
        img, b_box_2=cvzone.putTextRect(img,mcq.choice_2,[600,250],2,2,colorT=(45, 45, 45), colorR=(240, 234, 180),offset=40)
        img, b_box_3=cvzone.putTextRect(img,mcq.choice_3,[200,400],2,2,colorT=(45, 45, 45), colorR=(240, 234, 180),offset=40)
        img, b_box_4=cvzone.putTextRect(img,mcq.choice_4,[600,400],2,2,colorT=(45, 45, 45), colorR=(240, 234, 180),offset=40)
        img, b_box_5=cvzone.putTextRect(img,mcq.back,[950,350],2,2,colorT=(45, 45, 45), colorR=(240, 234, 180),offset=40)

        # print("y")
        if hands:
            lmList=hands[0]["lmList"]
            cursor=lmList[8][:2]
            # print("z")

            length,_,img=detector.findDistance(lmList[8][:2],lmList[12][:2],img)
            # print(length)
            # print("t")
            
            if length<40:
                mcq.update(cursor,[b_box_1,b_box_2,b_box_3,b_box_4,b_box_5])
                # print(mcq.user_ans)
                print("question->",que_num)
                if (mcq.user_ans ==-1) and (que_num==0):
                    que_num=0
                    time.sleep(0.30)
                if (mcq.user_ans ==-1) and (que_num!=0):
                    que_num-=1
                    time.sleep(0.30)
                elif (mcq.user_ans is not None) and (mcq.user_ans!=-1):
                    time.sleep(0.30)
                    que_num+=1

    else:
        score=0
        for mcq in mcqList:
            if mcq.ans==mcq.user_ans:
                score+=1  
        score=round((score/que_total)*100,2)
        print(score)
        if score>40:
            img, _ =cvzone.putTextRect(img,"Quiz completed",[250,300],2,2,colorT=(255, 0, 0), colorR=(240, 234, 180),offset=40)
            img, _ =cvzone.putTextRect(img,f'Your score: {score}%',[700,300],2,2,colorT=(0, 255, 0), colorR=(240, 234, 180),offset=40)
        else:
            img, _ =cvzone.putTextRect(img,"Quiz completed",[250,300],2,2,colorT=(255, 0, 0), colorR=(240, 234, 180),offset=40)
            img, _ =cvzone.putTextRect(img,f'Your score: {score}%',[700,300],2,2,colorT=(0, 0, 255), colorR=(240, 234, 180),offset=40)
            
    # Draw progress bar
    bar_value=150+(850//que_total)*que_num
    cv2.rectangle(img,(150,600),(bar_value,650),(255,255,255),cv2.FILLED)
    cv2.rectangle(img,(150,600),(1000,650),(20,20,20),4)
    img, _ =cvzone.putTextRect(img,f'{round((que_num/que_total)*100)}%',[1030,635],2,2,colorT=(45, 45, 45), colorR=(255, 255, 255),offset=16)

    cv2.imshow("img",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
