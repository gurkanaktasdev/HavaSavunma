import time
import socket
import cv2
import numpy as np
import random
import sys


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_adress = ('127.0.0.1',5005)
cam = cv2.VideoCapture(0)
i = 0
x1,x2 =50,100
y1,y2 =50,100
angle = None
for raw in sys.stdin:   # C#tarafından process sınıfının standardInput özelliği ile yollanan(sadece dosya başlatırken 1 defa veri gelir) veriyi alak için bu for bloğu 
    raw = raw.strip()
    if angle is None:
        angle = raw 
    elif raw == "quit":
        raw = raw.replace("quit", "")
        break
    else: 
        break

while True:

    i +=1
    if i%30 == 0:
        x1 = random.randint(1,450)
        x2 = random.randint(1,450)
        y1 = random.randint(1,450)
        y2 = random.randint(1,450)

    ret,frame = cam.read()
    cv2.putText(frame,f"Recieved Angle :{angle}",(30,50),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,255,0),1)
    cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0))
    _, buffer = cv2.imencode('.jpg', frame,[int(cv2.IMWRITE_JPEG_QUALITY), 30])
    byte_frame = buffer.tobytes()
    try:
        sock.sendto(byte_frame, server_adress)
    except OSError as e:
        print("hata")
        print(e)
        time.sleep(0.1)

    cv2.imshow("deneme",frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
sock.close()


