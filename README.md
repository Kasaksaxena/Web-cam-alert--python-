 # Webcam Alert and Email Notification App

A motion detection application using OpenCV that tracks movement via a webcam. When motion is detected, the app sends an email notification with an attached image.

## Features ##
- Real-time motion detection using a webcam.
- Automated email alerts when motion is detected.
- Captured image attached in the email.
- Filters small/irrelevant movements to reduce false alerts.
- Automatically deletes old images to save storage.
- Runs continuously until manually stopped.


## How It Works ##
1. The webcam continuously captures frames and processes them.
2. It detects motion by comparing the current frame with a reference frame.
3. If movement is detected:
   - A bounding box is drawn.
   - A snapshot is saved.
   - An email notification is sent with the captured image.
4. The app runs until the user presses "q" to quit.

## Configuration ##
1. You can modify the following settings in main.py:
2. Threshold values to adjust motion sensitivity.
3. Contour area filtering to ignore small objects.
4. Email settings to change sender/receiver details.

## Future Improvements ##
1. Face detection instead of general motion detection.
2. WhatsApp or Telegram alerts for real-time notifications.
3. Cloud storage integration (Google Drive).
4. GUI interface for easier interaction.

⭐ If you found this project useful, give it a star on GitHub! 🎯
