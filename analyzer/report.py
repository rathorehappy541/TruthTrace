from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


def generate_pdf_report(
    evidence_record,
    metadata,
    ocr_results,
    ai_results,
    risk_score,
    risk_level,
    findings
):
    """
    Generate a professional TruthTrace PDF report.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TruthTraceTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "TruthTraceSubtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        spaceAfter=18
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "NormalText",
        parent=styles["Normal"],
        fontSize=9,
        leading=13
    )

    small_style = ParagraphStyle(
        "SmallText",
        parent=styles["Normal"],
        fontSize=8,
        leading=11
    )

    story = []

    # ====================================================
    # TITLE
    # ====================================================

    story.append(
        Paragraph(
            "TRUTHTRACE",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Digital Media Forensics Report",
            subtitle_style
        )
    )

    story.append(
        Paragraph(
            "AI Media Detection & Source Tracing",
            subtitle_style
        )
    )

    # ====================================================
    # EVIDENCE RECORD
    # ====================================================

    story.append(
        Paragraph(
            "1. Evidence Record",
            heading_style
        )
    )

    evidence_data = [
        ["Evidence ID", evidence_record.get("Evidence ID", "N/A")],
        ["Filename", evidence_record.get("Filename", "N/A")],
        [
            "File Size",
            f"{evidence_record.get('File Size', 0):,} bytes"
        ],
        [
            "Analysis Time",
            evidence_record.get("Analysis Time", "N/A")
        ],
        [
            "Status",
            evidence_record.get("Status", "N/A")
        ]
    ]

    evidence_table = Table(
        evidence_data,
        colWidths=[45 * mm, 125 * mm]
    )

    evidence_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(evidence_table)

    # ====================================================
    # DIGITAL FINGERPRINT
    # ====================================================

    story.append(
        Paragraph(
            "2. Digital Evidence Fingerprint",
            heading_style
        )
    )

    fingerprint_data = [
        [
            "SHA-256",
            evidence_record.get("SHA-256", "N/A")
        ],
        [
            "Perceptual Hash",
            evidence_record.get("pHash", "N/A")
        ]
    ]

    fingerprint_table = Table(
        fingerprint_data,
        colWidths=[45 * mm, 125 * mm]
    )

    fingerprint_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(fingerprint_table)

    # ====================================================
    # METADATA
    # ====================================================

    story.append(
        Paragraph(
            "3. File Metadata / EXIF",
            heading_style
        )
    )

    metadata_data = [
        ["Field", "Value"]
    ]

    for key, value in metadata.items():

        if isinstance(value, bytes):

            value = "<binary data>"

        metadata_data.append([
            str(key),
            str(value)
        ])

    if len(metadata_data) == 1:

        metadata_data.append([
            "Information",
            "No additional metadata found."
        ])

    metadata_table = Table(
        metadata_data,
        colWidths=[55 * mm, 115 * mm],
        repeatRows=1
    )

    metadata_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
        ])
    )

    story.append(metadata_table)

    # ====================================================
    # OCR
    # ====================================================

    story.append(
        Paragraph(
            "4. Text Detection / OCR",
            heading_style
        )
    )

    if ocr_results:

        for result in ocr_results:

            text = result.get(
                "text",
                ""
            )

            confidence = result.get(
                "confidence",
                0
            )

            story.append(
                Paragraph(
                    f"<b>{text}</b> "
                    f"— Confidence: "
                    f"{confidence * 100:.1f}%",
                    normal_style
                )
            )

            story.append(
                Spacer(1, 3)
            )

    else:

        story.append(
            Paragraph(
                "No readable text was detected.",
                normal_style
            )
        )

    # ====================================================
    # AI MEDIA ANALYSIS
    # ====================================================

    story.append(
        Paragraph(
            "5. AI Media Analysis",
            heading_style
        )
    )

    if ai_results:

        ai_data = [
            ["Classification", "Confidence"]
        ]

        for result in ai_results:

            label = result.get(
                "label",
                "Unknown"
            )

            confidence = result.get(
                "score",
                0
            )

            ai_data.append([
                str(label),
                f"{confidence * 100:.1f}%"
            ])

        ai_table = Table(
            ai_data,
            colWidths=[90 * mm, 80 * mm]
        )

        ai_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ALIGN", (1, 1), (1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
            ])
        )

        story.append(ai_table)

    else:

        story.append(
            Paragraph(
                "No AI detection result was available.",
                normal_style
            )
        )

    # ====================================================
    # RISK ASSESSMENT
    # ====================================================

    story.append(
        Paragraph(
            "6. Forensic Risk Assessment",
            heading_style
        )
    )

    risk_data = [
        [
            "Investigative Risk Score",
            f"{risk_score}/100"
        ],
        [
            "Risk Level",
            str(risk_level)
        ]
    ]

    risk_table = Table(
        risk_data,
        colWidths=[90 * mm, 80 * mm]
    )

    risk_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
        ])
    )

    story.append(risk_table)

    # ====================================================
    # TECHNICAL OBSERVATIONS
    # ====================================================

    story.append(
        Paragraph(
            "7. Technical Observations",
            heading_style
        )
    )

    if findings:

        for finding in findings:

            story.append(
                Paragraph(
                    f"• {finding}",
                    normal_style
                )
            )

            story.append(
                Spacer(1, 3)
            )

    else:

        story.append(
            Paragraph(
                "No additional technical observations.",
                normal_style
            )
        )

    # ====================================================
    # DISCLAIMER
    # ====================================================

    story.append(
        Spacer(1, 15)
    )

    story.append(
        Paragraph(
            "<b>IMPORTANT FORENSIC DISCLAIMER</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            "This report contains automated technical analysis "
            "and machine-learning model predictions. The results "
            "are intended to support investigative triage and "
            "should not be treated as definitive proof of "
            "authenticity, manipulation, or AI generation. "
            "Independent forensic verification is recommended "
            "before making investigative or legal conclusions.",
            small_style
        )
    )

    # ====================================================
    # BUILD PDF
    # ====================================================

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()