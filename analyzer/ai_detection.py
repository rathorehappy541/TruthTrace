from PIL import Image


def detect_ai_image(image):
    """
    AI detection is temporarily disabled on the lightweight
    Streamlit deployment to prevent memory-related crashes.
    """

    if image is None:
        return []

    return []


def detect_ai_video(frames):
    """
    Video AI detection is unavailable.
    """

    if not frames:
        return []

    return [{
        "label": "unavailable",
        "score": 0.0,
        "validated": False,
        "reason": "AI video detection is unavailable."
    }]
