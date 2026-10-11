from paddleocr import PaddleOCR
from utils.image_convertation import crop_image
import cv2
import numpy as np

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    ocr_version="PP-OCRv5",
    lang="ru",
    device="gpu:0",
)

image_path = r"D:\My_folder\py_projects\my_paddleocr\images\one_frame.png"

my_image = cv2.imread(image_path)
image_to_predict = crop_image(my_image)
result = ocr.predict(image_to_predict)
white_canvas = np.full(image_to_predict.shape, 255, dtype=np.uint8)

for res in result:
    for text, score, box in zip(
            res["rec_texts"],
            res["rec_scores"],
            res["rec_boxes"],
    ):
        x1, y1, x2, y2 = map(int, box)
        # label = f"{text} ({score:.2f})"
        # print(text)

        if "local" in text.lower() and "all" in text.lower():
            print(text)

        cv2.putText(
            white_canvas,
            # label,
            text,
            (x1, y1 + 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )

cv2.imshow("Original", image_to_predict)
cv2.imshow("White_canvas", white_canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
