
import cv2

cap = cv2.VideoCapture('0 ! videoconvert ! appsink')

while True:
    try:
        ret, frame = cap.read()
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    except Exception as e:
        print(e)
        break
cap.release()
cv2.destroyAllWindows()
