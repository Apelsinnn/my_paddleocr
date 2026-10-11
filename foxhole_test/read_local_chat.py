from dxcam import create
from typing import TYPE_CHECKING, Optional
from threading import Thread
from utils.image_convertation import crop_image

import numpy as np
import time
import cv2

if TYPE_CHECKING:
    from dxcam import DXCamera

print("=" * 200)


class FoxholeChatReader:
    """Пайплайн чтения чата игры foxhole в реальном времени."""

    def __init__(self):
        self._camera: Optional["DXCamera"] = None

    def _initialize_pipline(self):
        """Задаёт начальные настройки перед запуском основного пайплайна."""
        self._running = True
        self._camera = create(output_idx=0)
        self._camera.start(target_fps=10)

    def _capture_loop(self):
        """Получает кадры с экрана."""
        while self._running:
            frame = self._camera.grab()

            if frame is None:
                time.sleep(0.2)
                continue

            cropped_image = crop_image(frame)
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
