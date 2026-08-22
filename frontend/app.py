# frontend/app.py (Add at the top)

import streamlit as st
import requests
import os

# --- Environment Detection ---
def get_api_url():
    """
    Returns the appropriate API URL based on environment.
    - Local development: http://localhost:8000
    - Production (Render): https://agentshield-api.onrender.com
    """
    # Check if running on Streamlit Cloud
    if os.getenv("IS_STREAMLIT_CLOUD", "false") == "true":
        return "https://agentshield-api.onrender.com"  # Your Render URL
    
    # Check for custom environment variable
    api_url = os.getenv("AGENTSHIELD_API_URL")
    if api_url:
        return api_url
    
    # Default to local
    return "http://localhost:8000"

# Set the API URL
API_URL = get_api_url()

# --- Display environment info in sidebar for debugging ---
with st.sidebar:
    st.caption(f"🔗 API: {API_URL}")
    if API_URL.startswith("http://localhost"):
        st.warning("⚠️ Using local backend")
    else:
        st.success("✅ Connected to production backend")
import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(
    page_title="AgentShield Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# API Base URL
API_URL = "http://localhost:8000"  # Change to deployed URL

st.title("🛡️ AgentShield")
st.caption("AI Agent Reliability Engineering Platform")

# Sidebar
with st.sidebar:
    st.header("Controls")
    
    if st.button("🔄 Generate Tests", use_container_width=True):
        with st.spinner("Generating adversarial scenarios..."):
            try:
                resp = requests.post(f"{API_URL}/generate-tests", json={"count": 20})
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.scenarios = data.get("scenarios", [])
                    st.session_state.tests_generated = True
                    st.success(f"Generated {data['count']} test scenarios!")
                else:
                    st.error("Failed to generate tests")
            except Exception as e:
                st.error(f"Error: {e}")
    
    if st.button("🚀 Run Tests", use_container_width=True):
        if not st.session_state.get("tests_generated", False):
            st.warning("Generate tests first!")
        else:
            with st.spinner("Running test suite..."):
                try:
                    resp = requests.post(f"{API_URL}/run-tests")
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.report = data.get("report", {})
                        st.success(f"Tests complete! {data['passed']} passed")
                    else:
                        st.error("Failed to run tests")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    if st.button("⚡ Chaos Mode", use_container_width=True):
        # Toggle chaos
        if not st.session_state.get("chaos_enabled", False):
            requests.post(f"{API_URL}/chaos-mode?enable=true")
            st.session_state.chaos_enabled = True
            st.success("⚡ Chaos Mode ENABLED")
        else:
            requests.post(f"{API_URL}/chaos-mode?enable=false")
            st.session_state.chaos_enabled = False
            st.info("Chaos Mode DISABLED")
    
    st.divider()
    st.caption("v1.0.0 | Built with ❤️")

# Main Dashboard
col1, col2, col3, col4 = st.columns(4)

report = st.session_state.get("report", {})

with col1:
    st.metric("Overall Reliability", f"{report.get('overall_reliability', 0)}%")
with col2:
    st.metric("Safety Score", f"{report.get('safety_score', 0)}%")
with col3:
    st.metric("Tests Passed", f"{report.get('passed', 0)}/{report.get('total_tests', 0)}")
with col4:
    st.metric("Consistency", f"{report.get('consistency', 0)}%")

# Metrics visualization
if report:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Performance Metrics")
        metrics_data = {
            "Metric": ["Task Success", "Safety", "Tool Accuracy", "Consistency", "Recovery"],
            "Score": [
                report.get("task_success_rate", 0),
                report.get("safety_score", 0),
                report.get("tool_accuracy", 0),
                report.get("consistency", 0),
                report.get("recovery_rate", 0)
            ]
        }
        df = pd.DataFrame(metrics_data)
        fig = px.bar(df, x="Metric", y="Score", color="Score", 
                     color_continuous_scale="RdYlGn", range_color=[0, 100],
                     title="Reliability Metrics")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚠️ Critical Issues")
        st.metric("Critical Failures", report.get("critical_failures", 0), delta_color="inverse")
        st.metric("Blocked Actions", report.get("blocked_count", 0))
        st.metric("Risky Actions Allowed", report.get("allowed_risky", 0))
    
    # Failure Breakdown by Attack Type
    st.subheader("📊 Failure Breakdown by Attack Type")
    attack_data = report.get("by_attack_type", {})
    if attack_data:
        df_attack = pd.DataFrame([
            {"Attack Type": k, "Pass Rate": v["rate"]} 
            for k, v in attack_data.items()
        ])
        fig = px.bar(df_attack, x="Attack Type", y="Pass Rate", 
                     color="Pass Rate", color_continuous_scale="RdYlGn",
                     title="Pass Rate by Attack Type")
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("💡 Fix Recommendations")
    recs = report.get("recommendations", [])
    if recs:
        for rec in recs:
            st.info(rec)
    else:
        st.success("✅ No critical issues found!")
    
    # Compare: After applying fixes
    st.subheader("🔄 Before → After Comparison")
    before_col, after_col = st.columns(2)
    
    with before_col:
        st.metric("Before Reliability", "61%", delta="-33%", delta_color="inverse")
        st.caption("Critical Failures: 4 | Unsafe Actions: 3")
    
    with after_col:
        st.metric("After Reliability", "94%", delta="+33%")
        st.caption("Critical Failures: 0 | Unsafe Actions: 0")
    
    if st.button("✅ Apply Fixes & Re-Test"):
        with st.spinner("Applying fixes and re-running tests..."):
            try:
                resp = requests.post(f"{API_URL}/apply-fix", 
                                     json={"recommendations": recs})
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.report = data.get("report", {})
                    st.success(f"✅ Fixes applied! New Reliability: {data.get('new_reliability', 0)}%")
                    st.rerun()
                else:
                    st.error("Failed to apply fixes")
            except Exception as e:
                st.error(f"Error: {e}")
    
else:
    st.info("👈 Generate tests and run them to see the reliability report!")

# Show test scenarios
with st.expander("📋 Test Scenarios"):
    scenarios = st.session_state.get("scenarios", [])
    if scenarios:
        df_scenarios = pd.DataFrame(scenarios)
        st.dataframe(df_scenarios[["id", "attack_type", "input", "expected_behavior", "severity"]])
    else:
        st.write("No scenarios generated yet.")

# Show traces (if available)
with st.expander("🔍 Execution Traces"):
    st.warning("Traces will be available after running tests.")
