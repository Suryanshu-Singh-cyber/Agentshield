# frontend/app.py
# AGENTSHIELD FRONTEND - COMPLETE VERSION WITH ALL FEATURES
# Version: 3.0.0

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
    .stSuccess { background: rgba(0, 210, 255, 0.1) !important; border-radius: 10px !important; }
    .stWarning { background: rgba(255, 165, 0, 0.1) !important; border-radius: 10px !important; }
    .stError { background: rgba(255, 0, 0, 0.1) !important; border-radius: 10px !important; }
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
if "datasets" not in st.session_state:
    st.session_state.datasets = None
if "dataset_tests" not in st.session_state:
    st.session_state.dataset_tests = None
if "eval_stats" not in st.session_state:
    st.session_state.eval_stats = None
if "canary_report" not in st.session_state:
    st.session_state.canary_report = None
if "fix_history" not in st.session_state:
    st.session_state.fix_history = None

# ============================================
# 6. API FUNCTIONS
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
    except:
        st.session_state.api_connected = False
        st.session_state.last_error = "Connection failed"
        return False

def api_request(method, endpoint, **kwargs):
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
            return None, f"HTTP {resp.status_code}"
    except Exception as e:
        return None, str(e)[:80]

# ============================================
# 7. HEADER
# ============================================
st.markdown("""
<div style="text-align: center; padding: 1rem 0 0.5rem 0;">
    <h1 style="font-size: 3.5rem; margin: 0;">🛡️ AgentShield</h1>
    <p style="font-size: 1.1rem; opacity: 0.7;">AI Agent Reliability Engineering Platform</p>
    <div style="background: linear-gradient(90deg, #00d2ff, #3a7bd5); height: 3px; width: 80px; margin: 0.5rem auto; border-radius: 2px;"></div>
</div>
""", unsafe_allow_html=True)

