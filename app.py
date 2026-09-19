import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="KOHLER AquaGuard AI",
    page_icon="💧",
    layout="wide"
)

# -------------------------------------------------
# STYLING
# -------------------------------------------------

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

div[data-testid="stMetric"] {
    background-color: #f7f9fc;
    border: 1px solid #e4e8ef;
    border-radius: 14px;
    padding: 18px;
}

div[data-testid="stMetricValue"] {
    font-size: 30px;
}

.status-card {
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #e4e8ef;
    background-color: #f7f9fc;
    text-align: center;
}

.reason-card {
    padding: 12px 15px;
    border-radius: 10px;
    background-color: #f7f9fc;
    border-left: 4px solid #4b8bbe;
    margin-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# LOAD SENSOR DATA
# -------------------------------------------------

df = pd.read_csv("data/sensor_data.csv")


# -------------------------------------------------
# AI REASONING ENGINE
# -------------------------------------------------

def analyze_restroom(row):

    leak_score = 0
    reasons = []

    if row["water_flow"] > 12:
        leak_score += 30
        reasons.append(
            "Water flow is unusually high."
        )

    if row["occupancy"] < 40:
        leak_score += 20
        reasons.append(
            "Occupancy is low compared with the observed water flow."
        )

    if row["flush_count"] < 8:
        leak_score += 15
        reasons.append(
            "Flush activity is low."
        )

    if row["leak_sensor"] == 1:
        leak_score += 25
        reasons.append(
            "The leak sensor is triggered."
        )

    sensor_warning = row["sensor_status"] != "OK"

    cleaning_needed = (
        row["time_since_cleaning"] > 100
        and row["occupancy"] > 70
    )

    if sensor_warning:
        reasons.append(
            "Sensor health requires attention."
        )

    if cleaning_needed:
        reasons.append(
            "High usage and time since cleaning indicate a hygiene need."
        )

    if leak_score >= 70:
        risk = "Critical"
        score = max(0, 100 - leak_score)
        insight = "Potential continuous water leak"

    elif sensor_warning:
        risk = "Attention"
        score = 60
        insight = "Sensor health issue"

    elif cleaning_needed:
        risk = "Attention"
        score = 72
        insight = "Cleaning recommended"

    else:
        risk = "Healthy"
        score = 95
        insight = "Normal operation"

    return risk, score, insight, reasons


results = df.apply(analyze_restroom, axis=1)

df["Risk"] = [x[0] for x in results]
df["Score"] = [x[1] for x in results]
df["AI Insight"] = [x[2] for x in results]
df["Reasons"] = [x[3] for x in results]


# -------------------------------------------------
# FACILITY CALCULATIONS
# -------------------------------------------------

total_restrooms = len(df)

active_alerts = len(
    df[df["Risk"] != "Healthy"]
)

critical_count = len(
    df[df["Risk"] == "Critical"]
)

attention_count = len(
    df[df["Risk"] == "Attention"]
)

healthy_count = len(
    df[df["Risk"] == "Healthy"]
)

facility_score = int(
    df["Score"].mean()
)

total_flow = df["water_flow"].sum()


# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("💧 KOHLER AquaGuard AI")

st.subheader(
    "Smart Facility & Water Sustainability Manager"
)

st.write(
    "AI-powered facility intelligence for water conservation, "
    "predictive hygiene and proactive maintenance."
)

st.caption(
    "Student prototype using simulated IoT telemetry."
)

st.divider()


# -------------------------------------------------
# SYSTEM STATUS
# -------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.success(
        "🟢 Monitoring System Online"
    )

with col2:
    st.info(
        "📡 24 IoT Sources Connected"
    )

with col3:
    st.info(
        "🤖 AI Analysis Active"
    )

st.divider()


# -------------------------------------------------
# KEY METRICS
# -------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Restrooms Monitored",
        total_restrooms
    )

with col2:
    st.metric(
        "Current Facility Flow",
        f"{total_flow:.1f} L/min"
    )

with col3:
    st.metric(
        "Active Alerts",
        active_alerts
    )

with col4:
    st.metric(
        "Facility Intelligence",
        f"{facility_score}/100"
    )

st.divider()


# -------------------------------------------------
# COMMAND CENTER
# -------------------------------------------------

st.header("🧠 Facility Command Center")

st.write(
    "AquaGuard evaluates multiple facility signals to identify "
    "anomalies, hygiene needs and maintenance priorities."
)

