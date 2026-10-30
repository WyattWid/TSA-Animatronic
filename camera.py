import os
import cv2
from pyzbar.pyzbar import decode
import numpy as np


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)  # Use self.cap

    def scan(self):
        ret = None
        frame = None
        self.cap.grab()
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame")
            return None  # Avoid using `break` here

        decoded_objects = decode(frame)
        if not decoded_objects:
            return None

        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            return qr_data  # Return the scanned QR code

        return None
    def get_frame(self):
        ret, frame1 = self.cap.read()
        if not ret:
            return None
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        return frame1
    def get_difference(self, frame1, frame2):
        if len(frame1.shape) == 3:  # If not already grayscale
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        if len(frame2.shape) == 3:  # If not already grayscale
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        frame1 = cv2.resize(frame1, (640, 480))
        frame2 = cv2.resize(frame2, (640, 480))
        frame_diff = cv2.absdiff(frame1, frame2)
        _, thresh = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)
        non_zero_count = np.count_nonzero(thresh)
        if non_zero_count < 100:  # Adjust this threshold based on your needs
            return True
        return False



