import cv2
import time
import glob
import os
from emailing import send_email
from threading import Thread
video=cv2.VideoCapture(0)
time.sleep(1)
first_frame=None
status_list=[]
count=1


def clean_folder():
    print("cleaning folder started")
    images=glob.glob("images/*.png")
    if not images:
        print("No.png files found in the folder")
    else:
        print(f"Found{len(images)} to delete.")    
    for image in images:
        try:
         time.sleep(0.02)
         os.remove(image)
         print(f"Deleted:{image}")
         
        except Exception as e:
            print(f"Error deleting {image} :{e}")
             
while True:
    status=0
    
    check,frame=video.read()
    
    if not check:
        continue # skips iterations if frame capture fails
    
    #converts frame from color(BGR) to grayscale
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    #smooth grayscale image to reduce noise
    gray_frame_gau=cv2.GaussianBlur(gray_frame,(21,21),0)
    
    #first blurred grayscale frame is stored as reference frame for motion
    if first_frame is None or count % 100==0: #update every 100 frames
        first_frame=gray_frame_gau
        continue
     
     # cal absolute diff between current frame and first frame to highlight changes   
    delta_frame=cv2.absdiff(first_frame,gray_frame_gau)  
    
    #converts diff image to binary image
    #pixels with intensity above 55 are set to 255(white),others are set to 0(black)
    thresh_frame=cv2.threshold(delta_frame,60,255,cv2.THRESH_BINARY)[1]  
    
    #expands white region in threeshold image to fill small gaps and make contours more prominent
    dil_frame=cv2.dilate(thresh_frame,None, iterations=2)
    cv2.imshow("Motion Detection",dil_frame)
    
    #detect contours(boundary of image) in binary image
    #RETR_EXTERNAL retrieve only external contours
    #CHAIN_APPROX_SIMPLE compresses contour points to save memory
    contours,_=cv2.findContours(dil_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    #filter smaller contours
    #skips contour smaller than 1000 to avoid noises 
    for contour in contours:
        if cv2.contourArea(contour)<3000:
            continue
        
        #draw rectangle around motion
        x,y,w,h=cv2.boundingRect(contour)
        rectangle=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        status=1 #indicate if motion is detected
          
        # Save the frame 
        resized_frame=cv2.resize(frame,(640,480))   
        cv2.imwrite(f"images/{count}.png",resized_frame)
        count=count+1
       
        all_images=glob.glob("images/*.png")
        image_with_object=None
        if all_images:
         index=int(len(all_images)/2)
         image_with_object=all_images[index]
            
    status_list.append(status) 
    status_list=status_list[-2:] # keeps only two recent statuses to avoid memory overload
    print(status_list)
    # transition (1 to 0) indicates motion stopped and send email func triggered
    if len(status_list)>=2 and status_list[0]==1 and status_list[1]==0:
      if image_with_object:
        email_thread=Thread(target=send_email,args=(image_with_object,))
        email_thread.daemon=True
        email_thread.start()
       # time.sleep(5)
        
        
      clean_thread=Thread(target=clean_folder)
      clean_thread.daemon=True
      clean_thread.start()
        
        
    cv2.imshow("Video",frame)
    key=cv2.waitKey(1)
    if key==ord("q"):
        break
        
               
video.release() 
cv2.destroyAllWindows()
        
    
    
    
    