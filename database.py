import os
import time 
from time import sleep
from datetime import datetime

file = open("/home/pi/faceattendancerpi/data_log.csv", "a")
i=0
if os.stat("/home/pi/faceattendancerpi/data_log.csv").st_size == 0:
        file.write("Time,Sensor1,Sensor2,Sensor3,Sensor4,Sensor5\n")
while True:
        i=i+1
        now = datetime.now()
        file.write(str(now)+","+str(i)+","+str(-i)+","+str(i-10)+","+str(i+5)+","+str(i*i)+"\n")
        file.flush()
        time.sleep(5)
        file.close()
