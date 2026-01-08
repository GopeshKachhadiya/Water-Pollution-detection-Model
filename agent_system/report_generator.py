def generate_report(analysis: str, detection_payload: dict, severity: str) -> str:
    """
    Generates a structured environmental incident report
    based on Gemini analysis and detection metadata.
    """

    location = detection_payload.get("location", {})
    detections = detection_payload.get("detections", [])

    report = f"""
## Water Pollution Incident Report

###  Location
- Latitude: {location.get('latitude')}
- Longitude: {location.get('longitude')}
- Depth: {location.get('depth_m')} m

### Severity
**{severity}**

### Detection Summary
- Detected object: {detections[0].get('class')}
- Confidence: {detections[0].get('confidence'):.2f}

---

###  AI Environmental Analysis
{analysis}

---

### Recommended Actions
- Immediate cleanup if accessible
- Notify local marine or municipal authorities
- Monitor area for recurring debris
- Investigate waste source if repeated detections occur
"""

    return report.strip()
