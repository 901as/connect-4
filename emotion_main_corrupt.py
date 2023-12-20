import cv2
from deepface import DeepFace

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not video.isOpened():
    raise IOError("Cannot open webcam")

def detect_emotion():
    _, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for x, y, w, h in face:
        image = cv2.rectangle(frame, (x, y), (x + w, y + h), (89, 2, 236), 1)
        try:
            analyze = DeepFace.analyze(frame, actions=['emotion'])
            return analyze
        except:
            print('no face')
            return None

    cv2.imshow('video', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        video.release()
        cv2.destroyAllWindows()