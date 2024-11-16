import asyncio

import cv2
from app.camera import Camera
from app.exceptions.camera_errors import GrabFrameException


class QRScanner:
    FAILED_TO_GRAB_FRAME = 'Failed to grab frame'

    def __init__(self):
        self.camera = Camera()
        self.qr_detector = cv2.QRCodeDetector()

    async def detect_and_decode(self, frame) -> str:
        data, _, _ = self.qr_detector.detectAndDecode(frame)
        return data

    async def scan(self, duration: int = 10) -> str | None:
        end_time = asyncio.get_event_loop().time() + duration

        while asyncio.get_event_loop().time() < end_time:
            frame = await self.camera.get_frame()

            if frame is None:
                raise GrabFrameException(self.FAILED_TO_GRAB_FRAME)

            data = await self.detect_and_decode(frame)

            if data:
                return data

        return None

    async def release(self) -> None:
        await self.camera.release()
