import hashlib

import imagehash
from PIL import Image
from io import BytesIO


def calculate_sha256(image_bytes):
    """Calculate SHA-256 hash of the original file."""

    return hashlib.sha256(image_bytes).hexdigest()


def calculate_phash(image_bytes):
    """Calculate perceptual hash of an image."""

    image = Image.open(BytesIO(image_bytes))

    return str(imagehash.phash(image))