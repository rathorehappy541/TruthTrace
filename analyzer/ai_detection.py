import streamlit as st
from PIL import Image


@st.cache_resource(show_spinner=False)
def _get_detector():
    """
    Load the AI image detector once and reuse it.
    """

    from transformers import pipeline

    detector = pipeline(
        "image-classification",
        model="Organika/sdxl-detector",
        device=-1,
    )

    return detector


def detect_ai_image(image):
    """
    Analyze an image for AI-generation indicators.
    """

    if image is None:
        return []

    try:
        if not isinstance(image, Image.Image):
            image = Image.open(image)

        # Convert to RGB
        image = image.convert("RGB")

        # Prevent extremely large images from consuming excessive memory
        max_size = 1600

        if max(image.size) > max_size:
            image.thumbnail((max_size, max_size))

        detector = _get_detector()

        results = detector(
            image,
            top_k=2
        )

        return results

    except Exception as e:
        print(f"AI detector error: {e}")
        return []


def detect_ai_video(frames):
    """
    Video AI detection is intentionally unavailable.
    """

    if not frames:
        return []

    return [{
        "label": "unavailable",
        "score": 0.0,
        "validated": False,
        "reason": (
            "Automated video AI detection is unavailable. "
            "The installed image detector is not validated "
            "for video."
        ),
    }]
