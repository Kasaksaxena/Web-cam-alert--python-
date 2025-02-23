Webcam Alert and Email Notification App

This project is a motion detection application that uses your webcam to detect motion in real-time and sends an email alert 
with an attached image when motion is detected. The application is built using OpenCV and Python's email libraries.


Features
Real-time motion detection using the webcam.
Sends an automated email alert when motion is detected.
Attaches an image of the motion to the email for verification.
Efficient filtering to ignore small or irrelevant movements.

How It Works

1. The program accesses the webcam using OpenCV.
2. It captures frames, processes them (grayscale, GaussianBlur), and compares the current frame with the first frame to detect motion.
3. When motion is detected:The moving object's bounding box is drawn.A snapshot of the motion is saved.
An email alert is sent to the recipient with the captured image attached.
4. The program continues running until the user presses the "q" key to quit.
  
