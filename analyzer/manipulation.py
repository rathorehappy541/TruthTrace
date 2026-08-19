from io import BytesIO

from PIL import Image, ImageChops, ImageEnhance


def create_ela_image(image):
    """
    Perform a basic Error Level Analysis (ELA).

    Accepts a PIL Image and returns an ELA PIL Image.
    """

    # Make sure we have a PIL image
    if not isinstance(image, Image.Image):
        raise TypeError(
            "create_ela_image() expects a PIL Image"
        )

    # Convert to RGB
    original = image.convert("RGB")

    # Save the image again as JPEG in memory
    buffer = BytesIO()

    original.save(
        buffer,
        format="JPEG",
        quality=90
    )

    buffer.seek(0)

    recompressed = Image.open(
        buffer
    ).convert("RGB")

    # Calculate pixel differences
    difference = ImageChops.difference(
        original,
        recompressed
    )

    # Find the maximum difference
    extrema = difference.getextrema()

    max_difference = max(
        channel_max
        for channel_min, channel_max in extrema
    )

    if max_difference == 0:
        max_difference = 1

    # Increase visibility
    scale = 255.0 / max_difference

    ela_image = ImageEnhance.Brightness(
        difference
    ).enhance(scale)

    return ela_image