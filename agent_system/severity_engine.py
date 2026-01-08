def calculate_severity(confidence, bbox_area):
    if confidence >= 0.90 and bbox_area >= 0.15:
        return "CRITICAL"
    elif confidence >= 0.75:
        return "HIGH"
    elif confidence >= 0.50:
        return "MEDIUM"
    else:
        return "LOW"
