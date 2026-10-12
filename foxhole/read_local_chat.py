from dxcam import create
from typing import TYPE_CHECKING, Optional
from threading import Thread
from utils.image_convertation import crop_image
from paddleocr import PaddleOCR

import numpy as np
import time
import cv2
import datetime

if TYPE_CHECKING:
    from dxcam import DXCamera

print("=" * 200)


class FoxholeChatReader:
    """Пайплайн чтения чата игры foxhole в реальном времени."""

    def __init__(self, ):
        self._camera: Optional["DXCamera"] = None
        self._captured_frame: np = None

    def _initialize_pipline(self):
        """Задаёт начальные настройки перед запуском основного пайплайна."""
        self._running = True
        self._camera = create(output_idx=0)
        self._camera.start(target_fps=10)

        self._ocr_model = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            ocr_version="PP-OCRv5",
            lang="ru",
            device="gpu:0",
        )

    def _is_frame_same(self, frame):
        """Проверяет что новый кадр отличается от предыдущего."""
        previous = cv2.cvtColor(self._captured_frame, cv2.COLOR_RGB2GRAY)
        current = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        diff = cv2.absdiff(current, previous)
        threshold = 15
        changed_ratio = 0.10

        _, mask = cv2.threshold(
            diff,
            threshold,
            255,
            cv2.THRESH_BINARY,
        )

        ratio = cv2.countNonZero(mask) / mask.size

        return bool(ratio >= changed_ratio)


    def _capture_loop(self):
        """Получает кадры с экрана."""
        first_frame = self._camera.grab()
        self._captured_frame = crop_image(first_frame)

        while self._running:
            frame = self._camera.grab()
            cropped_image = crop_image(frame)

            if frame is None or not self._is_frame_same(cropped_image):
                time.sleep(0.4)
                continue

            self._captured_frame = cropped_image
            result = self._ocr_model.predict(cropped_image)

            for res in result:
                for text, score, box in zip(
                        res["rec_texts"],
                        res["rec_scores"],
                        res["rec_boxes"],
                ):
                    if "local" in text.lower() and "all" in text.lower():
                        print()
                        print(text)
                        print(datetime.datetime.now(tz=None))

            cv2.imshow(winname="Captured frame", mat=cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR))

            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                self._running = False
                self._camera.stop()
                break

    def live_reading(self):
        """Запускает чтение чата игры на экране."""
        self._initialize_pipline()
        self._capture_loop()


reader = FoxholeChatReader()
reader.live_reading()
