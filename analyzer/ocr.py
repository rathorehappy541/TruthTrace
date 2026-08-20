import numpy as np
from functools import lru_cache


@lru_cache(maxsize=1)
def _get_reader():
    import easyocr

    return easyocr.Reader(
        ["en"],
        gpu=False,
        verbose=False
    )


def extract_text(image):

    if image is None:
        return []

    image_array = np.array(image)

    reader = _get_reader()

    results = reader.readtext(
        image_array,
        detail=1
    )

    extracted_text = []

    for detection in results:

        if len(detection) < 3:
            continue

        text = detection[1]
        confidence = detection[2]

        extracted_text.append({
            "text": text,
            "confidence": float(confidence)
        })

    return extracted_text
