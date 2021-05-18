from sklearn.decomposition import PCA as RandomizedPCA
import numpy as np
import glob
import cv2
import math
import os.path
import string
import time
import RPi.GPIO as GPIO
import httplib, urllib, urllib2
import subprocess
import urllib2
import cookielib
from getpass import getpass
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from time import sleep
from datetime import datetime





def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display




  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)





file = open("/home/pi/data_log.csv", "a")
i=0
if os.stat("/home/pi/data_log.csv").st_size == 0:
        file.write("Time,P_ID\n")



# Define GPIO to LCD mapping
LCD_RS = 19
LCD_E  = 13
LCD_D4 = 6
LCD_D5 = 5
LCD_D6 = 11
LCD_D7 = 9

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

buz=23

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT) # RS
GPIO.setup(LCD_D4, GPIO.OUT) # DB4
GPIO.setup(LCD_D5, GPIO.OUT) # DB5
GPIO.setup(LCD_D6, GPIO.OUT) # DB6
GPIO.setup(LCD_D7, GPIO.OUT) # DB7

GPIO.setup(26, GPIO.OUT)
GPIO.setup(buz, GPIO.OUT)

  # Initialise display
lcd_init()
lcd_byte(0x01,LCD_CMD)
lcd_string("   WELCOME",LCD_LINE_1)
lcd_string("Intializing..",LCD_LINE_2)



pwm = GPIO.PWM(26, 75)
pwm.start(5)
GPIO.output(buz,False)


time.sleep(2)
cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)






#function to get ID from filename
def ID_from_filename(filename):
    part = string.split(filename, '/')
    return part[1].replace("s", "")
 
#function to convert image to right format
def prepare_image(filename):
    img_color = cv2.imread(filename)
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_RGB2GRAY)
    img_gray = cv2.equalizeHist(img_gray)
    return img_gray.flat







def send_an_email():  
    toaddr = 'pragnakatasani.engg@gmail.com'      # To id 
    me = 'prasanthinimmala95@gmail.com'          # your id
    subject = "picture"              # Subject
  
    msg = MIMEMultipart()  
    msg['Subject'] = subject  
    msg['From'] = me  
    msg['To'] = toaddr  
    msg.preamble = "test "   
    #msg.attach(MIMEText(text))  
  
    part = MIMEBase('application', "octet-stream")  
    part.set_payload(open("image.jpg", "rb").read())  
    encoders.encode_base64(part)  
    part.add_header('Content-Disposition', 'attachment; filename="image.jpg"')   # File name and format name
    msg.attach(part)  
  
    try:  
       s = smtplib.SMTP('smtp.gmail.com', 587)  # Protocol
       s.ehlo()  
       s.starttls()  
       s.ehlo()  
       s.login(user = 'prasanthinimmala95@gmail.com', password = 'balajiprasanthi')  # User id & password
       #s.send_message(msg)  
       s.sendmail(me, toaddr, msg.as_string())  
       s.quit()  
    #except:  
    #   print ("Error: unable to send email")    
    except SMTPException as error:  
          print ("Error")                # Exception
  
send_an_email() 







IMG_RES = 92 * 112 # img resolution
NUM_EIGENFACES = 10 # images per train person
NUM_TRAINIMAGES = 110 # total images in training set

#loading training set from folder train_faces
folders = glob.glob('train_faces/*')
 
# Create an array with flattened images X
# and an array with ID of the people on each image y
cnt=0

duty = 20 / 10.0 + 2.5
pwm.ChangeDutyCycle(duty)

ss=0

lcd_string("PLS SHOW UR FACE",LCD_LINE_2)
while (1):


    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(200, 200),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    kk=0
    framex=frame
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        framex=frame[y:y+h, x:x+w]
        framex= cv2.resize(framex, (92, 112))
        kk=1

    if(kk==1):
        ss=ss+1


        
#        cv2.imshow('video',framex) 

        
##    cv2.imshow('video',framex) 

