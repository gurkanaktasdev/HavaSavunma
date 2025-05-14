import cv2
import numpy as np

# Kamera veya görüntü dosyasını aç
cam = cv2.VideoCapture(0)  # 0, webcam'i temsil eder

while True:
    ret, frame = cam.read()

    if not ret:
        print("Kamera hatası!")
        break

    # Görüntüyü gri tonlamaya çevir
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray) 
    # Görüntüyü bulanıklaştır (gürültüyü azaltmak için)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)

    # Kenarları tespit et (Canny Edge Detection)
    edges = cv2.Canny(blurred,50, 150)

    # Daireleri tespit et (Hough Circle Transform)
    circles = cv2.HoughCircles(edges,
                               cv2.HOUGH_GRADIENT, dp=1, minDist=30,
                               param1=100, param2=30, minRadius=20, maxRadius=200)

    # Eçizim aşaması 
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")  # Dairelerin koordinatlarını al
        for (x, y, r) in circles:               # burda dönen x,y değerleri çemberin x ve y kordinatları r ise yarıçapıdır 
            # Dairenin çevresini çiz
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            # Dairenin merkezini kırmızı ile işaretle
            cv2.circle(frame, (x, y), 5, (0, 0, 255), 3)

    # Sonuçları göster
    cv2.imshow("Balon ve Yuvarlak Tespiti", frame)
    cv2.imshow("Kenarlar", edges)

    # 'q' tuşuna basarak çıkış yap
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak ve pencereyi kapat
cam.release()
cv2.destroyAllWindows()
