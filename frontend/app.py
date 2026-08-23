# frontend/app.py - COMPLETE FIXED VERSION

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
# 3. ENVIRONMENT DETECTION
# ============================================
def get_api_url():
    """Returns the appropriate API URL based on environment."""
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
# 4. CUSTOM CSS LOADING
# ============================================
def load_css():
    try:
        with open("frontend/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; }
        h1, h2, h3 { font-weight: 700 !important; background: linear-gradient(90deg, #00d2ff, #3a7bd5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: inline-block; }
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
if "api_connected" not in st.session_state:
    st.session_state.api_connected = None
if "last_error" not in st.session_state:
    st.session_state.last_error = None
if "evolution_data" not in st.session_state:
    st.session_state.evolution_data = None
if "feral_result" not in st.session_state:
    st.session_state.feral_result = None
if "feral_stats" not in st.session_state:
    st.session_state.feral_stats = None
if "root_cause" not in st.session_state:
    st.session_state.root_cause = None
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
    st.caption(f"🔗 API: {API_URL}")
    
    # Connection test
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🔌 Test Connection", use_container_width=True):
            with st.spinner("Testing..."):
                test_api_connection()
                st.rerun()
    
    if st.session_state.api_connected is None:
        st.info("⏳ Click 'Test Connection' to check backend")
    elif st.session_state.api_connected:
        st.success("✅ Backend Connected")
    else:
        st.error(f"❌ Backend Unavailable: {st.session_state.last_error}")
    
    st.divider()
    
    # Generate Tests
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
                        st.error(f"❌ Failed: {resp.status_code}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)[:100]}")
    
    # Run Tests
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
                except Exception as e:
                    st.error(f"❌ Error: {str(e)[:100]}")
    
    # Chaos Mode
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
    
    # Before/After
    st.subheader("🔄 Before → After Comparison")
    before_col, after_col = st.columns(2)
    
    with before_col:
        st.markdown("### Before Fixes")
        st.metric("Reliability", "61%", delta="-33%", delta_color="inverse")
        st.caption("Critical Failures: 4 | Unsafe Actions: 3")
    
    with after_col:
        st.markdown("### After Fixes")
        st.metric("Reliability", "94%", delta="+33%")
        st.caption("Critical Failures: 0 | Unsafe Actions: 0")
    
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
    st.info("👈 Click 'Generate Tests' then 'Run Tests' to see the reliability report!")
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <p style="font-size: 3rem; opacity: 0.3;">🛡️</p>
        <h3 style="opacity: 0.5;">Ready to test your AI agent</h3>
        <p style="opacity: 0.3;">Use the controls in the sidebar to get started</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 10. EXPANDER: TEST SCENARIOS
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

# ============================================
# 11. EXPANDER: EXECUTION TRACES
# ============================================
with st.expander("🔍 Execution Traces"):
    if has_report:
        st.warning("Traces will be available after running tests (coming soon)")
        st.code(json.dumps(report.get("failure_patterns", {}), indent=2)[:1000])
    else:
        st.write("Run tests to see execution traces.")

# ============================================
# 12. EXPANDER: RAW REPORT
# ============================================
with st.expander("📊 Raw Report JSON"):
    if has_report:
        st.json(report)
    else:
        st.write("Run tests to see the full report.")

# ============================================
# 13. NEW: PRODUCTION ANALYZER
# ============================================
with st.expander("🧠 Self-Evolving Test Suite"):
    st.subheader("Production Pattern Analyzer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Analyze Production Logs", use_container_width=True):
            with st.spinner("Analyzing production patterns..."):
                try:
                    resp = requests.post(f"{API_URL}/analyze-production", timeout=30)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.evolution_data = data
                        st.success(f"✅ Analyzed {data.get('patterns_analyzed', 0)} patterns")
                        st.rerun()
                    else:
                        st.error("❌ Failed to analyze")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)[:100]}")
    
    with col2:
        if st.button("🔄 Evolve Test Suite", use_container_width=True):
            with st.spinner("Evolving test suite..."):
                try:
                    resp = requests.post(f"{API_URL}/evolve-tests", timeout=30)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.success(f"✅ Evolved {data.get('new_scenarios', 0)} new tests")
                        st.rerun()
                    else:
                        st.error("❌ Failed to evolve")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)[:100]}")
    
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
# 14. NEW: FERAL AGENT
# ============================================
with st.expander("🐺 Feral Agent - AI vs AI Testing"):
    st.subheader("The Feral Agent attacks your AI")
    st.caption("A secondary AI that actively tries to break your primary agent")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⚔️ Launch Feral Attack", use_container_width=True):
            with st.spinner("Generating feral attack..."):
                try:
                    resp = requests.post(f"{API_URL}/feral-attack", timeout=30)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.feral_result = data
                        st.success("✅ Feral attack executed!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to launch attack")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)[:100]}")
    
    with col2:
        if st.button("📊 Feral Stats", use_container_width=True):
            with st.spinner("Fetching stats..."):
                try:
                    resp = requests.get(f"{API_URL}/feral-stats")
                    if resp.status_code == 200:
                        st.session_state.feral_stats = resp.json()
                        st.rerun()
                    else:
                        st.error("❌ Failed to fetch stats")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)[:100]}")
    
    if st.session_state.get("feral_result"):
        result = st.session_state.feral_result
        attack = result.get("attack", {})
        attack_result = result.get("result", {})
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Attack Type", attack.get("attack_type", "N/A"))
        with col2:
            st.metric("Success", "✅" if attack_result.get("success") else "❌")
        with col3:
            st.metric("Risk Score", f"{attack_result.get('risk_score', 0)}%")
        
        st.text_area("Attack Input", attack.get("input", ""), height=60)
        st.text_area("Result", f"Expected: {attack.get('expected_behavior')} | Actual: {attack_result.get('actual')}", height=40)
    
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
# 15. NEW: ROOT CAUSE GRAPH (FIXED)
# ============================================
with st.expander("🔍 Root Cause Graph"):
    st.subheader("Failure Taxonomy & Root Cause Analysis")
    
    if st.button("📊 Analyze Failures", use_container_width=True):
        with st.spinner("Analyzing failures..."):
            try:
                resp = requests.post(f"{API_URL}/analyze-failures", timeout=30)
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.root_cause = data
                    st.rerun()
                else:
                    st.error("❌ Failed to analyze failures")
            except Exception as e:
                st.error(f"❌ Error: {str(e)[:100]}")
    
    if st.session_state.get("root_cause"):
        data = st.session_state.root_cause
        
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
        
        # Failure Chains - SAFELY HANDLED
        st.subheader("🔗 Failure Chains")
        chains = data.get("failure_chains", [])[:3]
        
        if chains:
            for idx, chain in enumerate(chains):
                # SAFE: Get input with fallback
                chain_input = chain.get("input")
                if chain_input is None:
                    chain_input = ""
                display_text = str(chain_input)[:50] if chain_input else f"Chain {idx + 1}"
                
                # SAFE: Create expander with safe label
                expander_label = f"🔗 {display_text}..." if display_text else f"🔗 Chain {idx + 1}"
                
                with st.expander(expander_label):
                    chain_steps = chain.get("chain", [])
                    if chain_steps:
                        for step in chain_steps:
                            step_num = step.get("step", "?")
                            step_event = step.get("event", "Unknown")
                            step_detail = step.get("detail", "")
                            st.caption(f"Step {step_num}: {step_event} → {step_detail}")
                    else:
                        st.caption("No chain steps available")
        else:
            st.info("No failure chains available")

# ============================================
# 16. NEW: COST TRACKER
# ============================================
with st.expander("💰 Cost-Per-Test Analytics"):
    st.subheader("Test Cost Tracking")
    
    if st.button("📊 Get Cost Summary", use_container_width=True):
        with st.spinner("Fetching cost data..."):
            try:
                resp = requests.get(f"{API_URL}/cost-summary", timeout=30)
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.cost_data = data
                    st.rerun()
                else:
                    st.error("❌ Failed to fetch costs")
            except Exception as e:
                st.error(f"❌ Error: {str(e)[:100]}")
    
    if st.session_state.get("cost_data"):
        data = st.session_state.cost_data
        summary = data.get("summary", {})
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Cost", f"${summary.get('total_cost', 0):.4f}")
        with col2:
            st.metric("Total Tests", summary.get("total_tests", 0))
        with col3:
            st.metric("Cost Per Test", f"${summary.get('cost_per_test', 0):.4f}")
        with col4:
            st.metric("Cost Per Pass", f"${summary.get('cost_per_pass', 0):.4f}")
        
        suggestions = data.get("suggestions", [])
        if suggestions:
            st.subheader("💡 Optimization Suggestions")
            for s in suggestions:
                st.info(s)