# ============================================
# 8. SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("### ⚙️ Control Panel")
    st.caption(f"🔗 {API_URL}")
    
    if st.button("🔌 Test Connection", use_container_width=True):
        test_api_connection()
        st.rerun()
    
    if st.session_state.api_connected is None:
        st.info("⏳ Click 'Test Connection'")
    elif st.session_state.api_connected:
        st.success("✅ Connected")
    else:
        st.error(f"❌ {st.session_state.last_error}")
    
    st.divider()
    
    if st.button("🔄 Generate Tests", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
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
    
    if st.button("🚀 Run Tests", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        elif not st.session_state.tests_generated:
            st.warning("Generate tests first!")
        else:
            with st.spinner("Running..."):
                data, error = api_request("post", "/run-tests", timeout=90)
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.session_state.report = data.get("report", {})
                    st.success(f"✅ {data['passed']} passed")
                    st.rerun()
    
    if st.button("⚡ Chaos Mode", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            new_state = not st.session_state.get("chaos_enabled", False)
            data, error = api_request("post", f"/chaos-mode?enable={str(new_state).lower()}", timeout=10)
            if not error:
                st.session_state.chaos_enabled = new_state
                st.success("✅ Toggled")
                st.rerun()
    
    if st.session_state.get("chaos_enabled"):
        st.markdown("🟢 **Chaos: ON**")
    else:
        st.markdown("⚪ **Chaos: OFF**")
    
    st.divider()
    
    if st.session_state.tests_generated:
        st.caption(f"📋 {len(st.session_state.scenarios)} scenarios")
    st.caption("v3.0.0 | OOSC 4.0")

# ============================================
# 9. METRICS
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
        st.metric("Risky", report.get("allowed_risky", 0))
    
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
    
    st.subheader("💡 Fixes")
    recs = report.get("recommendations", [])
    if recs:
        for rec in recs:
            st.info(rec)
    else:
        st.success("✅ All good!")
    
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
                data, error = api_request("post", "/apply-fix", json={"recommendations": recs}, timeout=90)
                if not error:
                    st.session_state.report = data.get("report", {})
                    st.success(f"✅ New: {data.get('new_reliability', 0)}%")
                    st.rerun()
else:
    st.info("👈 Generate and run tests to see results!")

# ============================================
# 11. TEST SCENARIOS
# ============================================
with st.expander("📋 Test Scenarios"):
    scenarios = st.session_state.get("scenarios", [])
    if scenarios:
        df = pd.DataFrame(scenarios)
        cols = ["id", "attack_type", "input", "expected_behavior", "severity"]
        available = [c for c in cols if c in df.columns]
        st.dataframe(df[available], use_container_width=True, height=250)
    else:
        st.write("No scenarios yet")

# ============================================
# 12. FERAL AGENT
# ============================================
with st.expander("🐺 Feral Agent"):
    st.subheader("AI vs AI Testing")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚔️ Launch Attack"):
            if not st.session_state.api_connected:
                st.warning("Connect first!")
            else:
                with st.spinner("Attacking..."):
                    data, error = api_request("post", "/feral-attack", timeout=30)
                    if error:
                        st.error(f"❌ {error}")
                    else:
                        st.session_state.feral_result = data
                        st.success("✅ Done!")
                        st.rerun()
    
    with col2:
        if st.button("📊 Stats"):
            if not st.session_state.api_connected:
                st.warning("Connect first!")
            else:
                data, error = api_request("get", "/feral-stats", timeout=10)
                if not error:
                    st.session_state.feral_stats = data
                    st.rerun()
    
    if st.session_state.get("feral_result"):
        result = st.session_state.feral_result
        attack = result.get("attack", {})
        r = result.get("result", {})
        c1, c2, c3 = st.columns(3)
        c1.metric("Type", attack.get("attack_type", "N/A"))
        c2.metric("Success", "✅" if r.get("success") else "❌")
        c3.metric("Risk", f"{r.get('risk_score', 0)}%")
        st.text_area("Input", attack.get("input", ""), height=50)
    
    if st.session_state.get("feral_stats"):
        stats = st.session_state.feral_stats
        c1, c2, c3 = st.columns(3)
        c1.metric("Total", stats.get("total_attacks", 0))
        c2.metric("Success Rate", f"{stats.get('success_rate', 0)}%")
        c3.metric("Mutations", stats.get("total_mutations", 0))

# ============================================
# 13. SELF-EVOLVING TESTS
# ============================================
with st.expander("🧠 Self-Evolving Tests"):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Analyze Production"):
            if not st.session_state.api_connected:
                st.warning("Connect first!")
            else:
                data, error = api_request("post", "/analyze-production", timeout=30)
                if not error:
                    st.session_state.evolution_data = data
                    st.success(f"✅ {data.get('patterns_analyzed', 0)} patterns")
                    st.rerun()
    
    with col2:
        if st.button("🔄 Evolve Tests"):
            if not st.session_state.api_connected:
                st.warning("Connect first!")
            else:
                data, error = api_request("post", "/evolve-tests", timeout=30)
                if not error:
                    st.success(f"✅ {data.get('new_scenarios', 0)} new tests")
                    st.rerun()
    
    if st.session_state.get("evolution_data"):
        d = st.session_state.evolution_data.get("summary", {})
        c1, c2, c3 = st.columns(3)
        c1.metric("Patterns", d.get("total_patterns", 0))
        c2.metric("Evolved", d.get("total_evolved_tests", 0))
        c3.metric("Last", d.get("last_analysis", "Never")[:10])
    
    # Self-Evolve button
    if st.button("🔄 Self-Evolve from Failures", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            with st.spinner("Self-evolving..."):
                data, error = api_request("post", "/self-evolve", timeout=30)
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.success(f"✅ {data.get('new_tests', 0)} new tests evolved")
                    st.rerun()

# ============================================
# 14. ROOT CAUSE
# ============================================
with st.expander("🔍 Root Cause"):
    st.subheader("Failure Analysis")
    
    if st.button("📊 Analyze Failures"):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        elif not st.session_state.report:
            st.warning("Run tests first!")
        else:
            data, error = api_request("post", "/analyze-failures", timeout=30)
            if not error:
                st.session_state.root_cause_data = data
                st.rerun()
    
    if st.session_state.get("root_cause_data"):
        data = st.session_state.root_cause_data
        
        taxonomy = data.get("taxonomy_breakdown", {})
        if taxonomy:
            st.subheader("Taxonomy")
            cols = st.columns(min(len(taxonomy), 4))
            for idx, (cat, info) in enumerate(taxonomy.items()):
                with cols[idx % 4]:
                    st.metric(cat.replace("_", " ").title(), info.get("count", 0))
        
        critical = data.get("critical_failures", [])
        if critical:
            st.subheader("🔥 Critical")
            for f in critical[:2]:
                st.warning(f.get("root_cause", "Unknown"))
        
        st.subheader("🔗 Failure Chains")
        chains = data.get("failure_chains", [])[:3]
        if chains:
            for idx, chain in enumerate(chains):
                chain_input = chain.get("input") or ""
                display_text = str(chain_input)[:40] + "..." if len(str(chain_input)) > 40 else str(chain_input) or f"Chain {idx+1}"
                st.markdown(f"**🔗 Chain {idx+1}:** {display_text}")
                for step in chain.get("chain", []):
                    st.caption(f"  Step {step.get('step')}: {step.get('event')} → {step.get('detail')}")
                st.divider()
        else:
            st.info("No failure chains available")

# ============================================
# 15. COST TRACKER (USD + INR)
# ============================================
with st.expander("💰 Cost Analytics"):
    st.subheader("Test Cost Tracking")
    USD_TO_INR = 83.5
    
    if st.button("📊 Refresh Cost Summary"):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            with st.spinner("Fetching..."):
                data, error = api_request("get", "/cost-summary", timeout=30)
                if not error:
                    st.session_state.cost_data = data
                    st.success("✅ Updated!")
                    st.rerun()
    
    if st.session_state.get("cost_data"):
        data = st.session_state.cost_data
        summary = data.get("summary", {})
        
        total_usd = summary.get("total_cost", 0)
        per_test_usd = summary.get("cost_per_test", 0)
        per_pass_usd = summary.get("cost_per_pass", 0)
        per_fail_usd = summary.get("cost_per_failure", 0)
        
        total_inr = total_usd * USD_TO_INR
        per_test_inr = per_test_usd * USD_TO_INR
        per_pass_inr = per_pass_usd * USD_TO_INR
        per_fail_inr = per_fail_usd * USD_TO_INR
        
        st.subheader("💵 Cost Summary")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🇺🇸 USD**")
            st.metric("Total", f"${total_usd:.4f}")
            st.metric("Per Test", f"${per_test_usd:.4f}")
            st.metric("Per Pass", f"${per_pass_usd:.4f}")
            st.metric("Per Failure", f"${per_fail_usd:.4f}")
        
        with col2:
            st.markdown("**🇮🇳 INR**")
            st.metric("Total", f"₹{total_inr:.2f}")
            st.metric("Per Test", f"₹{per_test_inr:.2f}")
            st.metric("Per Pass", f"₹{per_pass_inr:.2f}")
            st.metric("Per Failure", f"₹{per_fail_inr:.2f}")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Tests", summary.get("total_tests", 0))
        c2.metric("API Calls", summary.get("total_api_calls", 0))
        c3.metric("Tokens", f"{summary.get('total_tokens', 0):,}")
        
        # Cost-to-Fix
        if st.button("📊 Cost-to-Fix"):
            data, error = api_request("get", "/cost-to-fix", timeout=30)
            if not error:
                st.json(data)
    
    else:
        st.info("Click 'Refresh Cost Summary' to see cost data.")

# ============================================
# 16. PER-TURN EVALUATION (NEW)
# ============================================
with st.expander("⚡ Per-Turn Evaluation"):
    st.subheader("Real-time Agent Behavior Analysis")
    st.caption("Lightweight evaluation on every agent step")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Get Evaluation Stats"):
            if not st.session_state.api_connected:
                st.warning("Connect first!")
            else:
                data, error = api_request("get", "/evaluate-stats", timeout=10)
                if not error:
                    st.session_state.eval_stats = data
                    st.rerun()
    
    if st.session_state.get("eval_stats"):
        stats = st.session_state.eval_stats
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Turns", stats.get("total_turns_evaluated", 0))
        c2.metric("Safety Rate", f"{stats.get('safety_rate', 0)}%")
        c3.metric("Avg Confidence", stats.get("avg_confidence", 0))
        
        if stats.get("flag_breakdown"):
            st.subheader("Flag Breakdown")
            for flag, count in stats.get("flag_breakdown", {}).items():
                st.caption(f"  {flag}: {count}")
    
    st.subheader("Evaluate a Turn")
    user_input = st.text_input("User Input:", "Delete my account")
    agent_thought = st.text_input("Agent Thought:", "User wants account deletion")
    
    if st.button("🔍 Evaluate Turn"):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            with st.spinner("Evaluating..."):
                data, error = api_request("post", "/evaluate-turn", 
                                          json={"user_input": user_input, "agent_thought": agent_thought, "tool_calls": []}, 
                                          timeout=10)
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.json(data)

# ============================================
# 17. CANARY TESTING (NEW)
# ============================================
# ============================================
# 17. CANARY TESTING (FIXED)
# ============================================
with st.expander("🦜 Canary Testing"):
    st.subheader("Data Exfiltration Detection")
    st.caption("Detect when agent tries to leak sensitive data")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Canary Report"):
            if not st.session_state.api_connected:
                st.warning("Connect first!")
            else:
                data, error = api_request("get", "/canary-report", timeout=10)
                if not error:
                    st.session_state.canary_report = data
                    st.rerun()
    
    if st.session_state.get("canary_report"):
        report = st.session_state.canary_report
        c1, c2 = st.columns(2)
        c1.metric("Total Canaries", report.get("total_canaries", 0))
        c2.metric("Exfiltrated", report.get("exfiltrated", 0))
    
    st.subheader("Create Canary")
    test_id = st.text_input("Test ID:", "canary_test_001")
    data_type = st.selectbox("Data Type:", ["customer", "order", "api_key"])
    
    if st.button("🦜 Create Canary"):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            with st.spinner("Creating canary..."):
                # FIX: Send JSON body instead of query parameters
                data, error = api_request("post", "/create-canary", 
                                          json={"test_id": test_id, "data_type": data_type},
                                          timeout=10)
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.success("✅ Canary created!")
                    st.json(data)
    
    # Check Exfiltration (New)
    st.subheader("Check Response for Exfiltration")
    response_json = st.text_area("Response JSON:", '{"user_id": "canary_123", "email": "test@example.com"}')
    check_test_id = st.text_input("Test ID (optional):", "")
    
    if st.button("🔍 Check Exfiltration"):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            with st.spinner("Checking..."):
                try:
                    response_data = json.loads(response_json)
                    payload = {"response": response_data}
                    if check_test_id:
                        payload["test_id"] = check_test_id
                    
                    data, error = api_request("post", "/check-exfiltration", 
                                              json=payload,
                                              timeout=10)
                    if error:
                        st.error(f"❌ {error}")
                    else:
                        if data.get("exfiltrated"):
                            st.error("🚨 Data exfiltration detected!")
                        else:
                            st.success("✅ No exfiltration detected")
                        st.json(data)
                except json.JSONDecodeError:
                    st.error("❌ Invalid JSON format")

# ============================================
# 18. FIX → PR GENERATION (NEW)
# ============================================
with st.expander("🔧 Fix → PR Generation"):
    st.subheader("Automated Code Fix Generation")
    st.caption("Generate and apply fixes for failures")
    
    if st.button("📊 Fix History"):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            data, error = api_request("get", "/fix-history", timeout=10)
            if not error:
                st.session_state.fix_history = data
                st.rerun()
    
    if st.session_state.get("fix_history"):
        history = st.session_state.fix_history
        c1, c2 = st.columns(2)
        c1.metric("Total Fixes", history.get("total_fixes", 0))
        c2.metric("Applied", history.get("applied_fixes", 0))
    
    st.subheader("Generate Fix for Failure")
    failure_input = st.text_area("Failure Description:", "delete_account was called without confirmation")
    failure_type = st.selectbox("Failure Type:", ["destructive_action", "authority_override", "confirmation_missing", "tool_misuse"])
    
    if st.button("🔧 Generate Fix"):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            with st.spinner("Generating fix..."):
                data, error = api_request("post", "/generate-fix", 
                                          json={"failure": {"input": failure_input, "attack_type": failure_type, "id": "fix_test"}},
                                          timeout=30)
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.success("✅ Fix generated!")
                    st.code(data.get("code", "# Fix code here"), language="python")
                    st.caption(f"File: {data.get('file', 'agent.py')} | Description: {data.get('description', '')}")

# ============================================
# 19. DATASET LOADER (NEW)
# ============================================
# ============================================
# 19. DATASET LOADER (FIXED)
# ============================================
with st.expander("📚 Dataset Loader"):
    st.subheader("Evaluation Datasets")
    st.caption("Built-in datasets: OWASP, MITRE, Prompt Injections, Destructive Actions, Benign, Edge Cases")
    
    # List datasets
    if st.button("📊 List Datasets"):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            data, error = api_request("get", "/datasets", timeout=10)
            if not error:
                st.session_state.datasets = data
                st.rerun()
    
    if st.session_state.get("datasets"):
        datasets_data = st.session_state.datasets
        datasets = datasets_data.get("datasets", [])
        
        if datasets:
            df_datasets = pd.DataFrame(datasets)
            st.dataframe(df_datasets, use_container_width=True)
        
        summary = datasets_data.get("summary", {})
        if summary:
            c1, c2 = st.columns(2)
            c1.metric("Total Datasets", summary.get("total_datasets", 0))
            c2.metric("Total Items", summary.get("total_items", 0))
    
    st.subheader("Load Dataset")
    dataset_name = st.text_input("Dataset Name:", "owasp_top_10")
    limit = st.number_input("Limit:", min_value=1, max_value=50, value=10)
    filter_type = st.text_input("Filter by Attack Type (optional):", "")
    
    if st.button("📖 Load Dataset"):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            params = f"/dataset/{dataset_name}?limit={limit}"
            if filter_type:
                params += f"&filter_type={filter_type}"
            data, error = api_request("get", params, timeout=10)
            if error:
                st.error(f"❌ {error}")
            else:
                st.session_state.dataset_tests = data
                st.rerun()
    
    if st.session_state.get("dataset_tests"):
        data = st.session_state.dataset_tests
        st.subheader(f"Dataset: {data.get('dataset', 'Unknown')}")
        st.metric("Items", data.get("count", 0))
        tests = data.get("tests", [])
        if tests:
            df_tests = pd.DataFrame(tests)
            st.dataframe(df_tests, use_container_width=True)
        
        stats = data.get("stats", {})
        if stats:
            st.subheader("Statistics")
            for key, value in stats.items():
                if key not in ["name", "description", "category", "version", "created_at", "tags"]:
                    if isinstance(value, dict):
                        st.caption(f"  {key}: {value}")
    
    st.subheader("Generate Synthetic Dataset")
    gen_name = st.text_input("Dataset Name (for generation):", "my_synthetic_dataset")
    gen_size = st.number_input("Size:", min_value=5, max_value=100, value=20)
    gen_type = st.selectbox("Type:", ["synthetic", "owasp", "mitre", "production"])
    
    if st.button("🔄 Generate Dataset"):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            with st.spinner("Generating..."):
                # FIX: Send JSON body
                data, error = api_request("post", "/dataset/generate", 
                                          json={
                                              "name": gen_name,
                                              "size": gen_size,
                                              "dataset_type": gen_type,
                                              "seed": 42
                                          },
                                          timeout=30)
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.success(f"✅ Generated {data.get('size', 0)} items")
                    st.json(data)
    
    st.subheader("Random Tests")
    random_count = st.number_input("Random Count:", min_value=1, max_value=20, value=5)
    if st.button("🎲 Get Random Tests"):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            data, error = api_request("get", f"/dataset/random?count={random_count}", timeout=10)
            if not error:
                st.json(data)
    
    st.subheader("Compare Datasets")
    compare_name1 = st.text_input("Dataset 1:", "owasp_top_10")
    compare_name2 = st.text_input("Dataset 2:", "mitre_attacks")
    
    if st.button("📊 Compare Datasets"):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            data, error = api_request("get", f"/dataset/compare?name1={compare_name1}&name2={compare_name2}", timeout=10)
            if error:
                st.error(f"❌ {error}")
            else:
                st.json(data)
# ============================================
# 20. RAW REPORT
# ============================================
with st.expander("📊 Raw Report"):
    if has_report:
        st.json(report)
    else:
        st.write("Run tests to see report")

# ============================================
# 21. FOOTER
# ============================================
st.divider()
st.caption("🛡️ AgentShield v3.0.0 | OOSC 4.0 | IIIT Allahabad")
st.caption(f"🔗 {API_URL}")
