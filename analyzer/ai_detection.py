from functools import lru_cache


@lru_cache(maxsize=1)
def _get_detector():
    """Load the large detector only when it is actually needed."""
    from transformers import pipeline
    return pipeline("image-classification", model="Organika/sdxl-detector")


def detect_ai_image(image):
    """
    Analyze an image for AI-generation indicators.

    Returns the model's classification results.
    """

    return _get_detector()(image)


def detect_ai_video(frames):
    """Report that no validated video detector is configured.

    ``Organika/sdxl-detector`` is an image model. Applying it to sampled
    frames creates misleading video-level results, so it must never be used
    as a video AI detector. Configure a separately evaluated video model
    before enabling automated video verdicts.
    """

    if not frames:
        return []

    return [{
        "label": "unavailable",
        "score": 0.0,
        "validated": False,
        "reason": (
            "Automated video AI detection is unavailable. The installed "
            "image detector is not validated for video and has been disabled "
            "to prevent misleading results."
        ),
    }]
