import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
while (True):
    ret, frame = cap.read()
    cv2.imshow("",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        os._exit(0)
vid.release()
cv2.destroyAllWindows()
