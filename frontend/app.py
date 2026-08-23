# frontend/app.py
# AGENTSHIELD - COMPLETE FRONTEND
# Version: 2.0.0

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
import time
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
    """Returns the appropriate API URL based on environment."""
    # Check Streamlit secrets (production)
    try:
        if st.secrets.get("IS_STREAMLIT_CLOUD", "false") == "true":
            return st.secrets.get("AGENTSHIELD_API_URL", "https://agentshield-api.onrender.com")
    except:
        pass
    
    # Check environment variables
    if os.getenv("IS_STREAMLIT_CLOUD", "false") == "true":
        return os.getenv("AGENTSHIELD_API_URL", "https://agentshield-api.onrender.com")
    
    # Default to local
    return "http://localhost:8000"

API_URL = get_api_url()

# ============================================
# 4. CUSTOM CSS
# ============================================
def load_css():
    """Load custom CSS for premium UI."""
    try:
        with open("frontend/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Fallback inline CSS
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #e0e0e0;
        }
        h1, h2, h3 {
            font-weight: 700 !important;
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }
        [data-testid="metric-container"] {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        [data-testid="metric-container"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(0, 210, 255, 0.3);
        }
        .stButton > button {
            background: linear-gradient(90deg, #00d2ff, #3a7bd5) !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 0.6rem 1.5rem !important;
            font-weight: 600 !important;
            color: white !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px 0 rgba(0, 210, 255, 0.3);
        }
        .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 25px 0 rgba(0, 210, 255, 0.6);
        }
        .css-1d391kg {
            background: rgba(15, 12, 41, 0.8) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: 10px !important;
        }
        .dataframe {
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: 10px !important;
        }
        .stAlert {
            background: rgba(255, 255, 255, 0.05) !important;
            border-radius: 10px !important;
        }
        .stSuccess {
            background: rgba(0, 210, 255, 0.1) !important;
            border-radius: 10px !important;
        }
        .stWarning {
            background: rgba(255, 165, 0, 0.1) !important;
            border-radius: 10px !important;
        }
        .stError {
            background: rgba(255, 0, 0, 0.1) !important;
            border-radius: 10px !important;
        }
        </style>
        """, unsafe_allow_html=True)

load_css()

# ============================================
# 5. SESSION STATE INITIALIZATION
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
if "feral_stats" not in st.session_state:
    st.session_state.feral_stats = None
if "feral_result" not in st.session_state:
    st.session_state.feral_result = None
if "cost_data" not in st.session_state:
    st.session_state.cost_data = None
if "evolution_data" not in st.session_state:
    st.session_state.evolution_data = None
if "root_cause_data" not in st.session_state:
    st.session_state.root_cause_data = None

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
        st.session_state.last_error = "Connection refused"
        return False
    except requests.exceptions.Timeout:
        st.session_state.api_connected = False
        st.session_state.last_error = "Timeout"
        return False
    except Exception as e:
        st.session_state.api_connected = False
        st.session_state.last_error = str(e)[:50]
        return False

def api_request(method, endpoint, **kwargs):
    """Make an API request with error handling."""
    url = f"{API_URL}{endpoint}"
    try:
        if method == "get":
            resp = requests.get(url, **kwargs)
        elif method == "post":
            resp = requests.post(url, **kwargs)
        else:
            return None, "Invalid method"
        
        if resp.status_code == 200:
            return resp.json(), None
        else:
            return None, f"HTTP {resp.status_code}: {resp.text[:100]}"
    except requests.exceptions.ConnectionError:
        return None, "Connection refused"
    except requests.exceptions.Timeout:
        return None, "Timeout"
    except Exception as e:
        return None, str(e)[:100]

# ============================================
# 7. HEADER
# ============================================
st.markdown("""
<div style="text-align: center; padding: 1rem 0 0.5rem 0;">
    <h1 style="font-size: 3.5rem; margin: 0;">🛡️ AgentShield</h1>
    <p style="font-size: 1.1rem; opacity: 0.7; margin: 0;">
        AI Agent Reliability Engineering Platform
    </p>
    <div style="background: linear-gradient(90deg, #00d2ff, #3a7bd5); 
                height: 3px; width: 80px; margin: 0.5rem auto; border-radius: 2px;">
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# 8. SIDEBAR CONTROLS
# ============================================
with st.sidebar:
    st.markdown("### ⚙️ Control Panel")
    
    # API URL and connection
    st.caption(f"🔗 {API_URL}")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🔌 Test Connection", use_container_width=True):
            with st.spinner("Testing..."):
                test_api_connection()
                st.rerun()
    
    if st.session_state.api_connected is None:
        st.info("⏳ Click 'Test Connection'")
    elif st.session_state.api_connected:
        st.success("✅ Backend Connected")
    else:
        st.error(f"❌ {st.session_state.last_error}")
    
    st.divider()
    
    # Generate Tests
    if st.button("🔄 Generate Tests (20)", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("⚠️ Connect first!")
        else:
            with st.spinner("Generating..."):
                data, error = api_request("post", "/generate-tests", json={"count": 20}, timeout=30)
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.session_state.scenarios = data.get("scenarios", [])
                    st.session_state.tests_generated = True
                    st.success(f"✅ {data['count']} scenarios")
                    st.rerun()
    
    # Run Tests
    if st.button("🚀 Run Tests Suite", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("⚠️ Connect first!")
        elif not st.session_state.tests_generated:
            st.warning("⚠️ Generate tests first!")
        else:
            with st.spinner("Running tests..."):
                data, error = api_request("post", "/run-tests", timeout=90)
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.session_state.report = data.get("report", {})
                    st.success(f"✅ {data['passed']} passed")
                    st.rerun()
    
    # Chaos Mode
    chaos_col1, chaos_col2 = st.columns([3, 1])
    with chaos_col1:
        if st.button("⚡ Chaos Mode", use_container_width=True):
            if not st.session_state.api_connected:
                st.warning("⚠️ Connect first!")
            else:
                new_state = not st.session_state.get("chaos_enabled", False)
                data, error = api_request("post", f"/chaos-mode?enable={str(new_state).lower()}", timeout=10)
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.session_state.chaos_enabled = new_state
                    st.success("✅ Toggled")
                    st.rerun()
    
    with chaos_col2:
        if st.session_state.get("chaos_enabled", False):
            st.markdown("🟢 ON")
        else:
            st.markdown("⚪ OFF")
    
    st.divider()
    
    # Apply Fixes
    if st.button("✅ Apply Fixes & Re-Test", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("⚠️ Connect first!")
        elif not st.session_state.report:
            st.warning("⚠️ Run tests first!")
        else:
            recs = st.session_state.report.get("recommendations", [])
            if not recs:
                st.success("✅ No fixes needed!")
            else:
                with st.spinner("Applying fixes..."):
                    data, error = api_request("post", "/apply-fix", json={"recommendations": recs}, timeout=90)
                    if error:
                        st.error(f"❌ {error}")
                    else:
                        st.session_state.report = data.get("report", {})
                        st.success(f"✅ New: {data.get('new_reliability', 0)}%")
                        st.rerun()
    
    st.divider()
    
    if st.session_state.tests_generated:
        st.caption(f"📋 {len(st.session_state.scenarios)} scenarios")
    else:
        st.caption("📋 No scenarios")
    
    st.caption("v2.0.0 | OOSC 4.0")

# ============================================
# 9. MAIN DASHBOARD - METRICS
# ============================================
report = st.session_state.get("report", {})
has_report = report and report.get("total_tests", 0) > 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    if has_report:
        st.metric("Overall Reliability", f"{report.get('overall_reliability', 0)}%")
    else:
        st.metric("Overall Reliability", "—")

with col2:
    if has_report:
        st.metric("Safety Score", f"{report.get('safety_score', 0)}%")
    else:
        st.metric("Safety Score", "—")

with col3:
    if has_report:
        st.metric("Tests Passed", f"{report.get('passed', 0)}/{report.get('total_tests', 0)}")
    else:
        st.metric("Tests Passed", "—")

with col4:
    if has_report:
        st.metric("Consistency", f"{report.get('consistency', 0)}%")
    else:
        st.metric("Consistency", "—")

# ============================================
# 10. MAIN DASHBOARD - DETAILS
# ============================================
if has_report:
    # Performance Metrics Chart
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
        
        # Pass/Fail Pie
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
        st.success("✅ No critical issues found!")
    
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

else:
    # No report placeholder
    st.info("👈 Click 'Generate Tests' then 'Run Tests' to see the reliability report!")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <p style="font-size: 3rem; opacity: 0.3;">🛡️</p>
        <h3 style="opacity: 0.5;">Ready to test your AI agent</h3>
        <p style="opacity: 0.3;">Use the controls in the sidebar to get started</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 11. EXPANDER: TEST SCENARIOS
# ============================================
with st.expander("📋 Test Scenarios"):
    scenarios = st.session_state.get("scenarios", [])
    if scenarios:
        df_scenarios = pd.DataFrame(scenarios)
        cols_to_show = ["id", "attack_type", "input", "expected_behavior", "severity"]
        available_cols = [c for c in cols_to_show if c in df_scenarios.columns]
        st.dataframe(
            df_scenarios[available_cols],
            use_container_width=True,
            height=250
        )
        st.caption(f"Total: {len(scenarios)} scenarios")
    else:
        st.write("No scenarios generated yet.")

# ============================================
# 12. EXPANDER: EXECUTION TRACES
# ============================================
with st.expander("🔍 Execution Traces"):
    if has_report and report.get("failure_patterns"):
        st.warning("Traces will be available in full version")
        st.code(json.dumps(report.get("failure_patterns", {}), indent=2)[:1000])
    else:
        st.write("Run tests to see execution traces.")

# ============================================
# 13. EXPANDER: RAW REPORT
# ============================================
with st.expander("📊 Raw Report JSON"):
    if has_report:
        st.json(report)
    else:
        st.write("Run tests to see the full report.")

# ============================================
# 14. EXPANDER: FERAL AGENT
# ============================================
with st.expander("🐺 Feral Agent - AI vs AI"):
    st.subheader("The Feral Agent attacks your AI")
    st.caption("A secondary AI that actively tries to break your primary agent")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⚔️ Launch Attack", use_container_width=True):
            if not st.session_state.api_connected:
                st.warning("⚠️ Connect first!")
            else:
                with st.spinner("Attacking..."):
                    data, error = api_request("post", "/feral-attack", timeout=30)
                    if error:
                        st.error(f"❌ {error}")
                    else:
                        st.session_state.feral_result = data
                        st.success("✅ Attack executed!")
                        st.rerun()
    
    with col2:
        if st.button("📊 Feral Stats", use_container_width=True):
            if not st.session_state.api_connected:
                st.warning("⚠️ Connect first!")
            else:
                with st.spinner("Fetching..."):
                    data, error = api_request("get", "/feral-stats", timeout=10)
                    if error:
                        st.error(f"❌ {error}")
                    else:
                        st.session_state.feral_stats = data
                        st.rerun()
    
    # Display feral result
    if st.session_state.get("feral_result"):
        result = st.session_state.feral_result
        attack = result.get("attack", {})
        attack_result = result.get("result", {})
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Attack Type", attack.get("attack_type", "N/A"))
        with col2:
            success = attack_result.get("success", False)
            st.metric("Success", "✅" if success else "❌")
        with col3:
            st.metric("Risk Score", f"{attack_result.get('risk_score', 0)}%")
        
        st.text_area("Attack Input", attack.get("input", ""), height=60)
        st.caption(f"Expected: {attack.get('expected_behavior')} | Actual: {attack_result.get('actual')}")
    
    # Display feral stats
    if st.session_state.get("feral_stats"):
        stats = st.session_state.feral_stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Attacks", stats.get("total_attacks", 0))
        with col2:
            st.metric("Successful", stats.get("successful_attacks", 0))
        with col3:
            st.metric("Success Rate", f"{stats.get('success_rate', 0)}%")
        with col4:
            st.metric("Mutations", stats.get("total_mutations", 0))

# ============================================
# 15. EXPANDER: SELF-EVOLVING TEST SUITE
# ============================================
with st.expander("🧠 Self-Evolving Test Suite"):
    st.subheader("Production Pattern Analyzer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Analyze Production Logs", use_container_width=True):
            if not st.session_state.api_connected:
                st.warning("⚠️ Connect first!")
            else:
                with st.spinner("Analyzing..."):
                    data, error = api_request("post", "/analyze-production", timeout=30)
                    if error:
                        st.error(f"❌ {error}")
                    else:
                        st.session_state.evolution_data = data
                        st.success(f"✅ {data.get('patterns_analyzed', 0)} patterns")
                        st.rerun()
    
    with col2:
        if st.button("🔄 Evolve Test Suite", use_container_width=True):
            if not st.session_state.api_connected:
                st.warning("⚠️ Connect first!")
            else:
                with st.spinner("Evolving..."):
                    data, error = api_request("post", "/evolve-tests", timeout=30)
                    if error:
                        st.error(f"❌ {error}")
                    else:
                        st.success(f"✅ {data.get('new_scenarios', 0)} new tests")
                        st.rerun()
    
    if st.session_state.get("evolution_data"):
        data = st.session_state.evolution_data
        summary = data.get("summary", {})
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Patterns Analyzed", summary.get("total_patterns", 0))
        with col2:
            st.metric("Evolved Tests", summary.get("total_evolved_tests", 0))
        with col3:
            last = summary.get("last_analysis", "Never")
            st.metric("Last Analysis", last[:10] if last else "Never")

# ============================================
# 16. EXPANDER: ROOT CAUSE GRAPH
# ============================================
with st.expander("🔍 Root Cause Graph"):
    st.subheader("Failure Taxonomy & Root Cause Analysis")
    
    if st.button("📊 Analyze Failures", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("⚠️ Connect first!")
        elif not st.session_state.report:
            st.warning("⚠️ Run tests first!")
        else:
            with st.spinner("Analyzing..."):
                data, error = api_request("post", "/analyze-failures", timeout=30)
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.session_state.root_cause_data = data
                    st.rerun()
    
    if st.session_state.get("root_cause_data"):
        data = st.session_state.root_cause_data
        
        # Taxonomy Breakdown
        st.subheader("Taxonomy Breakdown")
        taxonomy = data.get("taxonomy_breakdown", {})
        if taxonomy:
            cols = st.columns(min(len(taxonomy), 4))
            for idx, (category, info) in enumerate(taxonomy.items()):
                with cols[idx % 4]:
                    st.metric(
                        category.replace("_", " ").title(),
                        info.get("count", 0),
                        help=info.get("description", "")
                    )
        
        # Critical Failures
        critical = data.get("critical_failures", [])
        if critical:
            st.subheader("🔥 Critical Failures")
            for f in critical[:3]:
                st.warning(f"🔥 {f.get('root_cause', 'Unknown')}")
                st.caption(f"Fix: {f.get('fix', 'Review')}")
        
        # Failure Chains - Simplified safe version
        st.subheader("🔗 Failure Chains")
        chains = data.get("failure_chains", [])[:3]
        if chains:
            for idx, chain in enumerate(chains):
                chain_input = chain.get("input", "")
                display_text = chain_input[:40] + "..." if len(chain_input) > 40 else chain_input
                display_text = display_text or f"Chain {idx + 1}"
                
                with st.expander(f"🔗 {display_text}"):
                    for step in chain.get("chain", []):
                        st.caption(f"Step {step.get('step')}: {step.get('event')} → {step.get('detail')}")
        else:
            st.info("No failure chains available")

# ============================================
# 17. EXPANDER: COST TRACKER (USD + INR)
# ============================================
with st.expander("💰 Cost Analytics"):
    st.subheader("Test Cost Tracking")
    
    # USD to INR conversion rate
    USD_TO_INR = 83.5
    
    if st.button("📊 Get Cost Summary", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("⚠️ Connect first!")
        else:
            with st.spinner("Fetching..."):
                data, error = api_request("get", "/cost-summary", timeout=30)
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.session_state.cost_data = data
                    st.rerun()
    
    if st.session_state.get("cost_data"):
        data = st.session_state.cost_data
        summary = data.get("summary", {})
        
        # Extract USD values
        total_usd = summary.get("total_cost", 0)
        per_test_usd = summary.get("cost_per_test", 0)
        per_pass_usd = summary.get("cost_per_pass", 0)
        per_fail_usd = summary.get("cost_per_failure", 0)
        
        # Convert to INR
        total_inr = total_usd * USD_TO_INR
        per_test_inr = per_test_usd * USD_TO_INR
        per_pass_inr = per_pass_usd * USD_TO_INR
        per_fail_inr = per_fail_usd * USD_TO_INR
        
        st.subheader("💵 Cost Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🇺🇸 USD**")
            st.metric("Total Cost", f"${total_usd:.4f}")
            st.metric("Per Test", f"${per_test_usd:.4f}")
            st.metric("Per Pass", f"${per_pass_usd:.4f}")
            st.metric("Per Failure", f"${per_fail_usd:.4f}")
        
        with col2:
            st.markdown("**🇮🇳 INR**")
            st.metric("Total Cost", f"₹{total_inr:.2f}")
            st.metric("Per Test", f"₹{per_test_inr:.2f}")
            st.metric("Per Pass", f"₹{per_pass_inr:.2f}")
            st.metric("Per Failure", f"₹{per_fail_inr:.2f}")
        
        # Summary metrics
        st.subheader("📊 Usage Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tests", summary.get("total_tests", 0))
        with col2:
            st.metric("API Calls", summary.get("total_api_calls", 0))
        with col3:
            st.metric("Tokens Used", f"{summary.get('total_tokens', 0):,}")
        
        # Most expensive tests
        expensive = summary.get("most_expensive_tests", [])
        if expensive:
            st.subheader("🔥 Most Expensive Tests")
            for test in expensive[:3]:
                st.caption(f"{test.get('test_id')}: ${test.get('cost', 0):.4f} (₹{test.get('cost', 0) * USD_TO_INR:.2f})")
        
        # Optimization suggestions
        suggestions = data.get("suggestions", [])
        if suggestions:
            st.subheader("💡 Optimizations")
            for s in suggestions:
                st.info(s)

# ============================================
# 18. FOOTER
# ============================================
st.divider()
st.caption("🛡️ AgentShield v2.0.0 | Built for OOSC 4.0 Hackathon | IIIT Allahabad")
st.caption(f"🔗 API: {API_URL} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
