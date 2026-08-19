import numpy as np
from functools import lru_cache


@lru_cache(maxsize=1)
def _get_reader():
    """Initialize OCR only when an uploaded image needs it."""
    import easyocr
    return easyocr.Reader(["en"], gpu=False)


def extract_text(image):
    """
    Extract text from an image using EasyOCR.
    """

    image_array = np.array(image)

    results = _get_reader().readtext(image_array)

    extracted_text = []

    for detection in results:
        text = detection[1]
        confidence = detection[2]

        extracted_text.append({
            "text": text,
            "confidence": float(confidence)
        })

    return extracted_text
