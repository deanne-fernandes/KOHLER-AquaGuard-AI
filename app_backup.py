import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="KOHLER AquaGuard AI",
    page_icon="💧",
    layout="wide"
)

# -----------------------------
# DATA
# -----------------------------

data = {
    "Restroom": ["A-101", "B-203", "C-201", "A-104"],
    "Water Flow (L/min)": [4.8, 18.8, 7.1, 0.0],
    "Flush Count": [12, 4, 22, 0],
    "Occupancy": [48, 20, 81, 18],
    "Leak Sensor": ["Normal", "Detected", "Normal", "Normal"],
    "Sensor Status": ["Healthy", "Healthy", "Healthy", "Warning"],
    "Minutes Since Cleaning": [35, 42, 118, 60]
}

df = pd.DataFrame(data)

# -----------------------------
# AI ANALYSIS
# -----------------------------

def analyze_restroom(row):

    if row["Water Flow (L/min)"] > 15 and row["Occupancy"] < 40:
        return "Critical", 31, "Potential continuous leak"

    if row["Sensor Status"] == "Warning":
        return "Attention", 48, "Sensor health issue"

    if row["Minutes Since Cleaning"] > 100 and row["Occupancy"] > 70:
        return "Attention", 67, "Cleaning recommended"

    return "Healthy", 92, "Normal operation"


analysis = df.apply(analyze_restroom, axis=1)

df["Risk"] = [x[0] for x in analysis]
df["Score"] = [x[1] for x in analysis]
df["AI Insight"] = [x[2] for x in analysis]

# -----------------------------
# HEADER
# -----------------------------

st.title("💧 KOHLER AquaGuard AI")
st.subheader("Smart Facility & Water Sustainability Manager")

st.write(
    "AI-powered facility intelligence for water conservation, "
    "hygiene prediction and proactive maintenance."
)

st.divider()

# -----------------------------
# TOP METRICS
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Restrooms Monitored",
    "24"
)

col2.metric(
    "Water Usage Today",
    "12,840 L"
)

col3.metric(
    "Water Saved",
    "2,340 L",
    "15.4%"
)

col4.metric(
    "Active Alerts",
    "3"
)

st.divider()

# -----------------------------
# FACILITY INTELLIGENCE
# -----------------------------

st.header("🧠 Facility Intelligence")

col1, col2 = st.columns([2, 1])

with col1:

    st.write("### Restroom Risk Overview")

    display_df = df[
        [
            "Restroom",
            "Score",
            "Risk",
            "Water Flow (L/min)",
            "Occupancy",
            "AI Insight"
        ]
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

with col2:

    average_score = int(df["Score"].mean())

    st.metric(
        "Overall Intelligence Score",
        f"{average_score}/100"
    )

    if average_score >= 80:
        st.success("Facility operating efficiently")
    elif average_score >= 60:
        st.warning("Facility needs attention")
    else:
        st.error("Critical facility conditions")

st.divider()

# -----------------------------
# ALERTS
# -----------------------------

st.header("🚨 AI-Detected Alerts")

st.error(
    "HIGH PRIORITY — Continuous water flow detected in Restroom B-203"
)

st.warning(
    "MEDIUM PRIORITY — Cleaning recommended for Restroom C-201"
)

st.warning(
    "MEDIUM PRIORITY — Sensor health issue detected in Restroom A-104"
)

st.divider()

# -----------------------------
# LEAK ANALYSIS
# -----------------------------

st.header("💧 Leak Intelligence")

st.write("### Restroom B-203")

flow = 18.8
duration = 27

wastage = flow * duration

st.write(
    "The system detected unusually high water flow while occupancy "
    "and flush activity remained low."
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Current Flow",
    "18.8 L/min"
)

col2.metric(
    "Continuous Duration",
    "27 min"
)

col3.metric(
    "Estimated Wastage",
    f"{wastage:.0f} L"
)

st.success(
    "AI Confidence: 94% — High probability of a continuous leak."
)

st.info(
    "Recommended action: Inspect the flush valve, supply line "
    "and plumbing system."
)

st.divider()

# -----------------------------
# COST OF IGNORING
# -----------------------------

st.header("⏱️ What Happens If The Leak Is Ignored?")

future_hours = 6
future_wastage = flow * 60 * future_hours

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Projected Additional Wastage",
        f"{future_wastage:.0f} L"
    )

with col2:

    st.metric(
        "Projected Flow Duration",
        "6 hours"
    )

st.warning(
    "AquaGuard recommends immediate maintenance intervention "
    "to prevent continued water loss."
)

st.divider()

# -----------------------------
# HYGIENE PREDICTION
# -----------------------------

st.header("🧹 Predictive Hygiene")

st.write("### Restroom C-201")

st.write(
    "High occupancy and increased flush activity indicate that "
    "the restroom is approaching its recommended cleaning threshold."
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Occupancy",
    "81%"
)

col2.metric(
    "Flush Count",
    "22"
)

col3.metric(
    "Time Since Cleaning",
    "118 min"
)

st.warning(
    "AI Recommendation: Schedule cleaning within the next 18 minutes."
)

st.divider()

# -----------------------------
# ASK AQUAGUARD
# -----------------------------

st.header("🤖 Ask AquaGuard")

question = st.text_input(
    "Ask a question about the facility:",
    placeholder="Why is B-203 critical?"
)

if question:

    question_lower = question.lower()

    if "b-203" in question_lower or "leak" in question_lower:

        st.write("### AquaGuard AI")

        st.write(
            "B-203 is classified as critical because water flow is "
            "18.8 L/min while occupancy is only 20% and flush activity "
            "is low. The continuous flow pattern strongly suggests "
            "a possible leak."
        )

    elif "c-201" in question_lower or "clean" in question_lower:

        st.write("### AquaGuard AI")

        st.write(
            "C-201 has high occupancy and 22 flushes with 118 minutes "
            "since the last cleaning. The system therefore recommends "
            "cleaning within approximately 18 minutes."
        )

    else:

        st.write("### AquaGuard AI")

        st.write(
            "Based on the available facility data, AquaGuard recommends "
            "prioritizing B-203 because of its high water-loss risk."
        )

st.divider()

# -----------------------------
# MAINTENANCE TICKET
# -----------------------------

st.header("🔧 Maintenance Action")

if st.button("Generate Maintenance Ticket"):

    st.success("Maintenance ticket generated!")

    st.write("**Ticket ID:** KA-1024")
    st.write("**Location:** Restroom B-203")
    st.write("**Issue:** Potential continuous water leak")
    st.write("**Priority:** HIGH")
    st.write("**Estimated Water Wastage:** 507 L")
    st.write("**AI Confidence:** 94%")
    st.write("**Recommended Action:** Inspect flush valve and supply line")
    st.write("**Status:** OPEN")

st.divider()

st.caption(
    "KOHLER AquaGuard AI — Student Prototype | "
    "IoT telemetry shown is simulated for demonstration."
)
