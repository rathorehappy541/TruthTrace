import streamlit as st
from PIL import Image
from io import BytesIO

from analyzer.metadata import extract_metadata
from analyzer.hashing import calculate_sha256, calculate_phash
from analyzer.ocr import extract_text
from analyzer.manipulation import create_ela_image
from analyzer.risk import calculate_risk_score
from analyzer.ai_detection import detect_ai_image
from analyzer.evidence import create_evidence_record
from analyzer.report import generate_pdf_report
from analyzer.timeline import create_timeline


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TruthTrace",
    page_icon="🔎",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
.stApp { background: radial-gradient(circle at 10% 0%, #e8f4ff 0, transparent 30%), radial-gradient(circle at 95% 10%, #e9fff7 0, transparent 24%), #f7f9fc; color: #172033; font-family: 'Manrope', sans-serif; }
.block-container { max-width: 1240px; padding-top: 2.5rem; padding-bottom: 3rem; }
h1, h2, h3 { font-family: 'Manrope', sans-serif !important; letter-spacing: -0.04em; color: #10233f; }
h1 { font-weight: 800 !important; font-size: 2.7rem !important; margin-bottom: .1rem !important; }
h2 { font-weight: 800 !important; border-bottom: 1px solid #dbe4f0; padding-bottom: .55rem; margin-top: 2.25rem !important; }
h3 { font-weight: 700 !important; }
p, .stMarkdown, .stCaption { font-size: 1rem; line-height: 1.65; }
.stCaption { color: #53627a !important; }
[data-testid="stMetric"] { background: rgba(255,255,255,.82); border: 1px solid #dbe4f0; border-radius: 14px; padding: 1rem 1.1rem; box-shadow: 0 8px 24px rgba(20,45,80,.06); }
[data-testid="stMetricLabel"] { color: #53627a; font-size: .78rem; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; }
[data-testid="stMetricValue"] { color: #102e57; font-size: 1.35rem; font-weight: 800; }
.stButton > button, .stDownloadButton > button { background: linear-gradient(120deg, #1167b1, #0a8f73); color: white; border: 0; border-radius: 9px; font-family: 'Manrope', sans-serif; font-weight: 700; padding: .55rem 1rem; }
.stFileUploader { background: rgba(255,255,255,.78); border: 1px dashed #6d91ba; border-radius: 14px; padding: .6rem; }
.stFileUploader button { background: #08090c !important; color: #ff4d4f !important; border: 1px solid #ff4d4f !important; border-radius: 8px !important; font-weight: 800 !important; }
.stFileUploader button:hover { background: #1c1f25 !important; color: #ff6b6d !important; border-color: #ff6b6d !important; }
.stCode, code { font-family: 'DM Mono', monospace !important; font-size: .82rem !important; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.title("🔎 TruthTrace")

st.subheader(
    "AI Media Detection & Source Tracing"
)

st.caption(
    "Evidence-first media forensics for clear, confident investigative triage"
)

st.markdown("---")


# ============================================================
# EVIDENCE UPLOAD
# ============================================================

st.header("📁 Evidence Upload")

st.write(
    "Upload an image to begin a transparent forensic assessment."
)

uploaded_file = st.file_uploader(
    "Choose an image",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp",
        "bmp"
    ]
)


# ============================================================
# MAIN APPLICATION
# ============================================================

if uploaded_file is not None:

    st.success(
        "Evidence uploaded successfully!"
    )

    # ========================================================
    # READ IMAGE
    # ========================================================

    image_bytes = uploaded_file.getvalue()

    try:
        image = Image.open(BytesIO(image_bytes))
        image.load()
    except Exception:
        st.error("This file could not be read as a valid image. Please upload a supported image file.")
        st.stop()

    # ========================================================
    # UPLOADED EVIDENCE
    # ========================================================

    st.subheader("🖼️ Uploaded Evidence")

    preview_col, _ = st.columns([1, 2])
    with preview_col:
        st.image(
            image,
            caption=uploaded_file.name,
            use_container_width=True
        )

    # ========================================================
    # FORENSIC ANALYSIS
    # ========================================================

    st.markdown("---")

    st.header("🔬 Forensic Analysis")

    # ========================================================
    # FILE INFORMATION
    # ========================================================

    st.subheader("📋 File Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Format",
            image.format or "Unknown"
        )

    with col2:

        st.metric(
            "Dimensions",
            f"{image.width} × {image.height}"
        )

    with col3:

        st.metric(
            "Color Mode",
            image.mode
        )

    # ========================================================
    # METADATA / EXIF
    # ========================================================

    st.subheader("🧾 Metadata / EXIF")

    try:

        metadata = extract_metadata(image_bytes, uploaded_file.name)

    except Exception:

        metadata = {
            "Filename": uploaded_file.name
        }

    if metadata:

        for key, value in metadata.items():

            if isinstance(value, bytes):

                value = "<binary data>"

            st.write(
                f"**{key}:** {value}"
            )

    else:

        st.info(
            "No EXIF metadata found."
        )

    # ========================================================
    # DIGITAL HASHES
    # ========================================================

    sha256_hash = calculate_sha256(
        image_bytes
    )

    phash = calculate_phash(
        image_bytes
    )

    # ========================================================
    # EVIDENCE RECORD
    # ========================================================

    try:

        evidence_record = create_evidence_record(
            uploaded_file.name,
            len(image_bytes),
            sha256_hash,
            phash
        )

    except Exception:

        evidence_record = {
            "Evidence ID": "TT-UNKNOWN",
            "Filename": uploaded_file.name,
            "File Size": len(image_bytes),
            "SHA-256": sha256_hash,
            "pHash": phash,
            "Analysis Time": "N/A",
            "Status": "Analyzed"
        }

    # ========================================================
    # EVIDENCE ID
    # ========================================================

    st.subheader("🆔 Evidence Record")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Evidence ID",
            evidence_record.get(
                "Evidence ID",
                "N/A"
            )
        )

    with col2:

        st.metric(
            "Status",
            evidence_record.get(
                "Status",
                "Analyzed"
            )
        )

    st.write(
        f"**Analysis Time:** "
        f"{evidence_record.get('Analysis Time', 'N/A')}"
    )

    st.write(
        f"**Original Filename:** "
        f"{evidence_record.get('Filename', uploaded_file.name)}"
    )

    st.write(
        f"**File Size:** "
        f"{evidence_record.get('File Size', len(image_bytes)):,} bytes"
    )

    # ========================================================
    # DIGITAL EVIDENCE FINGERPRINT
    # ========================================================

    st.subheader(
        "🔐 Digital Evidence Fingerprint"
    )

    st.write("**SHA-256:**")

    st.code(
        sha256_hash
    )

    st.write(
        "**Perceptual Hash (pHash):**"
    )

    st.code(
        phash
    )

    # ========================================================
    # OCR
    # ========================================================

    st.subheader(
        "📝 Text Detection / OCR"
    )

    try:

        ocr_results = extract_text(
            image
        )

    except Exception as e:

        ocr_results = []

        st.warning(
            f"OCR could not be completed: {e}"
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

            st.write(
                f"**{text}**"
            )

            st.caption(
                f"Confidence: "
                f"{confidence * 100:.1f}%"
            )

    else:

        st.info(
            "No readable text detected."
        )

    # ========================================================
    # IMAGE MANIPULATION / ELA
    # ========================================================

    st.subheader(
        "🧪 Image Manipulation Analysis"
    )

    try:

        ela_image = create_ela_image(
            image
        )

        if ela_image is not None:

            original_col, ela_col = st.columns(2)

            with original_col:
                st.image(
                    image,
                    caption="Original evidence",
                    use_container_width=True
                )

            with ela_col:
                st.image(
                    ela_image,
                    caption="Error Level Analysis (ELA)",
                    use_container_width=True
                )

            st.caption(
                "ELA highlights differences in image "
                "compression patterns. It is an investigative "
                "indicator and not definitive proof of editing."
            )

    except Exception as e:

        st.warning(
            f"ELA analysis could not be completed: {e}"
        )

    # ========================================================
    # AI MEDIA DETECTION
    # ========================================================

    st.subheader(
        "🤖 AI Media Analysis"
    )

    st.caption(
        "Automated model-based assessment of the uploaded image."
    )

    try:

        with st.spinner(
            "Analyzing image with AI detection model..."
        ):

            ai_results = detect_ai_image(
                image
            )

    except Exception as e:

        ai_results = []

        st.error(
            f"AI detection could not be completed: {e}"
        )

    # ========================================================
    # AI RESULTS
    # ========================================================

    dashboard_label = "UNAVAILABLE"
    dashboard_confidence = 0

    if ai_results:

        ai_results = sorted(
            ai_results,
            key=lambda x: x.get(
                "score",
                0
            ),
            reverse=True
        )

        top_result = ai_results[0]

        top_label = top_result.get(
            "label",
            "unknown"
        )

        top_confidence = top_result.get(
            "score",
            0
        )

        if top_label.lower() == "artificial":

            prediction = "AI-GENERATED LIKELY"
            dashboard_label = "AI-LIKELY"

        elif top_label.lower() == "human":

            prediction = "HUMAN-LIKELY"
            dashboard_label = "HUMAN-LIKELY"

        else:

            prediction = top_label.upper()
            dashboard_label = prediction

        dashboard_confidence = top_confidence

        st.markdown(
            "### Model Prediction"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Prediction",
                prediction
            )

        with col2:

            st.metric(
                "Model Confidence",
                f"{top_confidence * 100:.1f}%"
            )

        st.markdown(
            "### Confidence Breakdown"
        )

        for result in ai_results:

            label = result.get(
                "label",
                "unknown"
            )

            confidence = result.get(
                "score",
                0
            )

            if label.lower() == "artificial":

                display_label = "AI-generated"

            elif label.lower() == "human":

                display_label = "Human"

            else:

                display_label = label.capitalize()

            st.write(
                f"**{display_label}: "
                f"{confidence * 100:.1f}%**"
            )

            st.progress(
                min(
                    max(
                        float(confidence),
                        0.0
                    ),
                    1.0
                )
            )

        st.markdown(
            "### ⚠️ Interpretation"
        )

        if top_confidence >= 0.90:

            interpretation = (
                f"The model strongly favors the "
                f"**{prediction.lower()}** classification."
            )

        elif top_confidence >= 0.70:

            interpretation = (
                f"The model moderately favors the "
                f"**{prediction.lower()}** classification."
            )

        else:

            interpretation = (
                "The model result has relatively low "
                "confidence and should be treated cautiously."
            )

        st.info(
            interpretation
        )

        st.caption(
            "This is an automated model prediction, "
            "not definitive proof of whether an image "
            "is authentic, manipulated, or AI-generated."
        )

    else:

        st.warning(
            "The AI detection model returned no usable result."
        )

    # ========================================================
    # FINAL FORENSIC RISK ASSESSMENT
    # ========================================================

    st.markdown("---")

    st.subheader(
        "🚨 Final Forensic Assessment"
    )

    try:

        risk_score, risk_level, findings = (
            calculate_risk_score(
                metadata,
                ocr_results,
                image_bytes,
                ai_results
            )
        )

    except Exception as e:

        risk_score = 0
        risk_level = "Unavailable"

        findings = [
            f"Risk assessment could not be completed: {e}"
        ]

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Investigative Risk Score",
            f"{risk_score}/100"
        )

    with col2:

        st.metric(
            "Risk Level",
            risk_level
        )

    if findings:

        st.write(
            "**Technical Observations:**"
        )

        for finding in findings:

            st.write(
                f"• {finding}"
            )

    else:

        st.info(
            "No additional technical observations."
        )

    st.caption(
        "The Investigative Risk Score combines automated "
        "technical indicators for triage. It does not establish "
        "whether an image is authentic, manipulated, or "
        "AI-generated."
    )

    # ========================================================
    # INVESTIGATION CASE SUMMARY
    # ========================================================

    st.markdown("---")

    st.header(
        "🕵️ Investigation Case Summary"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🆔 Evidence ID",
            evidence_record.get(
                "Evidence ID",
                "N/A"
            )
        )

    with col2:

        st.metric(
            "🚨 Risk Score",
            f"{risk_score}/100"
        )

    with col3:

        st.metric(
            "🤖 AI Assessment",
            dashboard_label
        )

    with col4:

        st.metric(
            "📋 Case Status",
            "COMPLETE"
        )

    st.write(
        "### Investigation Overview"
    )

    overview_col1, overview_col2 = st.columns(2)

    with overview_col1:

        st.write(
            f"**Evidence:** "
            f"{evidence_record.get('Filename', uploaded_file.name)}"
        )

        st.write(
            f"**Evidence ID:** "
            f"{evidence_record.get('Evidence ID', 'N/A')}"
        )

        st.write(
            f"**Risk Level:** "
            f"{risk_level}"
        )

    with overview_col2:

        st.write(
            f"**AI Confidence:** "
            f"{dashboard_confidence * 100:.1f}%"
        )

        st.write(
            f"**OCR Findings:** "
            f"{len(ocr_results)}"
        )

        st.write(
            f"**Technical Findings:** "
            f"{len(findings)}"
        )

    # ========================================================
    # EVIDENCE ANALYSIS TIMELINE
    # ========================================================

    st.markdown("---")

    st.subheader(
        "🔐 Evidence Analysis Timeline"
    )

    try:

        timeline = create_timeline()

        for item in timeline:

            col1, col2, col3 = st.columns(
                [1, 5, 1]
            )

            with col1:

                st.write(
                    f"**{item.get('time', '')}**"
                )

            with col2:

                st.write(
                    item.get(
                        "event",
                        "Unknown event"
                    )
                )

            with col3:

                st.success(
                    item.get(
                        "status",
                        "Completed"
                    )
                )

    except Exception as e:

        st.warning(
            f"Timeline could not be generated: {e}"
        )

    st.caption(
        "This timeline records the automated analysis "
        "workflow performed by TruthTrace. It is an "
        "application audit trail and not a legally "
        "certified chain of custody."
    )

    # ========================================================
    # FORENSIC PDF REPORT
    # ========================================================

    st.markdown("---")

    st.subheader(
        "📄 Forensic Investigation Report"
    )

    try:

        pdf_report = generate_pdf_report(
            evidence_record,
            metadata,
            ocr_results,
            ai_results,
            risk_score,
            risk_level,
            findings
        )

        st.download_button(
            label="📥 Download Forensic PDF Report",
            data=pdf_report,
            file_name=(
                f"{evidence_record.get('Evidence ID', 'TruthTrace')}_"
                f"Forensic_Report.pdf"
            ),
            mime="application/pdf"
        )

    except Exception as e:

        st.error(
            f"PDF report generation failed: {e}"
        )


# ============================================================
# NO FILE UPLOADED
# ============================================================

else:

    st.info(
        "Please upload an image above to begin forensic analysis."
    )

    st.markdown(
        """
        ### What TruthTrace analyzes

        🔐 **Digital Fingerprint**  
        SHA-256 and perceptual hashing

        🧾 **Metadata**  
        EXIF and file information

        📝 **OCR**  
        Text detection and confidence

        🧪 **Manipulation Analysis**  
        Error Level Analysis

        🤖 **AI Detection**  
        Machine-learning based assessment

        🚨 **Risk Assessment**  
        Automated investigative indicators

        📄 **Forensic Report**  
        Downloadable PDF evidence report
        """
    )
