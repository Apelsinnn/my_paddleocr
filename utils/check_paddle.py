import paddle
from paddleocr import PaddleOCR

print(paddle.__version__)
print(paddle.is_compiled_with_cuda())
print(paddle.device.get_device())