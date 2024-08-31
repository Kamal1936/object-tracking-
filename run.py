import cv2
import numpy as np
from object_detection import ObjectDetection
import math


od = ObjectDetection()
cap=cv2.VideoCapture("video.mp4")
count =0
center_points_pre_frame =[]
traking_objects ={}
track_id =0

while True:
    ret, frame = cap.read()
    count+=1
    if not ret:
        break
    center_points_cur_frame=[]
    (class_id,score,boxes)=od.detect(frame)
    for box in boxes:
        (x,y,w,h)=box
        cx = int((x+x+w)/2)
        cy= int((y+y+h)/2)
        center_points_cur_frame.append((cx,cy))
        print("frame no",count,x,y,w,h)
        # cv2.circle(frame,(cx,cy),5,(0,0,255),-1)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    for pt in center_points_cur_frame:
        for pt2 in center_points_pre_frame:
            distance=math.hypot(pt2[0]-pt[0],pt2[1]-pt[1])

            if distance < 10:
                traking_objects[track_id] = pt
                track_id +=1

    for object_id, pt in traking_objects.items():
         cv2.circle(frame,(cx,cy),5,(0,0,255),-1)
         cv2.putText(frame,str(object_id),(pt[0],pt[1]-7),0,1,(0,0,255),-2)
    print("tracking objects")
    print(traking_objects)

         
    print("CUR FRAME")
    print(center_points_cur_frame)
    print("prev frame")
    print(center_points_pre_frame)  

    
    
    cv2.imshow("Frame",frame)
    center_points_pre_frame = center_points_cur_frame.copy()

    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()