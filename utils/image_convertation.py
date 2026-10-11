

def crop_image(image):
    """Точно обрезает окно чата фоксхолла."""
    h, w = image.shape[:2]
    x1 = w - 543
    y1 = h - 350
    x2 = w - 33
    y2 = h - 74

    return image[y1:y2, x1:x2]