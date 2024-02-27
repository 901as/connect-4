#!/usr/bin/env python3
# Jonathan De Leon && Ethan Beaver
# CPTR 430 Artificial Intelligence
# Final Project
# June 6, 2018
#
# Problem:
# Create a Connect Four game and implement an AI bot that uses minimax algorithm with alpha-beta pruning
#
# References
# GUI was created by AI Sweigart; we did some code refactoring and connected our algorithm/classes to the GUI
# http://inventwithpython.com/blog/2011/06/10/new-game-source-code-four-in-a-row/

from fourInARowGUI import fourInARowGUI as GUI
import cv2
from deepface import DeepFace
import tkinter as tk

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not video.isOpened():
    raise IOError("Cannot open webcam")

class DebugWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Debug Info")
        self.emotion_label = tk.Label(self.window, text="Emotion: ")
        self.emotion_label.pack()
        self.depth_label = tk.Label(self.window, text="Depth: ")
        self.depth_label.pack()

    def update_emotion(self, emotion):
        self.emotion_label["text"] = f"Emotion: {emotion}"

    def update_depth(self, depth):
        self.depth_label["text"] = f"Depth: {depth}"

debug_window = DebugWindow()

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

infinity = float('inf')
def calculate_sadness(emotion_data):
    sadness_level = 0
    if emotion_data == 'sad':
        sadness_level = 1

    return sadness_level

def adjust_difficulty_based_on_emotion(self):
    emotion_data = get_emotion_data()  # Assuming this function fetches the current emotion data
    sadness_level = calculate_sadness(emotion_data)
    self.ai_search_depth = max(1,  7 - sadness_level)  # Adjust the depth based on sadness
    debug_window.update_depth(self.ai_search_depth)  # Update the debug window with the new depth


class Game:
    AI = -1
    PLAYER = 0

    def __init__(self, game_board):
        self.current_state = State(0, 0)
        self.turn = self.AI
        self.first = self.turn
        self.board = game_board
        self.ai_search_depth = 7

    def adjust_difficulty_based_on_emotion(self):
        # TODO: Implement this method
        pass

    def make_move(self, column):
        # Implement your move logic here
        pass

    def is_over(self):
        # Check if the game is over
        # Return True if the game is over, False otherwise
        pass

    def switch_turn(self):
        # Switch the turn between the AI and the player
        self.turn = ~self.turn

    def play(self):
        while not self.is_over():
            if self.turn == self.AI:
                self.adjust_difficulty_based_on_emotion()
                # Make the AI's move
                self.make_move(some_column)
            else:
                # Get the player's move
                column = get_player_move()
                self.make_move(column)

            self.switch_turn()

if __name__ == "__main__":
    print("Welcome to Connect Four!")
    display_webcam() # Start displaying the webcam feed
    debug_window.window.mainloop() # Start the debug window
    game = Game(some_game_board)
    game.play()