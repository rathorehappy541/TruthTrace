def calculate_risk_score(
    metadata,
    ocr_results,
    image_bytes,
    ai_results=None
):
    """
    Calculate an investigative risk score.

    This score combines several technical indicators.
    It is NOT proof that an image is fake or manipulated.
    """

    score = 0
    findings = []

    # ========================================================
    # 1. METADATA
    # ========================================================

    useful_metadata = [
        key
        for key in metadata
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


    # ========================================================
    # 2. OCR
    # ========================================================

    if ocr_results:

        average_confidence = (
            sum(
                result["confidence"]
                for result in ocr_results
            )
            / len(ocr_results)
        )

        if average_confidence < 0.60:

            score += 10

            findings.append(
                "OCR confidence is relatively low."
            )


    # ========================================================
    # 3. AI DETECTOR
    # ========================================================

    if ai_results:

        artificial_score = 0

        for result in ai_results:

            if (
                result.get("label", "").lower() == "artificial"
                and result.get("validated", True)
            ):

                artificial_score = result["score"]

        if artificial_score >= 0.90:

            score += 45

            findings.append(
                "AI detection model strongly favors "
                "the artificial classification."
            )

        elif artificial_score >= 0.70:

            score += 30

            findings.append(
                "AI detection model moderately favors "
                "the artificial classification."
            )

        elif artificial_score >= 0.50:

            score += 15

            findings.append(
                "AI detection model shows some "
                "artificial-image likelihood."
            )


    # ========================================================
    # 4. FILE SIZE
    # ========================================================

    if len(image_bytes) < 50_000:

        score += 5

        findings.append(
            "The uploaded file is relatively small."
        )


    # ========================================================
    # LIMIT SCORE
    # ========================================================

    score = min(score, 100)


    # ========================================================
    # RISK LEVEL
    # ========================================================

    if score < 20:

        level = "Low"

    elif score < 50:

        level = "Moderate"

    else:

        level = "High"


    return score, level, findings
