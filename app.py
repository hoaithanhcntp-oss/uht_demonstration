import streamlit as st
import pandas as pd
import numpy as np
import time

# Set page configuration
st.set_page_config(
    page_title="UHT & Injection Simulation Dashboard",
    page_icon="🧃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for industrial theme
st.markdown("""
    <style>
    .main-header {
        font-size: 28px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #1E3A8A;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧃 UHT Fruit Juice Processing Dashboard")
st.subheader("Real-time Industrial Process Simulator")

# Sidebar Configuration
st.sidebar.header("⚙️ Process Parameters")
process_type = st.sidebar.radio(
    "Select Packaging Injection Method:",
    ("Cold Aseptic Injection", "Hot Fill Injection")
)

st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Live Plant Controls")

# Dynamic inputs based on processing type
if process_type == "Cold Aseptic Injection":
    target_temp = st.sidebar.slider("UHT Heating Temp (°C)", 130, 145, 137)
    holding_time = st.sidebar.slider("Holding Time (seconds)", 2, 10, 4)
    filling_temp = st.sidebar.slider("Nozzle Filling Temp (°C)", 15, 30, 20)
    cleanroom_press = st.sidebar.slider("Cleanroom Delta Pressure (Pa)", 5, 25, 18)
    
    # Validation Logic for Cold Aseptic
    is_safe = (target_temp >= 135) and (holding_time >= 3) and (filling_temp <= 25) and (cleanroom_press >= 15)

else:
    target_temp = st.sidebar.slider("Pasteurization Temp (°C)", 85, 98, 92)
    holding_time = st.sidebar.slider("Holding Time (seconds)", 15, 45, 30)
    filling_temp = st.sidebar.slider("Nozzle Filling Temp (°C)", 75, 90, 83)
    inverter_time = st.sidebar.slider("Cap Inversion Timer (seconds)", 10, 45, 20)
    
    # Validation Logic for Hot Fill
    is_safe = (target_temp >= 90) and (filling_temp >= 80) and (inverter_time >= 15)

flow_rate = st.sidebar.slider("Product Flow Rate (L/h)", 2000, 8000, 5000)

# Main Dashboard Layout
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Sterilization Temp", value=f"{target_temp} °C", delta=f"{target_temp - 135 if process_type == 'Cold Aseptic Injection' else target_temp - 90} °C Baseline")
with col2:
    st.metric(label="Filling Temperature", value=f"{filling_temp} °C", delta="- Optimal" if (process_type == "Cold Aseptic Injection" and filling_temp <= 25) or (process_type == "Hot Fill Injection" and filling_temp >= 80) else "- CRITICAL WARNING", delta_color="normal" if ((process_type == "Cold Aseptic Injection" and filling_temp <= 25) or (process_type == "Hot Fill Injection" and filling_temp >= 80)) else "inverse")
with col3:
    if process_type == "Cold Aseptic Injection":
        st.metric(label="Isolator Pressure", value=f"{cleanroom_press} Pa", delta="Sterile" if cleanroom_press >= 15 else "Contamination Risk")
    else:
        st.metric(label="Inversion Time", value=f"{inverter_time}s", delta="Sterilized" if inverter_time >= 15 else "Insufficient")
with col4:
    st.metric(label="Production Yield", value=f"{flow_rate} L/h")

st.markdown("---")

# Critical Control Point Status Check
st.subheader("🚨 Critical Control Point (CCP) Status")
if is_safe:
    st.success("✅ SYSTEM RUNNING WITHIN SAFE PARAMETERS: Product commercial sterility achieved.")
else:
    st.error("❌ CRITICAL ALARM: Process values violate safe biological destruction thresholds! Check configurations immediately.")

# Animated chart simulation
st.subheader("📈 Live Sensor Telemetry (Last 30 Seconds)")

# Generate pseudo-live historical data
np.random.seed(42)
chart_data = pd.DataFrame(
    np.random.randn(30, 2) * 0.5 + [target_temp, filling_temp],
    columns=['Sterilization Zone Temp', 'Nozzle Fill Temp']
)

st.line_chart(chart_data)

# Informative documentation section
st.markdown("---")
st.markdown("""
### 📘 Process Architecture Details
* **UHT Continuous Stage:** Rapid high-heat thermal calculation avoids browning and vitamin breakdown while fully neutralizing spores.
* **Aseptic Boundary:** Maintains sterile physical product separation from raw materials to final containment.
""")