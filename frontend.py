import streamlit as st
import requests
from PIL import Image
import pandas as pd
import os
import folium
from streamlit_folium import st_folium

# PAGE CONFIG
st.set_page_config(
    page_title="Water Pollution Detection AI",
    page_icon="🌊",
    layout="centered"
)

st.title("🌊 Water Pollution Detection AI")
st.write(
    "Upload an underwater image to detect pollution and generate "
    "AI-powered environmental analysis and reports."
)

# FILE UPLOAD
uploaded_file = st.file_uploader(
    "Upload Underwater Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width="stretch")

# LOCATION (FIXED)
DEFAULT_LAT = 15.4912
DEFAULT_LON = 73.8185

st.subheader("📍 Detection Location")

m = folium.Map(
    location=[DEFAULT_LAT, DEFAULT_LON],
    zoom_start=8
)

folium.Marker(
    location=[DEFAULT_LAT, DEFAULT_LON],
    popup="Detection Location",
    tooltip="Fixed Geo Tag",
    icon=folium.Icon(color="red")
).add_to(m)

st_folium(m, height=400, width=700)

latitude = DEFAULT_LAT
longitude = DEFAULT_LON

# BUTTON ACTION
if st.button("🚀 Detect Pollution"):

    if not uploaded_file:
        st.warning("Please upload an image first.")
    else:
        with st.spinner("Running AI detection and analysis..."):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            response = requests.post(
                "http://127.0.0.1:8000/detect/",
                files=files,
                data={
                    "latitude": latitude,
                    "longitude": longitude
                }
            )

            if response.status_code != 200:
                st.error("Failed to contact backend API")
                st.stop()

            # STORE RESPONSE 
            st.session_state["api_response"] = response.json()

# RENDER RESULTS 
if "api_response" in st.session_state:

    data = st.session_state["api_response"]

    # YOLO DETECTIONS

    records = data.get("detections", [])

    st.subheader(" Pollution Detection Records")

    if not records:
        st.success("No pollution detected.")
    else:
        df = pd.DataFrame(records)
        st.dataframe(df, width="stretch")

        st.subheader(" Detection Details")

        for r in records:
            st.markdown("---")
            st.write(f"**Datetime:** {r['datetime']}")
            st.write(
                f"**Location:** ({r['lat']}, {r['lon']}) | "
                f"**Depth:** {r['depth']} m"
            )
            st.write(f"**Class:** {r['class']}")
            st.write(f"**Confidence:** {r['confidence'] * 100:.2f}%")

            if r.get("image_clip") and os.path.exists(r["image_clip"]):
                st.image(
                    r["image_clip"],
                    caption="Detected Object (Image Clip)",
                    width=250
                )

    # GEMINI AGENT OUTPUT
    agent_results = data.get("agent_results", [])

    if agent_results:
        st.subheader(" AI Agent Environmental Analysis")

        for i, agent in enumerate(agent_results, start=1):
            st.markdown(f"### Detection {i}")

            st.markdown(f"**Severity:** {agent.get('severity', 'N/A')}")

            st.markdown("#### AI Analysis")
            analysis = agent.get("analysis")
            if analysis:
                st.markdown(analysis)
            else:
                st.warning("No analysis returned")

            st.markdown("#### Full Incident Report")
            report = agent.get("report")
            if report:
                st.markdown(report)
            else:
                st.warning("No report generated")

    else:
        st.warning("No AI agent analysis returned.")

    #  EMAIL STATUS
    for agent in agent_results:
        if "email_status" in agent:
            st.subheader(" Cleanup Authority Notification")

            for mail in agent["email_status"]:
                st.success(
                    f"Email sent successfully to **{mail['authority']}** "
                    f"({mail['email']})"
                )
