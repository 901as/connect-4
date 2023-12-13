import cv2
import numpy as np
from keras.models import load_model

# Load the model
model = load_model('D:\!dev\connect-4\model.h5')

# Define the list of labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Start the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert color to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the face
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        face = gray[y:y + h, x:x + w]
        face = cv2.resize(face, (48, 48))
        face = np.expand_dims(face, -1)
        face = np.expand_dims(face, 0)

        # Predict the emotion
        emotion = model.predict(face)[0]
        max_index = np.argmax(emotion)
        emotion_label = emotion_labels[max_index]

        # Display the emotion
        cv2.putText(frame, emotion_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    # Display the resulting frame
    cv2.imshow('Emotion Recognition', frame)

    # Break the loop by clicking q to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