#    if (((cv2.waitKey(1) & 0xFF == ord('s')))):

    if(ss==35):
            lcd_string("FACE DETECTED    ",LCD_LINE_2)
            ss=0
            cv2.imwrite("test_faces/test.jpg",framex)
            cv2.imwrite("image.jpg",frame)
            line = "Captured image"
            X = np.zeros([NUM_TRAINIMAGES, IMG_RES], dtype='int8')
            y = []

            # Populate training array with flattened imags from subfolders of train_faces and names
            c = 0
            for x, folder in enumerate(folders):
                train_faces = glob.glob(folder + '/*')
                for i, face in enumerate(train_faces):
                    X[c,:] = prepare_image(face)
                    y.append(ID_from_filename(face))
                    c = c + 1

            # perform principal component analysis on the images
            pca = RandomizedPCA(n_components=NUM_EIGENFACES, whiten=True).fit(X)
            X_pca = pca.transform(X)

            # load test faces (usually one), located in folder test_faces
            
            test_faces = glob.glob('test_faces/*')

            # Create an array with flattened images X
            X = np.zeros([len(test_faces), IMG_RES], dtype='int8')
         
            # Populate test array with flattened imags from subfolders of train_faces 
            for i, face in enumerate(test_faces):
                X[i,:] = prepare_image(face)
         
            # run through test images (usually one)
            for j, ref_pca in enumerate(pca.transform(X)):
                distances = []
                # Calculate euclidian distance from test image to each of the known images and save distances
                for i, test_pca in enumerate(X_pca):
                    dist = math.sqrt(sum([diff**2 for diff in (ref_pca - test_pca)]))
                    distances.append((dist, y[i]))
         
                found_ID = min(distances)[1]
                print min(distances)[0]
                if((min(distances)[0] <1.2) and kk==1):
                    print "Identified (result: "+ str(found_ID) +" - dist - " + str(min(distances)[0])  + ")"
                    line = "Identified (result: "+ str(found_ID) +" - dist - " + str(min(distances)[0])
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame,str(found_ID), (30,30), font, 1, (255,0,0),2)
                    now = datetime.now()
                    file.write(str(now)+","+str(found_ID)+"\n")
                    file.flush()

#                    params = urllib.urlencode({'field1': str(found_ID),'key':'RRQ36WY55P4NLBNB'})
#                    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
#                    conn = httplib.HTTPConnection("api.thingspeak.com:80")
#                    conn.request("POST", "/update", params, headers)
#                    response = conn.getresponse()
                    #print response.status, response.reason#
#                    data = response.read()
                    #print data
#                    conn.close()

                    if(str(found_ID)=="1" or str(found_ID)=="2" or str(found_ID)=="3" or str(found_ID)=="4" or str(found_ID)=="5"):

                        lcd_string("AUTHORIZED .....  ",LCD_LINE_2)
                        print 'child found'
                        duty = 110 / 10.0 + 2.5
                        pwm.ChangeDutyCycle(duty)
                        time.sleep(5)
                        print 'next please'
                        duty = 20 / 10.0 + 2.5
                        pwm.ChangeDutyCycle(duty)
                        lcd_string("PLS SHOW UR FACE  ",LCD_LINE_2)

                    else:
                            lcd_string("UNAUTHORIZED .....",LCD_LINE_2)
                            print ("Not found")
                            line = "not found"
                            GPIO.output(buz,True)
                            time.sleep(2)
                            GPIO.output(buz,False)
                            lcd_string("PLS SHOW UR FACE  ",LCD_LINE_2)
                            

  
                elif(kk==1):
                    lcd_string("UNAUTHORIZED .....",LCD_LINE_2)
                    print ("missing child not found")
                    line = "missing child not found"
                    GPIO.output(buz,True)
                    time.sleep(2)
                    GPIO.output(buz,False)
                    lcd_string("PLS SHOW UR FACE  ",LCD_LINE_2)
                
##        # Display the resulting frame
##        
    cv2.imshow('Video1', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
video_capture.release()
cv2.destroyAllWindows()