display_df = df[
    [
        "restroom",
        "Score",
        "Risk",
        "water_flow",
        "occupancy",
        "flush_count",
        "AI Insight"
    ]
].copy()

display_df.columns = [
    "Restroom",
    "Score",
    "Risk",
    "Water Flow (L/min)",
    "Occupancy (%)",
    "Flush Count",
    "AI Insight"
]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=420
)

st.divider()


# -------------------------------------------------
# RISK OVERVIEW
# -------------------------------------------------

st.header("📊 Facility Risk Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🔴 Critical",
        critical_count
    )

with col2:
    st.metric(
        "🟠 Attention",
        attention_count
    )

with col3:
    st.metric(
        "🟢 Healthy",
        healthy_count
    )

risk_chart = pd.DataFrame({
    "Status": [
        "Critical",
        "Attention",
        "Healthy"
    ],
    "Restrooms": [
        critical_count,
        attention_count,
        healthy_count
    ]
})

st.bar_chart(
    risk_chart.set_index("Status")
)

st.divider()


# -------------------------------------------------
# RESTROOM INVESTIGATOR
# -------------------------------------------------

st.header("🔎 Restroom Investigator")

selected_restroom = st.selectbox(
    "Select a restroom to investigate:",
    df["restroom"].tolist()
)

selected = df[
    df["restroom"] == selected_restroom
].iloc[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "AI Score",
        f"{selected['Score']}/100"
    )

with col2:
    st.metric(
        "Risk",
        selected["Risk"]
    )

with col3:
    st.metric(
        "Water Flow",
        f"{selected['water_flow']} L/min"
    )

with col4:
    st.metric(
        "Occupancy",
        f"{selected['occupancy']}%"
    )

st.write(
    f"**AI Insight:** {selected['AI Insight']}"
)

if selected["Reasons"]:

    st.write("### 🧠 AI Reasoning")

    for reason in selected["Reasons"]:

        st.markdown(
            f"""
            <div class="reason-card">
            ✓ {reason}
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.success(
        "No abnormal signals detected."
    )

st.divider()


# -------------------------------------------------
# AI ALERT CENTER
# -------------------------------------------------

st.header("🚨 AI Alert Center")

if critical_count > 0:

    for _, row in df[
        df["Risk"] == "Critical"
    ].iterrows():

        st.error(
            f"🔴 HIGH PRIORITY — {row['restroom']} | "
            f"{row['AI Insight']}"
        )

if attention_count > 0:

    for _, row in df[
        df["Risk"] == "Attention"
    ].iterrows():

        st.warning(
            f"🟠 ATTENTION — {row['restroom']} | "
            f"{row['AI Insight']}"
        )

if active_alerts == 0:

    st.success(
        "No active facility alerts."
    )

st.divider()


# -------------------------------------------------
# LEAK INTELLIGENCE
# -------------------------------------------------

st.header("💧 Leak Intelligence")

leak_rows = df[
    df["Risk"] == "Critical"
]

if len(leak_rows) > 0:

    leak_row = leak_rows.iloc[0]

    st.subheader(
        f"Restroom {leak_row['restroom']}"
    )

    st.write(
        "AquaGuard detected multiple independent signals "
        "that together indicate a possible continuous leak."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Water Flow",
            f"{leak_row['water_flow']} L/min"
        )

    with col2:
        st.metric(
            "Occupancy",
            f"{leak_row['occupancy']}%"
        )

    with col3:
        st.metric(
            "Flush Count",
            leak_row["flush_count"]
        )

    st.write(
        "### 🧠 Why did AquaGuard flag this?"
    )

    for reason in leak_row["Reasons"]:

        st.markdown(
            f"""
            <div class="reason-card">
            ✓ {reason}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.success(
        "High-confidence anomaly: multiple sensor signals "
        "support the leak hypothesis."
    )

    st.info(
        "Recommended action: Inspect the flush valve, "
        "supply line and nearby plumbing."
    )

else:

    st.success(
        "No high-confidence leak detected."
    )

st.divider()


# -------------------------------------------------
# WATER LOSS PROJECTION
# -------------------------------------------------

st.header("⏱️ What Happens If The Leak Is Ignored?")

if len(leak_rows) > 0:

    leak_flow = leak_rows.iloc[0]["water_flow"]

    projection_hours = 6

    projected_wastage = (
        leak_flow * 60 * projection_hours
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Potential Additional Water Loss",
            f"{projected_wastage:.0f} L"
        )

    with col2:
        st.metric(
            "Projection Window",
            "6 hours"
        )

    st.warning(
        "Scenario projection assuming the abnormal flow "
        "continues unchanged for six hours."
    )

st.divider()


# -------------------------------------------------
# PREDICTIVE HYGIENE
# -------------------------------------------------

st.header("🧹 Predictive Hygiene")

cleaning_rows = df[
    (df["time_since_cleaning"] > 100)
    & (df["occupancy"] > 70)
]

if len(cleaning_rows) > 0:

    for _, row in cleaning_rows.iterrows():

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                f"{row['restroom']} Occupancy",
                f"{row['occupancy']}%"
            )

        with col2:
            st.metric(
                "Flush Count",
                row["flush_count"]
            )

        with col3:
            st.metric(
                "Time Since Cleaning",
                f"{row['time_since_cleaning']} min"
            )

        st.warning(
            f"AI Recommendation: Schedule cleaning for "
            f"Restroom {row['restroom']} soon based on "
            "usage and time since cleaning."
        )

