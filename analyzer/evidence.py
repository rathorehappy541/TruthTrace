from datetime import datetime
import uuid


def create_evidence_record(
    filename,
    file_size,
    sha256_hash,
    phash
):
    """
    Create a digital evidence record.
    """

    evidence_id = (
        "TT-"
        + datetime.now().strftime("%Y%m%d")
        + "-"
        + uuid.uuid4().hex[:8].upper()
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return {
        "Evidence ID": evidence_id,
        "Filename": filename,
        "File Size": file_size,
        "SHA-256": sha256_hash,
        "pHash": phash,
        "Analysis Time": timestamp,
        "Status": "Analysis Completed"
    }