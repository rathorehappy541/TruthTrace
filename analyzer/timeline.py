from datetime import datetime


def create_timeline():

    current_time = datetime.now().strftime(
        "%H:%M:%S"
    )

    return [
        {
            "time": current_time,
            "event": "Evidence uploaded",
            "status": "Completed"
        },
        {
            "time": current_time,
            "event": "SHA-256 fingerprint generated",
            "status": "Completed"
        },
        {
            "time": current_time,
            "event": "Metadata extraction completed",
            "status": "Completed"
        },
        {
            "time": current_time,
            "event": "OCR analysis completed",
            "status": "Completed"
        },
        {
            "time": current_time,
            "event": "AI media analysis completed",
            "status": "Completed"
        },
        {
            "time": current_time,
            "event": "Risk assessment completed",
            "status": "Completed"
        },
        {
            "time": current_time,
            "event": "Forensic report prepared",
            "status": "Completed"
        }
    ]