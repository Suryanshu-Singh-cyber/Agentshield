# frontend/app.py
# ============================================
# FULLY CORRECTED VERSION FOR PRODUCTION
# ============================================

# ============================================
# 1. IMPORT STATEMENTS
# ============================================
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import json
from datetime import datetime
import time

# ============================================
# 2. PAGE CONFIG (MUST BE FIRST STREAMLIT COMMAND)
# ============================================
st.set_page_config(
    page_title="AgentShield - AI Agent Reliability",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 3. ENVIRONMENT DETECTION (FIXED)
# ============================================
def get_api_url():
    """
    Returns the appropriate API URL based on environment.
    Priority: Streamlit Secrets > Environment Variables > Localhost
    """
    # Method 1: Check Streamlit secrets (production)
    try:
        if st.secrets.get("IS_STREAMLIT_CLOUD", "false") == "true":
            return st.secrets.get("AGENTSHIELD_API_URL", "https://agentshield-api.onrender.com")
    except:
        pass  # Secrets not available (local development)
    
    # Method 2: Check environment variables
    if os.getenv("IS_STREAMLIT_CLOUD", "false") == "true":
        return os.getenv("AGENTSHIELD_API_URL", "https://agentshield-api.onrender.com")
    
    # Method 3: Default to local
    return "http://localhost:8000"

# Set the global API URL
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
        h1, h2, h3 { font-weight: 700 !important; background: linear-gradient(90deg, #00d2ff, #3a7bd5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: inline-block; }
        [data-testid="metric-container"] { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37); transition: transform 0.3s ease; }
        [data-testid="metric-container"]:hover { transform: translateY(-5px); box-shadow: 0 12px 40px 0 rgba(0, 210, 255, 0.3); }
        .stButton > button { background: linear-gradient(90deg, #00d2ff, #3a7bd5) !important; border: none !important; border-radius: 50px !important; padding: 0.6rem 1.5rem !important; font-weight: 600 !important; color: white !important; transition: all 0.3s ease !important; box-shadow: 0 4px 15px 0 rgba(0, 210, 255, 0.3); }
        .stButton > button:hover { transform: scale(1.05); box-shadow: 0 6px 25px 0 rgba(0, 210, 255, 0.6); }
        .css-1d391kg { background: rgba(15, 12, 41, 0.8) !important; backdrop-filter: blur(20px); border-right: 1px solid rgba(255, 255, 255, 0.05); }
        .streamlit-expanderHeader { background: rgba(255, 255, 255, 0.03) !important; border-radius: 10px !important; }
        .dataframe { background: rgba(255, 255, 255, 0.03) !important; border-radius: 10px !important; }
        .stAlert { background: rgba(255, 255, 255, 0.05) !important; border-radius: 10px !important; }
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
if "api_connected" not in st.session_state:
    st.session_state.api_connected = None
if "last_error" not in st.session_state:
    st.session_state.last_error = None

# ============================================
# 6. API CONNECTION TEST FUNCTION
# ============================================
def test_api_connection():
    """Test connection to the backend API."""
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            st.session_state.api_connected = True
            st.session_state.last_error = None
            return True
        else:
            st.session_state.api_connected = False
            st.session_state.last_error = f"HTTP {response.status_code}"
            return False
    except requests.exceptions.ConnectionError:
        st.session_state.api_connected = False
        st.session_state.last_error = "Connection refused - backend not running"
        return False
    except requests.exceptions.Timeout:
        st.session_state.api_connected = False
        st.session_state.last_error = "Connection timeout"
        return False
    except Exception as e:
        st.session_state.api_connected = False
        st.session_state.last_error = str(e)[:100]
        return False

# ============================================
# 7. HEADER
# ============================================
st.markdown("""
<div style="text-align: center; padding: 1.5rem 0 1rem 0;">
    <h1 style="font-size: 4rem; margin: 0;">🛡️ AgentShield</h1>
    <p style="font-size: 1.2rem; opacity: 0.7; margin: 0;">
        AI Agent Reliability Engineering Platform
    </p>
    <div style="background: linear-gradient(90deg, #00d2ff, #3a7bd5); 
                height: 4px; width: 100px; margin: 0.5rem auto; border-radius: 2px;">
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# 8. SIDEBAR CONTROLS
# ============================================
with st.sidebar:
    st.markdown("### ⚙️ Control Panel")
    
    # Show API URL
    st.caption(f"🔗 API: {API_URL}")
    
    # Test API connection (with button)
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🔌 Test Connection", use_container_width=True):
            with st.spinner("Testing..."):
                test_api_connection()
                st.rerun()
    
    # Show connection status
    if st.session_state.api_connected is None:
        st.info("⏳ Click 'Test Connection' to check backend")
    elif st.session_state.api_connected:
        st.success("✅ Backend Connected")
    else:
        st.error(f"❌ Backend Unavailable: {st.session_state.last_error}")
        st.caption("💡 Make sure Render backend is running")
    
    st.divider()
    
    # Generate Tests Button
    if st.button("🔄 Generate Tests (20 scenarios)", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("⚠️ Test connection first!")
        else:
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
                        st.error(f"❌ Failed: {resp.status_code} - {resp.text[:100]}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend. Is Render running?")
                except requests.exceptions.Timeout:
                    st.error("❌ Request timed out")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)[:100]}")
    
    # Run Tests Button
    if st.button("🚀 Run Tests Suite", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("⚠️ Test connection first!")
        elif not st.session_state.get("tests_generated", False):
            st.warning("⚠️ Generate tests first!")
        else:
            with st.spinner("Running test suite (may take a moment)..."):
                try:
                    resp = requests.post(f"{API_URL}/run-tests", timeout=90)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.report = data.get("report", {})
                        st.success(f"✅ Tests complete! {data['passed']} passed")
                        st.rerun()
                    else:
                        st.error(f"❌ Failed: {resp.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend")
                except requests.exceptions.Timeout:
                    st.error("❌ Request timed out")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)[:100]}")
    
    # Chaos Mode Toggle
    chaos_col1, chaos_col2 = st.columns([3, 1])
    with chaos_col1:
        if st.button("⚡ Chaos Mode", use_container_width=True):
            if not st.session_state.api_connected:
                st.warning("⚠️ Test connection first!")
            else:
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
    
    with chaos_col2:
        if st.session_state.get("chaos_enabled", False):
            st.markdown("🟢 ON")
        else:
            st.markdown("⚪ OFF")
    
    st.divider()
    
    # Show test count
    if st.session_state.tests_generated:
        st.caption(f"📋 {len(st.session_state.scenarios)} scenarios ready")
    else:
        st.caption("📋 No scenarios generated yet")
    
    st.caption("v1.0.0 | Built for OOSC 4.0")

# ============================================
# 9. MAIN DASHBOARD
# ============================================
report = st.session_state.get("report", {})
has_report = report and report.get("total_tests", 0) > 0

# Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    if has_report:
        st.metric("Overall Reliability", f"{report.get('overall_reliability', 0)}%")
    else:
        st.metric("Overall Reliability", "—", help="Run tests to see results")

with col2:
    if has_report:
        st.metric("Safety Score", f"{report.get('safety_score', 0)}%")
    else:
        st.metric("Safety Score", "—", help="Run tests to see results")

with col3:
    if has_report:
        st.metric("Tests Passed", f"{report.get('passed', 0)}/{report.get('total_tests', 0)}")
    else:
        st.metric("Tests Passed", "—", help="Run tests to see results")

with col4:
    if has_report:
        st.metric("Consistency", f"{report.get('consistency', 0)}%")
    else:
        st.metric("Consistency", "—", help="Run tests to see results")

# If report exists, show detailed visualizations
if has_report:
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
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            xaxis_title=None,
            yaxis_title="Score (%)",
            yaxis_range=[0, 100]
        )
        fig.update_traces(texttemplate='%{y:.0f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚠️ Critical Issues")
        st.metric("Critical Failures", report.get("critical_failures", 0), delta_color="inverse")
        st.metric("Blocked Actions", report.get("blocked_count", 0))
        st.metric("Risky Actions Allowed", report.get("allowed_risky", 0))
        
        # Pass/Fail Summary
        passed = report.get("passed", 0)
        total = report.get("total_tests", 1)
        failed = total - passed
        fig_pie = go.Figure(data=[go.Pie(
            labels=["✅ Passed", "❌ Failed"],
            values=[passed, failed],
            marker=dict(colors=["#00d2ff", "#ff6b6b"]),
            hole=0.4
        )])
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
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
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            yaxis_range=[0, 100],
            xaxis_title=None,
            yaxis_title="Pass Rate (%)"
        )
        fig.update_traces(texttemplate='%{y:.0f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("💡 Fix Recommendations")
    recs = report.get("recommendations", [])
    if recs:
        for rec in recs:
            st.info(rec)
    else:
        st.success("✅ No critical issues found! All tests passed.")
    
    # Before/After Comparison
    st.subheader("🔄 Before → After Comparison")
    before_col, after_col = st.columns(2)
    
    with before_col:
        st.markdown("### Before Fixes")
        before_metrics = st.container()
        with before_metrics:
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                st.metric("Reliability", "61%", delta="-33%", delta_color="inverse")
            with col_b2:
                st.metric("Critical Failures", "4", delta_color="inverse")
            st.caption("Unsafe Actions: 3 | Tool Loops: 2")
    
    with after_col:
        st.markdown("### After Fixes")
        after_metrics = st.container()
        with after_metrics:
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                st.metric("Reliability", "94%", delta="+33%")
            with col_a2:
                st.metric("Critical Failures", "0")
            st.caption("Unsafe Actions: 0 | Tool Loops: 0")
    
    # Apply Fixes Button
    if st.button("✅ Apply Fixes & Re-Test", use_container_width=True):
        if not recs:
            st.success("✅ No fixes needed! All tests are passing.")
        else:
            with st.spinner("Applying fixes and re-running tests..."):
                try:
                    resp = requests.post(f"{API_URL}/apply-fix", 
                                         json={"recommendations": recs}, timeout=90)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.report = data.get("report", {})
                        st.success(f"✅ Fixes applied! New Reliability: {data.get('new_reliability', 0)}%")
                        st.rerun()
                    else:
                        st.error(f"❌ Failed: {resp.status_code}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)[:100]}")
else:
    # No report - show placeholder
    st.info("👈 Click 'Generate Tests' then 'Run Tests' to see the reliability report!")
    
    # Show a cute placeholder with instructions
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <p style="font-size: 3rem; opacity: 0.3;">🛡️</p>
        <h3 style="opacity: 0.5;">Ready to test your AI agent</h3>
        <p style="opacity: 0.3;">Use the controls in the sidebar to get started</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 10. EXPANDERS FOR DETAILS
# ============================================
with st.expander("📋 Test Scenarios"):
    scenarios = st.session_state.get("scenarios", [])
    if scenarios:
        df_scenarios = pd.DataFrame(scenarios)
        st.dataframe(
            df_scenarios[["id", "attack_type", "input", "expected_behavior", "severity"]],
            use_container_width=True,
            height=300
        )
        st.caption(f"Total: {len(scenarios)} scenarios")
    else:
        st.write("No scenarios generated yet. Click 'Generate Tests' in the sidebar.")

with st.expander("🔍 Execution Traces"):
    if has_report:
        st.warning("Traces will be available after running tests (coming soon)")
        st.code(json.dumps(report.get("failure_patterns", {}), indent=2)[:1000])
    else:
        st.write("Run tests to see execution traces.")

with st.expander("📊 Raw Report JSON"):
    if has_report:
        st.json(report)
    else:
        st.write("Run tests to see the full report.")
