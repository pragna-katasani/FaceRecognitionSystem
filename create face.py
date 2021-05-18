import cv2
import sys
import os
cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
kk=1
os.chdir('train_faces/s4')
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(200, 200),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
        framex=frame[y:y+h, x:x+w]
        framex= cv2.resize(framex, (92, 112))
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite(str(kk)+".jpg",framex)
            print 'Train face-' + str(kk)
            kk=kk+1
            if(kk==11):
                kk=1
        
        
    # Display the resulting frame
    cv2.imshow('Video', frame)
    


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
