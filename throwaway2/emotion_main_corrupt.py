import cv2
from deepface import DeepFace

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not video.isOpened():
    raise IOError("Cannot open webcam")

def display_webcam():
    while True:
        _, frame = video.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (89, 2, 236), 1)
            try:
                analyze = DeepFace.analyze(frame, actions=['emotion'])
                emotion = analyze['dominant_emotion']
                cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            except Exception as e:
                print(f"Error: {e}")

        cv2.imshow('Emotion Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def get_emotion_data():
    _, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        try:
            analyze = DeepFace.analyze(frame, actions=['emotion'])
            return analyze
        except Exception as e:
            print(f"Error: {e}")
            return {'emotion': {'happy': 0, 'sad': 0}, 'face_confidence': 0}
