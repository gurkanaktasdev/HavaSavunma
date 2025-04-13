import cv2
import numpy as np


cam = cv2.VideoCapture(0)

while True:
    
    ret,frame = cam.read()

    if not ret:
        print("Görüntü alınamadı!")
        exit()
    frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])         # kırmızı için hsv de iki farklı aralık olduğu için her bir değer için iki adet yaptık .
    upper_red1 = np.array([5, 255, 255])
    lower_red2 = np.array([160, 120, 70])
    upper_red2 = np.array([172, 255, 255])
    mask_red1 = cv2.inRange(frame_hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(frame_hsv, lower_red2, upper_red2)
    mask_red = mask_red1 + mask_red2 

    lower_blue = np.array([85, 120,70])
    upper_blue = np.array([140, 255, 255])
    mask_blue = cv2.inRange(frame_hsv, lower_blue, upper_blue)

    mask_sum = mask_red + mask_blue

    contours, _ = cv2.findContours(mask_sum, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center_points = []
    # 6️⃣ Orta noktaları hesapla ve işaretle
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100:
            M = cv2.moments(cnt)
            if M["m00"] != 0:  # Alan sıfır değilse
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                center_points.append((cx, cy)) 
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)  # Orta noktayı kırmızı işaretle
    cv2.imshow("ana",frame)
    cv2.imshow("maks_red",mask_sum)
    center_points.clear()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()