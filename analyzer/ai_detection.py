import streamlit as st
from PIL import Image


@st.cache_resource(show_spinner=False)
def _get_detector():
    """
    Load the AI image detector once and cache it across Streamlit reruns.
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

    Returns the model's classification results.
    """

    if image is None:
        return []

    try:
        if not isinstance(image, Image.Image):
            image = Image.open(image)

        image = image.convert("RGB")

        detector = _get_detector()

        results = detector(image)

        return results

    except Exception as e:
        print(f"AI detector error: {e}")
        return []


def detect_ai_video(frames):
    """
    Video AI detection is intentionally unavailable.

    The installed detector is an image model and has not been
    validated as a video-level detector.
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