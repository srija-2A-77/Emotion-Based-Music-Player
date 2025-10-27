import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Could not open webcam")
else:
    print("✅ Webcam opened! Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("Test Camera - Press Q to quit", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