else:

    st.success(
        "No restroom currently requires predictive cleaning."
    )

st.divider()


# -------------------------------------------------
# SENSOR HEALTH
# -------------------------------------------------

st.header("📡 Sensor Health")

warning_sensors = df[
    df["sensor_status"] != "OK"
]

if len(warning_sensors) > 0:

    for _, row in warning_sensors.iterrows():

        st.warning(
            f"{row['restroom']} — Sensor status: "
            f"{row['sensor_status']}"
        )

else:

    st.success(
        "All monitored sensors are reporting normally."
    )

st.divider()


# -------------------------------------------------
# ASK AQUAGUARD
# -------------------------------------------------

st.header("🤖 Ask AquaGuard")

question = st.text_input(
    "Ask a question about the facility:",
    placeholder="Why is B-203 critical?"
)

if question:

    question_lower = question.lower()

    if "b-203" in question_lower:

        b203 = df[
            df["restroom"] == "B-203"
        ].iloc[0]

        st.write("### AquaGuard AI")

        st.write(
            f"B-203 is classified as critical because its "
            f"water flow is {b203['water_flow']} L/min while "
            f"occupancy is only {b203['occupancy']}% and "
            f"flush activity is low. The leak sensor is also "
            "triggered. AquaGuard combines these signals "
            "to increase confidence in the leak detection."
        )

    elif "leak" in question_lower:

        st.write("### AquaGuard AI")

        st.write(
            "AquaGuard looks for combinations of abnormal "
            "water flow, low occupancy, low flush activity "
            "and leak-sensor signals before raising a "
            "high-priority leak alert."
        )

    elif "clean" in question_lower:

        st.write("### AquaGuard AI")

        st.write(
            "AquaGuard evaluates occupancy, flush activity "
            "and time since the previous cleaning to identify "
            "restrooms that may require cleaning."
        )

    else:

        st.write("### AquaGuard AI")

        st.write(
            "AquaGuard evaluates multiple facility signals "
            "to detect anomalies, identify hygiene needs "
            "and prioritize maintenance actions."
        )

st.divider()


# -------------------------------------------------
# MAINTENANCE ACTION
# -------------------------------------------------

st.header("🔧 Maintenance Action")

if st.button(
    "Generate Maintenance Ticket"
):

    if len(leak_rows) > 0:

        leak_row = leak_rows.iloc[0]

        st.success(
            "Maintenance ticket generated!"
        )

        st.write(
            "**Ticket ID:** KA-1024"
        )

        st.write(
            f"**Location:** Restroom {leak_row['restroom']}"
        )

        st.write(
            "**Issue:** Potential continuous water leak"
        )

        st.write(
            "**Priority:** HIGH"
        )

        st.write(
            f"**Current Flow:** "
            f"{leak_row['water_flow']} L/min"
        )

        st.write(
            "**AI Confidence:** High"
        )

        st.write(
            "**Recommended Action:** Inspect flush valve "
            "and supply line"
        )

        st.write(
            "**Status:** OPEN"
        )

    else:

        st.info(
            "No high-priority maintenance issue detected."
        )


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.caption(
    "KOHLER AquaGuard AI — Student Prototype | "
    "IoT telemetry is simulated for demonstration."
)