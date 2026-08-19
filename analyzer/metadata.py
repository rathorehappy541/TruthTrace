from io import BytesIO

from PIL import Image
from PIL.ExifTags import TAGS


def extract_metadata(image_bytes, filename="Unknown"):
    """Extract useful image metadata and EXIF information."""

    image = Image.open(BytesIO(image_bytes))

    metadata = {
        "Filename": filename,
        "Format": image.format or "Unknown",
        "Width": image.width,
        "Height": image.height,
        "Mode": image.mode,
    }

    exif_data = image.getexif()

    if exif_data:
        for tag_id, value in exif_data.items():

            tag_name = TAGS.get(tag_id)

            # Ignore unknown/private EXIF tags
            if tag_name is None:
                continue

            # Ignore internal EXIF pointer information
            if tag_name in ["ExifOffset", "GPSInfo"]:
                continue

            # Avoid displaying huge binary values
            if isinstance(value, bytes):
                continue

            try:
                metadata[tag_name] = str(value)
            except Exception:
                continue

    return metadata