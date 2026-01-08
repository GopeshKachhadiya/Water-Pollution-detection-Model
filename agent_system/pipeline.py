print("------ LOADED agent_system.pipeline FROM:", __file__)

import os

from agent_system.gemini_agent import run_agent
from agent_system.severity_engine import calculate_severity
from agent_system.authority_registry import get_authorities
from agent_system.report_generator import generate_report
from agent_system.email_notifier import send_email


def process_detection(detection_payload: dict) -> dict:
    print("\n process_detection EXECUTED ")
    print("Payload keys:", detection_payload.keys())

    # Extract first detection
    detection = detection_payload["detections"][0]

    # Calculate severity
    severity = calculate_severity(
        confidence=detection["confidence"],
        bbox_area=detection.get("bbox_area", 0.2)
    )

    print(" Severity calculated:", severity)

    # Gemini reasoning agent
    print(" Calling Gemini agent")
    agent_analysis = run_agent(detection_payload)
    print(" Gemini returned analysis")

    # Generate incident report
    print(" Generating report")
    report = generate_report(
        analysis=agent_analysis,
        detection_payload=detection_payload,
        severity=severity
    )
    print(" Report generated successfully")

    # Notify authorities via email
    authorities = get_authorities("sea")
    email_logs = []

    for authority in authorities:
        print(f" Sending email to {authority['name']}")

        result = send_email(
            report=report,
            image_path=detection_payload.get("image_proof_path"),
            authority_name=authority["name"]
        )

        email_logs.append({
            "authority": authority["name"],
            "email": os.getenv("TEST_ALERT_EMAIL"),
            "status": result.get("status", "failed"),
            "error": result.get("error")
        })

        print(" Email result:", email_logs[-1])

    # FINAL RESPONSE (THIS IS WHAT UI READS)
    final_response = {
        "severity": severity,
        "analysis": agent_analysis,
        "report": report,
        "email_status": email_logs
    }

    print(" FINAL AGENT RESPONSE:", final_response)
    return final_response
