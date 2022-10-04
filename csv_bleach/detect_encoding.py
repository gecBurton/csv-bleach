import logging
from io import BytesIO

from cchardet import UniversalDetector  # type: ignore


def detect_encoding(rows: BytesIO):
    with UniversalDetector() as detector:
        for row in rows:
            detector.feed(row)
            if detector.done:
                break

    encoding = detector.result["encoding"]
    confidence = detector.result["confidence"] * 100

    logging.info(
        f"`{encoding}` has been identified as the encoding format with {confidence}% confidence"
    )
    return encoding
