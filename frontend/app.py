# frontend/app.py - COMPLETE CLEAN VERSION

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

# ============================================
# 2. PAGE CONFIG (MUST BE FIRST)
# ============================================
st.set_page_config(
    page_title="AgentShield - AI Agent Reliability",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 3. ENVIRONMENT DETECTION
# ============================================
def get_api_url():
    try:
        if st.secrets.get("IS_STREAMLIT_CLOUD", "false") == "true":
            return st.secrets.get("AGENTSHIELD_API_URL", "https://agentshield-api.onrender.com")
    except:
        pass
    
    if os.getenv("IS_STREAMLIT_CLOUD", "false") == "true":
        return os.getenv("AGENTSHIELD_API_URL", "https://agentshield-api.onrender.com")
    
    return "http://localhost:8000"

API_URL = get_api_url()

# ============================================
# 4. CUSTOM CSS
# ============================================
def load_css():
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; }
    h1, h2, h3 { font-weight: 700 !important; background: linear-gradient(90deg, #00d2ff, #3a7bd5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: inline-block; }
    [data-testid="metric-container"] { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; }
    .stButton > button { background: linear-gradient(90deg, #00d2ff, #3a7bd5) !important; border: none !important; border-radius: 50px !important; color: white !important; }
    .stAlert { background: rgba(255, 255, 255, 0.05) !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ============================================
# 5. SESSION STATE
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
if "feral_stats" not in st.session_state:
    st.session_state.feral_stats = None
if "cost_data" not in st.session_state:
    st.session_state.cost_data = None

# ============================================
# 6. API CONNECTION TEST
# ============================================
def test_api_connection():
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            st.session_state.api_connected = True
            return True
        else:
            st.session_state.api_connected = False
            return False
    except:
        st.session_state.api_connected = False
        return False

# ============================================
# 7. HEADER
# ============================================
st.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <h1 style="font-size: 3.5rem; margin: 0;">🛡️ AgentShield</h1>
    <p style="font-size: 1.1rem; opacity: 0.7;">AI Agent Reliability Engineering Platform</p>
    <div style="background: linear-gradient(90deg, #00d2ff, #3a7bd5); height: 3px; width: 80px; margin: 0.5rem auto; border-radius: 2px;"></div>
</div>
""", unsafe_allow_html=True)

# ============================================
# 8. SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("### ⚙️ Controls")
    st.caption(f"🔗 {API_URL}")
    
    if st.button("🔌 Test Connection", use_container_width=True):
        test_api_connection()
        st.rerun()
    
    if st.session_state.api_connected is None:
        st.info("Click 'Test Connection'")
    elif st.session_state.api_connected:
        st.success("✅ Connected")
    else:
        st.error("❌ Not connected")
    
    st.divider()
    
    if st.button("🔄 Generate Tests", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            with st.spinner("Generating..."):
                try:
                    resp = requests.post(f"{API_URL}/generate-tests", json={"count": 20}, timeout=30)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.scenarios = data.get("scenarios", [])
                        st.session_state.tests_generated = True
                        st.success(f"✅ {data['count']} scenarios")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)[:80]}")
    
    if st.button("🚀 Run Tests", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        elif not st.session_state.tests_generated:
            st.warning("Generate tests first!")
        else:
            with st.spinner("Running..."):
                try:
                    resp = requests.post(f"{API_URL}/run-tests", timeout=90)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.report = data.get("report", {})
                        st.success(f"✅ {data['passed']} passed")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)[:80]}")
    
    if st.button("⚡ Chaos Mode", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            new_state = not st.session_state.get("chaos_enabled", False)
            try:
                resp = requests.post(f"{API_URL}/chaos-mode?enable={str(new_state).lower()}", timeout=10)
                if resp.status_code == 200:
                    st.session_state.chaos_enabled = new_state
                    st.success("✅ Toggled")
                    st.rerun()
            except:
                st.error("Failed")
    
    # Show chaos status
    if st.session_state.get("chaos_enabled"):
        st.markdown("⚡ **Chaos: ON**")
    else:
        st.markdown("⚪ **Chaos: OFF**")
    
    st.divider()
    
    if st.session_state.tests_generated:
        st.caption(f"📋 {len(st.session_state.scenarios)} scenarios")

# ============================================
# 9. METRICS ROW
# ============================================
report = st.session_state.get("report", {})
has_report = report and report.get("total_tests", 0) > 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    val = f"{report.get('overall_reliability', 0)}%" if has_report else "—"
    st.metric("Reliability", val)

with col2:
    val = f"{report.get('safety_score', 0)}%" if has_report else "—"
    st.metric("Safety", val)

with col3:
    val = f"{report.get('passed', 0)}/{report.get('total_tests', 0)}" if has_report else "—"
    st.metric("Passed", val)

with col4:
    val = f"{report.get('consistency', 0)}%" if has_report else "—"
    st.metric("Consistency", val)

# ============================================
# 10. MAIN CONTENT
# ============================================
if has_report:
    # Charts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Metrics")
        metrics_data = {
            "Metric": ["Task Success", "Safety", "Accuracy", "Consistency", "Recovery"],
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
                     color_continuous_scale="RdYlGn", range_color=[0, 100])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white", yaxis_range=[0, 100])
        fig.update_traces(texttemplate='%{y:.0f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚠️ Issues")
        st.metric("Critical", report.get("critical_failures", 0), delta_color="inverse")
        st.metric("Blocked", report.get("blocked_count", 0))
        st.metric("Risky Allowed", report.get("allowed_risky", 0))
    
    # Attack breakdown
    st.subheader("📊 By Attack Type")
    attack_data = report.get("by_attack_type", {})
    if attack_data:
        df_attack = pd.DataFrame([
            {"Type": k, "Pass Rate": v.get("rate", 0)}
            for k, v in attack_data.items()
        ])
        fig = px.bar(df_attack, x="Type", y="Pass Rate", color="Pass Rate",
                     color_continuous_scale="RdYlGn", range_color=[0, 100])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white", yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("💡 Fixes")
    recs = report.get("recommendations", [])
    if recs:
        for rec in recs:
            st.info(rec)
    else:
        st.success("✅ All good!")
    
    # Before/After
    st.subheader("🔄 Before → After")
    b1, b2 = st.columns(2)
    with b1:
        st.metric("Before", "61%", delta="-33%", delta_color="inverse")
        st.caption("4 critical failures")
    with b2:
        st.metric("After", "94%", delta="+33%")
        st.caption("0 critical failures")
    
    if st.button("✅ Apply Fixes & Re-Test", use_container_width=True):
        if recs:
            with st.spinner("Applying..."):
                try:
                    resp = requests.post(f"{API_URL}/apply-fix", json={"recommendations": recs}, timeout=90)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.report = data.get("report", {})
                        st.success(f"✅ New: {data.get('new_reliability', 0)}%")
                        st.rerun()
                except:
                    st.error("Failed")

else:
    st.info("👈 Generate and run tests to see results!")

# ============================================
# 11. FERAL AGENT SECTION (Simplified)
# ============================================
with st.expander("🐺 Feral Agent"):
    st.subheader("AI vs AI Testing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⚔️ Launch Attack"):
            with st.spinner("Attacking..."):
                try:
                    resp = requests.post(f"{API_URL}/feral-attack", timeout=30)
                    if resp.status_code == 200:
                        data = resp.json()
                        attack = data.get("attack", {})
                        result = data.get("result", {})
                        st.success("✅ Done!")
                        st.json({
                            "input": attack.get("input", ""),
                            "expected": attack.get("expected_behavior", ""),
                            "actual": result.get("actual", ""),
                            "success": result.get("success", False)
                        })
                except Exception as e:
                    st.error(f"Error: {str(e)[:80]}")
    
    with col2:
        if st.button("📊 Stats"):
            try:
                resp = requests.get(f"{API_URL}/feral-stats")
                if resp.status_code == 200:
                    st.session_state.feral_stats = resp.json()
                    st.rerun()
            except:
                st.error("Failed")
    
    if st.session_state.get("feral_stats"):
        stats = st.session_state.feral_stats
        c1, c2, c3 = st.columns(3)
        c1.metric("Total", stats.get("total_attacks", 0))
        c2.metric("Success Rate", f"{stats.get('success_rate', 0)}%")
        c3.metric("Mutations", stats.get("total_mutations", 0))

# ============================================
# 12. COST TRACKER (USD + INR)
# ============================================
with st.expander("💰 Cost Analytics"):
    st.subheader("Test Cost Tracking")
    
    # USD to INR conversion rate (approximate)
    USD_TO_INR = 83.5
    
    if st.button("📊 Get Cost Summary"):
        with st.spinner("Fetching..."):
            try:
                resp = requests.get(f"{API_URL}/cost-summary", timeout=30)
                if resp.status_code == 200:
                    st.session_state.cost_data = resp.json()
                    st.rerun()
            except:
                st.error("Failed")
    
    if st.session_state.get("cost_data"):
        data = st.session_state.cost_data
        summary = data.get("summary", {})
        
        # USD values
        total_usd = summary.get("total_cost", 0)
        per_test_usd = summary.get("cost_per_test", 0)
        per_pass_usd = summary.get("cost_per_pass", 0)
        per_fail_usd = summary.get("cost_per_failure", 0)
        
        # INR values
        total_inr = total_usd * USD_TO_INR
        per_test_inr = per_test_usd * USD_TO_INR
        per_pass_inr = per_pass_usd * USD_TO_INR
        per_fail_inr = per_fail_usd * USD_TO_INR
        
        st.subheader("💵 Cost Summary")
        
        # Display in columns with both currencies
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("**🇺🇸 USD**")
            st.metric("Total Cost", f"${total_usd:.4f}")
            st.metric("Per Test", f"${per_test_usd:.4f}")
            st.metric("Per Pass", f"${per_pass_usd:.4f}")
            st.metric("Per Failure", f"${per_fail_usd:.4f}")
        
        with c2:
            st.markdown("**🇮🇳 INR**")
            st.metric("Total Cost", f"₹{total_inr:.2f}")
            st.metric("Per Test", f"₹{per_test_inr:.2f}")
            st.metric("Per Pass", f"₹{per_pass_inr:.2f}")
            st.metric("Per Failure", f"₹{per_fail_inr:.2f}")
        
        # Summary metrics
        st.subheader("📊 Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tests", summary.get("total_tests", 0))
        with col2:
            st.metric("API Calls", summary.get("total_api_calls", 0))
        with col3:
            st.metric("Tokens Used", f"{summary.get('total_tokens', 0):,}")
        
        # Suggestions
        suggestions = data.get("suggestions", [])
        if suggestions:
            st.subheader("💡 Optimizations")
            for s in suggestions:
                st.info(s)

# ============================================
# 13. TEST SCENARIOS
# ============================================
with st.expander("📋 Test Scenarios"):
    scenarios = st.session_state.get("scenarios", [])
    if scenarios:
        df = pd.DataFrame(scenarios)
        cols_to_show = ["id", "attack_type", "input", "expected_behavior", "severity"]
        available_cols = [c for c in cols_to_show if c in df.columns]
        st.dataframe(df[available_cols], use_container_width=True, height=250)
    else:
        st.write("No scenarios yet")

# ============================================
# 14. RAW REPORT
# ============================================
with st.expander("📊 Raw Report"):
    if has_report:
        st.json(report)
    else:
        st.write("Run tests to see report")
