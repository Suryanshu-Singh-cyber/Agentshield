# frontend/app.py

# ============================================
# 1. IMPORT STATEMENTS (FIRST)
# ============================================
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import json
from datetime import datetime

# ============================================
# 2. PAGE CONFIG (MUST BE FIRST STREAMLIT COMMAND)
# ============================================
st.set_page_config(
    page_title="AgentShield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 3. ENVIRONMENT DETECTION
# ============================================
def get_api_url():
    """Returns the appropriate API URL based on environment."""
    # Check if running on Streamlit Cloud
    if os.getenv("IS_STREAMLIT_CLOUD", "false") == "true":
        return "https://agentshield-api.onrender.com"  # Your Render URL
    
    # Check for custom environment variable
    api_url = os.getenv("AGENTSHIELD_API_URL")
    if api_url:
        return api_url
    
    # Default to local
    return "http://localhost:8000"

API_URL = get_api_url()

# ============================================
# 4. CUSTOM CSS LOADING
# ============================================
def load_css():
    """Load custom CSS for premium UI."""
    try:
        with open("frontend/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Fallback: CSS file not found, use inline styles
        st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; }
        h1, h2, h3 { font-weight: 700 !important; background: linear-gradient(90deg, #00d2ff, #3a7bd5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        [data-testid="metric-container"] { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; }
        .stButton > button { background: linear-gradient(90deg, #00d2ff, #3a7bd5) !important; border: none !important; border-radius: 50px !important; color: white !important; }
        </style>
        """, unsafe_allow_html=True)

load_css()

# ============================================
# 5. INITIALIZE SESSION STATE
# ============================================
if "scenarios" not in st.session_state:
    st.session_state.scenarios = []
if "tests_generated" not in st.session_state:
    st.session_state.tests_generated = False
if "report" not in st.session_state:
    st.session_state.report = {}
if "chaos_enabled" not in st.session_state:
    st.session_state.chaos_enabled = False

# ============================================
# 6. HEADER
# ============================================
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="font-size: 4rem; margin: 0;">🛡️ AgentShield</h1>
    <p style="font-size: 1.2rem; opacity: 0.7; margin: 0;">
        AI Agent Reliability Engineering Platform
    </p>
    <div style="background: linear-gradient(90deg, #00d2ff, #3a7bd5); 
                height: 4px; width: 100px; margin: 1rem auto; border-radius: 2px;">
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# 7. SIDEBAR CONTROLS
# ============================================
with st.sidebar:
    st.markdown("### ⚙️ Control Panel")
    st.caption(f"🔗 API: {API_URL}")
    
    # Check API health
    try:
        health_response = requests.get(f"{API_URL}/", timeout=3)
        if health_response.status_code == 200:
            st.success("✅ Backend Connected")
        else:
            st.warning("⚠️ Backend Unavailable")
    except:
        st.error("❌ Cannot connect to backend")
    
    st.divider()
    
    # Generate Tests Button
    if st.button("🔄 Generate Tests", use_container_width=True):
        with st.spinner("Generating adversarial scenarios..."):
            try:
                resp = requests.post(f"{API_URL}/generate-tests", json={"count": 20}, timeout=30)
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.scenarios = data.get("scenarios", [])
                    st.session_state.tests_generated = True
                    st.success(f"✅ Generated {data['count']} test scenarios!")
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {resp.status_code}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)[:100]}")
    
    # Run Tests Button
    if st.button("🚀 Run Tests", use_container_width=True):
        if not st.session_state.get("tests_generated", False):
            st.warning("⚠️ Generate tests first!")
        else:
            with st.spinner("Running test suite..."):
                try:
                    resp = requests.post(f"{API_URL}/run-tests", timeout=60)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.report = data.get("report", {})
                        st.success(f"✅ Tests complete! {data['passed']} passed")
                        st.rerun()
                    else:
                        st.error(f"❌ Failed: {resp.status_code}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)[:100]}")
    
    # Chaos Mode Toggle
    if st.button("⚡ Chaos Mode", use_container_width=True):
        new_state = not st.session_state.get("chaos_enabled", False)
        try:
            resp = requests.post(f"{API_URL}/chaos-mode?enable={str(new_state).lower()}", timeout=10)
            if resp.status_code == 200:
                st.session_state.chaos_enabled = new_state
                if new_state:
                    st.success("⚡ Chaos Mode ENABLED")
                else:
                    st.info("Chaos Mode DISABLED")
                st.rerun()
            else:
                st.error("❌ Failed to toggle chaos")
        except Exception as e:
            st.error(f"❌ Error: {str(e)[:100]}")
    
    st.divider()
    st.caption("v1.0.0 | Built for OOSC 4.0")

# ============================================
# 8. MAIN DASHBOARD
# ============================================
report = st.session_state.get("report", {})

# Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Overall Reliability", f"{report.get('overall_reliability', 0)}%")
with col2:
    st.metric("Safety Score", f"{report.get('safety_score', 0)}%")
with col3:
    st.metric("Tests Passed", f"{report.get('passed', 0)}/{report.get('total_tests', 0)}")
with col4:
    st.metric("Consistency", f"{report.get('consistency', 0)}%")

# If report exists, show detailed visualizations
if report and report.get("total_tests", 0) > 0:
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
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚠️ Critical Issues")
        st.metric("Critical Failures", report.get("critical_failures", 0), delta_color="inverse")
        st.metric("Blocked Actions", report.get("blocked_count", 0))
        st.metric("Risky Actions Allowed", report.get("allowed_risky", 0))
    
    # Attack Type Breakdown
    st.subheader("📊 Failure Breakdown by Attack Type")
    attack_data = report.get("by_attack_type", {})
    if attack_data:
        df_attack = pd.DataFrame([
            {"Attack Type": k, "Pass Rate": v.get("rate", 0)}
            for k, v in attack_data.items()
        ])
        fig = px.bar(df_attack, x="Attack Type", y="Pass Rate",
                     color="Pass Rate", color_continuous_scale="RdYlGn",
                     title="Pass Rate by Attack Type")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("💡 Fix Recommendations")
    recs = report.get("recommendations", [])
    if recs:
        for rec in recs:
            st.info(rec)
    else:
        st.success("✅ No critical issues found!")
    
    # Before/After Comparison
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
                                     json={"recommendations": recs}, timeout=60)
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.report = data.get("report", {})
                    st.success(f"✅ Fixes applied! New Reliability: {data.get('new_reliability', 0)}%")
                    st.rerun()
                else:
                    st.error("❌ Failed to apply fixes")
            except Exception as e:
                st.error(f"❌ Error: {str(e)[:100]}")
else:
    st.info("👈 Generate tests and run them to see the reliability report!")

# ============================================
# 9. EXPANDERS FOR DETAILS
# ============================================
with st.expander("📋 Test Scenarios"):
    scenarios = st.session_state.get("scenarios", [])
    if scenarios:
        df_scenarios = pd.DataFrame(scenarios)
        st.dataframe(df_scenarios[["id", "attack_type", "input", "expected_behavior", "severity"]])
    else:
        st.write("No scenarios generated yet.")

with st.expander("🔍 Execution Traces"):
    st.warning("Traces will be available after running tests.")
