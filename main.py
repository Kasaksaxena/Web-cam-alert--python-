import cv2
import time
import glob
from emailing import send_email
video=cv2.VideoCapture(0)
time.sleep(1)
first_frame=None
status_list=[]
count=1

while True:
    status=0
    
    check,frame=video.read()
    
    #converts frame from color(BGR) to grayscale
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    #smooth grayscale image to reduce noise
    gray_frame_gau=cv2.GaussianBlur(gray_frame,(21,21),0)
    
    #first blurred grayscale frame is stored as reference frame for motion
    if first_frame is None:
        first_frame=gray_frame_gau
     
     # cal absolute diff between current frame and first frame to highlight changes   
    delta_frame=cv2.absdiff(first_frame,gray_frame_gau)  
    
    #converts diff image to binary image
    #pixels with intensity above 55 are set to 255(white),others are set to 0(black)
    thresh_frame=cv2.threshold(delta_frame,55,255,cv2.THRESH_BINARY)[1]  
    
    #expands white region in threeshold image to fill small gaps and make contours more prominent
    dil_frame=cv2.dilate(thresh_frame,None, iterations=2)
    cv2.imshow("My video",dil_frame)
    
    #detect contours(boundary of image) in binary image
    #RETR_EXTERNAL retrieve only external contours
    #CHAIN_APPROX_SIMPLE compresses contour points to save memory
    contours,check=cv2.findContours(dil_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    #filter smaller contours
    #skips contour smaller than 1000 to avoid noises 
    for contour in contours:
        if cv2.contourArea(contour)<5000:
            continue
        
        #cal bounding rectangle
        x,y,w,h=cv2.boundingRect(contour)
        rectangle=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        if rectangle.any():
            status=1 #indicate if motion is detected
            
            cv2.imwrite(f"images/{count}.png",frame)
            count=count+1
            all_images=glob.glob("images/*.png")
            index=int(len(all_images)/2)
            image_with_object=all_images[index]
            
    status_list.append(status) 
    status_list=status_list[-2:] # keeps only two recent statuses to avoid memory overload
    print(status_list)
    # transition (1 to 0) indicates motion stopped and send email func triggered
    if status_list[0]==1 and status_list[1]==0:
        send_email()
                
    cv2.imshow("Video",frame)
        
    
    key=cv2.waitKey(1)
    
    if key==ord("q"):
        break
    
video.release()    
    