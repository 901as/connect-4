import cv2
import numpy as np
from keras.models import model_from_json
from connect_4_ai import Game, GUI

# Load the model
json_file = open('fer.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("fer.h5")
print("Loaded model from disk")

# Set image resizing parameters
WIDTH = 48
HEIGHT = 48
labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Load the cascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Open webcam
cap = cv2.VideoCapture(0)

# Start game data structure
game_board = GUI.getNewBoard()
game = Game(game_board)

while True:
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Crop and resize image to fit model input
        roi_gray = gray[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
        cv2.normalize(cropped_img, cropped_img, alpha=0, beta=1, norm_type=cv2.NORM_L2, dtype=cv2.CV_32F)

        # Predict emotion
        yhat = loaded_model.predict(cropped_img)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.putText(frame, labels[int(np.argmax(yhat))], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)

        # Adjust AI difficulty based on emotion
        if labels[int(np.argmax(yhat))] == 'Happy':
            game.d = 7  # High difficulty
        else:
            game.d = 4  # Lower difficulty

    # Display the frame with bounding box and emotion
    cv2.imshow('Emotion', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Play Connect 4 game
    if not game.is_game_over():
        game.next_turn()
        GUI.drawBoard(game.board)
        GUI.updateDisplay()

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()