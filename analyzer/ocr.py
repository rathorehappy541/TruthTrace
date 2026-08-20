import numpy as np
import streamlit as st


@st.cache_resource
def _get_reader():
    """Load EasyOCR once and reuse it."""
    import easyocr

    return easyocr.Reader(
        ["en"],
        gpu=False,
        verbose=False
    )


def extract_text(image):
    """
    Extract text from an image using EasyOCR.
    """

    image_array = np.array(image)

    reader = _get_reader()

    results = reader.readtext(image_array)

    extracted_text = []

    for detection in results:
        text = detection[1]
        confidence = detection[2]

        extracted_text.append({
            "text": text,
            "confidence": float(confidence)
        })

    return extracted_text
