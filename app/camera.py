import cv2
import numpy as np


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    async def get_frame(self) -> np.ndarray | None:
        ret, frame = self.cap.read()
        return frame if ret else None

    async def release(self):
        self.cap.release()
