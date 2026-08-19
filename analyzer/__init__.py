def calculate_risk_score(metadata, ocr_results, image_bytes):
    """
    Calculate an investigative risk score.

    This is NOT a definitive authenticity detector.
    It combines simple forensic indicators for triage.
    """

    score = 0
    findings = []

    # --------------------------------
    # METADATA
    # --------------------------------

    useful_metadata = [
        key for key in metadata
        if key not in [
            "Filename",
            "Format",
            "Width",
            "Height",
            "Mode"
        ]
    ]

    if not useful_metadata:
        score += 10
        findings.append(
            "No additional EXIF metadata was available."
        )

    # --------------------------------
    # OCR
    # --------------------------------

    if ocr_results:

        average_confidence = sum(
            result["confidence"]
            for result in ocr_results
        ) / len(ocr_results)

        if average_confidence < 0.60:
            score += 10
            findings.append(
                "OCR confidence is relatively low."
            )

    # --------------------------------
    # FILE SIZE
    # --------------------------------

    if len(image_bytes) < 50_000:

        score += 5

        findings.append(
            "The uploaded file is relatively small."
        )

    # --------------------------------
    # LIMIT SCORE
    # --------------------------------

    score = min(score, 100)

    # --------------------------------
    # INTERPRETATION
    # --------------------------------

    if score < 20:

        level = "Low"

    elif score < 50:

        level = "Moderate"

    else:

        level = "High"

    return score, level, findings