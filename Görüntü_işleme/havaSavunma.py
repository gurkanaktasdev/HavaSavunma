
import cv2
import numpy as np


birler_x = []
birler_y = []
def redMasked(y, x):
    for i in range(y - 1):
        for k in range(x - 1):
            if mask_red[i, k] == 255:
                birler_x.append(k)
                birler_y.append(i)
    birler_y.sort()
    birler_x.sort()
    return [birler_x[0], birler_y[0], birler_x[-1], birler_y[-1]]

birler1_x = []
birler1_y = []
def blueMasked(y, x):
    for i in range(y - 1):
        for k in range(x - 1):
            if mask_blue[i, k] == 255:
                birler1_x.append(k)
                birler1_y.append(i)
    birler1_y.sort()
    birler1_x.sort()
    return [birler1_x[0], birler1_y[0], birler1_x[-1], birler1_y[-1]]


cam = cv2.VideoCapture(0)

while True:

    ret,frame = cam.read()

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

    """
    blurred = cv2.GaussianBlur(mask_sum, (5, 5), 0)

    kernel = np.ones((5, 5), np.uint8)
    clean_mask = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel)  # Küçük boşlukları kapatır
    clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_OPEN, kernel)  # Gürültüleri temizler

   

    contours, hierarchy = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    """
    y,x,z=frame.shape 

    try:
        d_kor = redMasked(y,x)
        cv2.rectangle(frame, (d_kor[0], d_kor[1]), (d_kor[2], d_kor[3]), (0, 255, 0), 4)
    except:
        print("filtreleme basarisiz")

    try:
        d_kor1 = blueMasked(y,x)
        cv2.rectangle(frame, (d_kor1[0], d_kor1[1]), (d_kor1[2], d_kor1[3]), (0, 255, 0), 4)
    except:
        print("filtreleme basarisiz")   

    cv2.imshow("ana",frame)
    cv2.imshow("mask_blue",mask_blue )
    cv2.imshow("maks_red",mask_red)
    

    birler_x.clear()
    birler_y.clear()
    birler1_x.clear()
    birler1_y.clear()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()