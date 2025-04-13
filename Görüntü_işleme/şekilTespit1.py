import cv2

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()

    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    canny_img = cv2.Canny(gray_frame,80,150)

    contours,_ = cv2.findContours(canny_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)         # bulduğu area pixel biriminden büyükse çizer 
        if area > 200:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True) #bu approx bize cismin köşe sayısını verecek
            cornerCount = len(approx)

           # x,y,w,h = cv2.boundingRect(approx )    #x,y değerleri şeklin etrafına çizdiği dikdörtgenin sol üst köşe konumu w ise genişlik h ise yüksekliktir
           # cv2.putText(img,str(area),(x+10,y+10),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            if cornerCount > 15  and cornerCount <50:
              cv2.drawContours(frame,cnt,-1,(0,255,0),2)

    cv2.imshow("canny",canny_img)
    cv2.imshow("paint",frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()