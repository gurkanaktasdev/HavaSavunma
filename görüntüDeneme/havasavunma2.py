import time
import socket
import cv2
import numpy as np
import random
import sys
from multiprocessing import Process,Queue



def ObjectDetect(queue):

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server_adress = ('127.0.0.1',5005)
    cam = cv2.VideoCapture(0)
    i = 0
    x1,x2 =50,100
    y1,y2 =50,100
    Hedef_piksel = []
    
    while True:
    
        i +=1
        if i%30 == 0:       #burada sanki object detection yapmışımda bana balonun hedef piksel değerleri verilmiş olduğuunu varsayıyorum.
            x1 = random.randint(1,450)
            x2 = random.randint(1,450)
            y1 = random.randint(1,450)
            y2 = random.randint(1,450)
        Hedef_piksel = [x1,x2,y1,y2]
        queue.put(Hedef_piksel)
        print(f" kuyruk noyutu : {queue.qsize()}")
        ret,frame = cam.read()
        # cv2.putText(frame,f"Recieved Angle :{angle}",(30,50),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,255,0),1)
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


def ControlAlgo(angle,queue):
     frame_deneme = np.zeros((300, 400, 3), dtype=np.uint8)
    
     cv2.putText(frame_deneme, 
            angle,                # Yazı
            (50, 50),            # Başlangıç noktası (x,y)
            cv2.FONT_HERSHEY_SIMPLEX, 
            2,                    # Font büyüklüğü
            (255, 255, 255),      # Renk: Beyaz (BGR)
            3,                    # Kalınlık
            cv2.LINE_AA)          # Çizgi tipi (antialiasing)
     Gelen_hedef = []
     while True:
        frame_de = np.zeros((300, 400, 3), dtype=np.uint8)
        try:
            Gelen_hedef = queue.get()
            cv2.putText(frame_de, 
                Gelen_hedef[0],                # Yazı
                (50, 100),            # Başlangıç noktası (x,y)
                cv2.FONT_HERSHEY_SIMPLEX, 
                2,                    # Font büyüklüğü
                (255, 255, 255),      # Renk: Beyaz (BGR)
                3,                    # Kalınlık
                cv2.LINE_AA)          # Çizgi tipi (antialiasing)
        except:
            print("kuyrukdan veriyi alamadim")    
        

        cv2.imshow("Hedef",frame_de)
            
     

     


def MainFunc():
    q = Queue()

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

    p1 = Process(target=ObjectDetect,args=(q,))
    p2 =Process(target=ControlAlgo,args=(angle,q))

    p1.start()
    p2.start()

    p1.join()
    p2.join()



if __name__ == "__main__":     #  bu satır olmazsa ortalık 56 olur(sonsuz döngü vs)
    MainFunc()    