import numpy as np
import cv2 as cv


cap = cv.VideoCapture('vtest.avi')
ret, frame1 = cap.read()
prvs = cv.cvtColor(frame1,cv.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255
b=0
sample_count=7
fourcc = cv.VideoWriter_fourcc(*'XVID') 
out = cv.VideoWriter('output1.avi', fourcc, 20.0, (int(cap.get(3)),int(cap.get(4)))) 
font = cv.FONT_HERSHEY_SIMPLEX
while cap.isOpened():
    ret, frame2 = cap.read()
    next = cv.cvtColor(frame2,cv.COLOR_BGR2GRAY)
    flow = cv.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv.cartToPolar(flow[...,0], flow[...,1])
    
    mag[mag<1]=0
    a=mag[mag!=0]
    
    for i in range(7):
     a[abs(a-np.mean(a))>0.5]=0
     a=a[a!=0]
    sample_count+=1
    if sample_count==7:
       b=np.mean(a)
    if sample_count==8:
       #print(b*0.3)
       cv.putText(frame2,str(b*0.3),(5,400), font, 1, (200,255,155), 2, cv.LINE_AA)
       sample_count=0
    else:
       #print(np.mean(a))
       cv.putText(frame2,str(np.mean(a)*0.3),(5,400), font, 1, (200,255,155), 2, cv.LINE_AA)
    #(values,counts) = np.unique(a,return_counts=True)
    #ind=np.argmax(counts)
    #print (values[ind])
    
    #cv.imshow('mag',mag)
    
    #hsv[...,0] = ang*180/np.pi/2
    #hsv[...,2] = cv.normalize(mag,None,0,255,cv.NORM_MINMAX)
    #bgr = cv.cvtColor(hsv,cv.COLOR_HSV2BGR)
    cv.imshow('frame2',frame2)
    out.write(frame2)  
    k = cv.waitKey(10) & 0xff
    if k == ord('q'):
        break
    elif k == ord('s'):
        cv.imwrite('opticalfb.png',frame2)
        cv.imwrite('opticalhsv.png',bgr)
    prvs = next 
   
        
cap.release()
out.release()
cv.destroyAllWindows()