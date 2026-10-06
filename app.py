import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

from streamlit_autorefresh import st_autorefresh
from user_agents import parse

# -------------------------------
# Page settings
# -------------------------------

st.set_page_config(
    page_title="HoneyTrapX Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ HoneyTrapX Dashboard")

st_autorefresh(
    interval=5000,
    key="dashboard_refresh"
)

# -------------------------------
# Database connection
# -------------------------------

conn = sqlite3.connect(
    "database/attacks.db"
)

df = pd.read_sql_query(

    """
    SELECT *
    FROM attacks
    ORDER BY id DESC
    """,

    conn
)

conn.close()

# -------------------------------
# Parse User-Agent
# -------------------------------

browsers = []
operating_systems = []
devices = []

for agent_string in df["user_agent"]:

    user_agent = parse(
        str(agent_string)
    )

    browsers.append(
        user_agent.browser.family
    )

    operating_systems.append(
        user_agent.os.family
    )

    if user_agent.is_mobile:

        devices.append(
            "Mobile"
        )

    elif user_agent.is_tablet:

        devices.append(
            "Tablet"
        )

    else:

        devices.append(
            "Desktop"
        )

df["browser"] = browsers

df["os"] = operating_systems

df["device"] = devices

# -------------------------------
# Statistics
# -------------------------------

st.subheader("📊 Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Attacks",
        len(df)
    )

with col2:

    st.metric(
        "Unique IPs",
        df["ip_address"].nunique()
    )

with col3:

    st.metric(
        "Attack Types",
        df["attack_type"].nunique()
    )

with col4:

    st.metric(
        "High Severity",
        len(
            df[
                df["severity"] == "High"
            ]
        )
    )

# -------------------------------
# Top attacker IPs
# -------------------------------

st.subheader(
    "🌐 Top Attacker IPs"
)

ip_counts = (

    df["ip_address"]

    .value_counts()

    .reset_index()
)

ip_counts.columns = [

    "IP Address",

    "Attempts"
]

fig_ip = px.bar(

    ip_counts,

    x="IP Address",

    y="Attempts",

    title="Attack Count by IP"
)

st.plotly_chart(

    fig_ip,

    use_container_width=True
)

# -------------------------------
# Browser statistics
# -------------------------------

st.subheader(
    "🌍 Browser Usage"
)

browser_counts = (

    df["browser"]

    .value_counts()

    .reset_index()
)

browser_counts.columns = [

    "Browser",

    "Count"
]

fig_browser = px.pie(

    browser_counts,

    names="Browser",

    values="Count",

    title="Browsers"
)

st.plotly_chart(

    fig_browser,

    use_container_width=True
)

# -------------------------------
# OS statistics
# -------------------------------

st.subheader(
    "💻 Operating Systems"
)

os_counts = (

    df["os"]

    .value_counts()

    .reset_index()
)

os_counts.columns = [

    "OS",

    "Count"
]

fig_os = px.pie(

    os_counts,

    names="OS",

    values="Count",

    title="Operating Systems"
)

st.plotly_chart(

    fig_os,

    use_container_width=True
)

# -------------------------------
# Device statistics
# -------------------------------

st.subheader(
    "📱 Device Types"
)

device_counts = (

    df["device"]

    .value_counts()

    .reset_index()
)

device_counts.columns = [

    "Device",

    "Count"
]

fig_device = px.pie(

    device_counts,

    names="Device",

    values="Count",

    title="Devices"
)

st.plotly_chart(

    fig_device,

    use_container_width=True
)

# -------------------------------
# Attack types
# -------------------------------

st.subheader(
    "⚠️ Attack Types"
)

attack_counts = (

    df["attack_type"]

    .value_counts()

    .reset_index()
)

attack_counts.columns = [

    "Attack",

    "Count"
]

fig_attack = px.bar(

    attack_counts,

    x="Attack",

    y="Count",

    title="Attack Distribution"
)

st.plotly_chart(

    fig_attack,

    use_container_width=True
)

# -------------------------------
# Attack table
# -------------------------------

st.subheader(
    "📜 Attack Logs"
)

st.dataframe(

    df,

    use_container_width=True
)

# -------------------------------
# PDF button
# -------------------------------

st.subheader(
    "📄 Reports"
)

if st.button(
    "Generate PDF Report"
):

    os.system(
        "python generate_report.py"
    )

    st.success(
        "PDF report generated successfully!"
    )
