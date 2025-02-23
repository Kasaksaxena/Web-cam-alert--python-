import smtplib #provide tools to send emails using SIMPLE MAIL TRANSFER PROTOCOL(SMTP)
import imghdr # use to determine type of image(eg jpeg,png)
from email.message import EmailMessage # provides esy way to contruct email messages including attachments
PASSWORD="gwld jyer rkei ctah"
SENDER="kasaksaxena6@gmail.com"
RECIEVER="kasaksaxena6@gmail.com"
def send_email(image_path):
    print("email has sent")
    email_message=EmailMessage()
    email_message["Subject"]="New customer showed up!"
    email_message.set_content("Hey, we just saw a new customer!")
     
    with open(image_path,"rb") as file :
        content=file.read()
    
    #maintype="image"- species that this is image attachment
    #subtype=imghdr.what(None,content)- automatically detects img format   
    email_message.add_attachment(content,maintype="image",subtype=imghdr.what(None,content))  
       
    
    gmail=smtplib.SMTP("smtp.gmail.com",587)
    gmail.ehlo() # send EHLO(Extended Hello) Command to server 
    gmail.starttls()# upgrade the connection to a secure encrypted TLS connection
    gmail.login(SENDER,PASSWORD)
    gmail.sendmail(SENDER,RECIEVER,email_message.as_string())
    gmail.quit()
    print(" email end")
    
if __name__=="__main__":
    send_email(image_path="images/19.png")    