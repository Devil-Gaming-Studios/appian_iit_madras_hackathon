import streamlit as st
import pandas as pd
from simulation import simulate_process
from scenario import run_scenario

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Predictive Operations Command Center",
    layout="wide"
)

# ---------------- MATTE BLACK CSS ----------------
st.markdown("""
<style>

/* Global background */
.stApp {
    background-color: #0b0d10; /* matte black */
    color: #ffffff;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111418;
    border-right: 1px solid #1f2933;
}

/* Headings */
h1, h2, h3 {
    color: #ffffff;
    font-weight: 700;
}

/* Cards */
.card {
    background-color: #14181f;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #1f2933;
    box-shadow: 0 6px 18px rgba(0,0,0,0.6);
}

/* Metrics */
[data-testid="stMetric"] {
    background-color: #14181f;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #1f2933;
}

/* Divider */
hr {
    border: 0;
    border-top: 1px solid #1f2933;
}

/* Buttons */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-weight: 600;
    border: none;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: #9ca3af;
    font-size: 16px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff;
    border-bottom: 2px solid #2563eb;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="card">
<h1>🛰️ Predictive Operations Command Center</h1>
<p style="font-size:16px;color:#cbd5e1">
Real-time simulation • SLA risk intelligence • Decision support
</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Operational Inputs")

wip = st.sidebar.slider("📦 Work in Progress", 50, 500, 240)
arrival_rate = st.sidebar.slider("📈 Arrival Rate (cases/hr)", 10, 100, 40)
agents = st.sidebar.slider("👥 Active Agents", 1, 50, 12)
avg_service_time = st.sidebar.slider("⏱ Avg Handle Time (hrs)", 0.5, 5.0, 1.5)
sla_hours = st.sidebar.slider("⏳ SLA Deadline (hrs)", 2, 24, 8)

base_config = {
    "wip": wip,
    "arrival_rate": arrival_rate,
    "agents": agents,
    "avg_service_time": avg_service_time,
    "sla_hours": sla_hours
}

result = simulate_process(**base_config)
risk = result["breach_probability"]

# Risk coloring
if risk < 30:
    risk_color, label = "#22c55e", "LOW"
elif risk < 60:
    risk_color, label = "#facc15", "MEDIUM"
else:
    risk_color, label = "#ef4444", "HIGH"

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🧪 Simulator", "🧠 AI Optimizer"])

# ================= TAB 1 =================
with tab1:
    st.markdown("## Operational Risk Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card">
        <h3>SLA Breach Probability</h3>
        <h1 style="color:{risk_color}">{risk}%</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
        <h3>Expected Backlog (8h)</h3>
        <h1>{result['expected_backlog']}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card">
        <h3>Risk Level</h3>
        <h1 style="color:{risk_color}">{label}</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### ⏱ Backlog Forecast")
    df = pd.DataFrame({
        "Hour": range(1, 9),
        "Backlog": result["timeline"]
    })
    st.line_chart(df.set_index("Hour"))

# ================= TAB 2 =================
with tab2:
    st.markdown("## Scenario Simulator")

    col4, col5 = st.columns(2)
    with col4:
        agent_change = st.slider("🔄 Agent Reallocation", -10, 10, 3)
    with col5:
        automation_label = st.selectbox(
            "🤖 Automation Strategy",
            ["None", "Partial Automation (20%)", "High Automation (40%)"]
        )

    automation_map = {
        "None": 1.0,
        "Partial Automation (20%)": 0.8,
        "High Automation (40%)": 0.6
    }

    scenario = run_scenario(
        base_config,
        agent_change=agent_change,
        automation_factor=automation_map[automation_label]
    )

    st.markdown("### Current vs Scenario")
    compare_df = pd.DataFrame({
        "Current": result["timeline"],
        "Scenario": scenario["timeline"]
    })
    st.line_chart(compare_df)

    st.metric(
        "Scenario SLA Risk",
        f"{scenario['breach_probability']}%",
        delta=f"{risk - scenario['breach_probability']}%"
    )

# ================= TAB 3 =================
with tab3:
    st.markdown("## 🧠 AI Staffing Optimizer")

    st.write(
        "This optimizer searches for the **best achievable staffing configuration** "
        "under current demand and SLA constraints."
    )

    results = []

    for a in range(1, 51):
        test = simulate_process(
            wip=wip,
            arrival_rate=arrival_rate,
            agents=a,
            avg_service_time=avg_service_time,
            sla_hours=sla_hours
        )
        results.append((a, test["breach_probability"]))

    df_opt = pd.DataFrame(results, columns=["Agents", "SLA Risk (%)"])
    best_row = df_opt.loc[df_opt["SLA Risk (%)"].idxmin()]

    st.markdown("### 📉 SLA Risk vs Staffing Curve")
    st.line_chart(df_opt.set_index("Agents"))

    st.markdown("### 🏆 Best Achievable Configuration")

    st.success(
        f"""
        **Optimal Under Constraints**
        
        - Agents: **{int(best_row['Agents'])}**
        - Minimum SLA Risk: **{best_row['SLA Risk (%)']}%**
        
        This is the *lowest possible risk* achievable **without changing demand or automation**.
        """
    )

    if best_row["SLA Risk (%)"] > 20:
        st.warning(
            """
            ⚠️ **SLA Target Not Achievable with Staffing Alone**
            
            Even maximum staffing cannot absorb incoming demand.
            
            **AI Recommendation:**
            - Increase automation
            - Reduce arrival rate
            - Prioritize high-SLA cases
            """
        )
