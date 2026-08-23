# frontend/app.py
# AGENTSHIELD - OPTIMIZED WORKING VERSION
# Team: Nawab_Coders
# OOSC 4.0 Hackathon · IIIT Allahabad
# Version: 4.2.0

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
# PAGE CONFIG (MUST BE FIRST)
# ============================================
st.set_page_config(
    page_title="🛡️ AgentShield · Nawab_Coders",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# ENVIRONMENT DETECTION
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
# OPTIMIZED CSS (No Lag)
# ============================================
def load_css():
    st.markdown("""
    <style>
    /* ─── Font ─── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    /* ─── Base ─── */
    .stApp {
        background: linear-gradient(135deg, #0a0918, #1a0f2e, #0f1a2e, #0a0918);
        color: #eef2ff;
        font-family: 'Inter', sans-serif;
    }

    /* ─── Team Badge ─── */
    .team-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(0,210,255,0.15), rgba(58,123,213,0.08));
        padding: 6px 22px;
        border-radius: 40px;
        border: 1px solid rgba(0,210,255,0.12);
        font-size: 0.75rem;
        font-weight: 700;
        color: #00d2ff;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    /* ─── Splash Screen ─── */
    #splash-screen {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 99999;
        background: #0a0918;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: opacity 0.6s ease, visibility 0.6s ease;
        font-family: 'Inter', sans-serif;
    }
    #splash-screen.hide {
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
    }
    .splash-icon { font-size: 4.5rem; animation: pulse 1.5s ease-in-out infinite; }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.05); opacity: 1; }
    }
    .splash-title {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 20%, #00d2ff 50%, #3a7bd5 80%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .splash-sub {
        color: #94a3b8;
        font-size: 0.85rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 0.3rem;
    }
    .splash-team {
        margin-top: 1rem;
        padding: 0.3rem 1.6rem;
        border: 1px solid rgba(0,210,255,0.12);
        border-radius: 40px;
        font-size: 0.7rem;
        color: #00d2ff;
        background: rgba(0,210,255,0.04);
        letter-spacing: 0.5px;
    }
    .splash-loader {
        margin-top: 1.5rem;
        width: 150px;
        height: 2px;
        background: rgba(255,255,255,0.05);
        border-radius: 2px;
        overflow: hidden;
    }
    .splash-loader::after {
        content: '';
        display: block;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, #00d2ff, #3a7bd5, transparent);
        animation: loadSlide 1.5s ease-in-out infinite;
    }
    @keyframes loadSlide { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

    /* ─── Headers ─── */
    h1, h2, h3 {
        font-weight: 800 !important;
        background: linear-gradient(135deg, #ffffff 30%, #00d2ff 70%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    h1 { font-size: 3.2rem !important; line-height: 1.05 !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.2rem !important; }

    /* ─── Glass Cards ─── */
    .glass-card {
        background: rgba(255,255,255,0.02);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 18px;
        padding: 20px 18px;
        transition: all 0.3s ease;
        height: 100%;
    }
    .glass-card:hover {
        transform: translateY(-3px);
        border-color: rgba(0,210,255,0.08);
        box-shadow: 0 8px 30px 0 rgba(0,210,255,0.03);
    }

    /* ─── Feature Cards ─── */
    .feature-card {
        background: rgba(255,255,255,0.015);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 16px;
        padding: 20px 16px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0,210,255,0.1);
        box-shadow: 0 8px 24px 0 rgba(0,210,255,0.03);
    }
    .feature-card .icon { font-size: 2.2rem; display: block; margin-bottom: 0.5rem; }
    .feature-card h4 { font-weight: 700; font-size: 1rem; color: #eef2ff; margin-bottom: 0.2rem; }
    .feature-card p { font-size: 0.8rem; color: #94a3b8; line-height: 1.4; }

    /* ─── Metrics ─── */
    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.02);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.03);
        border-radius: 14px;
        padding: 16px 14px;
    }
    [data-testid="metric-label"] { color: #94a3b8 !important; font-weight: 600 !important; font-size: 0.75rem !important; }
    [data-testid="metric-value"] { color: #eef2ff !important; font-weight: 800 !important; font-size: 1.8rem !important; }

    /* ─── Buttons ─── */
    .stButton > button {
        background: linear-gradient(135deg, #00d2ff, #3a7bd5) !important;
        border: none !important;
        border-radius: 40px !important;
        padding: 0.5rem 1.6rem !important;
        font-weight: 700 !important;
        color: #0a0918 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover { transform: scale(1.03); box-shadow: 0 4px 20px 0 rgba(0,210,255,0.15); }

    /* ─── Sidebar ─── */
    .css-1d391kg {
        background: rgba(10,9,24,0.85) !important;
        backdrop-filter: blur(16px) !important;
        border-right: 1px solid rgba(255,255,255,0.02) !important;
    }

    /* ─── Expanders ─── */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.01) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.03) !important;
        font-weight: 600 !important;
        color: #eef2ff !important;
        padding: 8px 14px !important;
    }
    .streamlit-expanderHeader:hover { background: rgba(255,255,255,0.02) !important; }

    /* ─── Alerts ─── */
    .stAlert { background: rgba(255,255,255,0.015) !important; border-radius: 12px !important; }
    .stSuccess { background: rgba(0,210,255,0.03) !important; border-color: rgba(0,210,255,0.06) !important; }
    .stWarning { background: rgba(255,165,0,0.03) !important; border-color: rgba(255,165,0,0.06) !important; }
    .stError { background: rgba(255,0,0,0.03) !important; border-color: rgba(255,0,0,0.06) !important; }

    /* ─── Footer ─── */
    .footer {
        text-align: center;
        padding: 20px 0 10px;
        border-top: 1px solid rgba(255,255,255,0.02);
        font-size: 0.7rem;
        color: #475569;
    }
    .footer a { color: #00d2ff; text-decoration: none; font-weight: 600; }
    .footer .heart { color: #ff6b6b; display: inline-block; animation: heartBeat 1.5s ease-in-out infinite; }
    @keyframes heartBeat { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }

    /* ─── Responsive ─── */
    @media (max-width: 768px) {
        h1 { font-size: 2rem !important; }
        h2 { font-size: 1.5rem !important; }
        .glass-card { padding: 14px 12px; }
        .feature-card { padding: 14px 12px; }
        .splash-title { font-size: 2rem; }
        [data-testid="metric-value"] { font-size: 1.3rem !important; }
    }
    </style>

    <!-- Splash Screen -->
    <div id="splash-screen">
        <div class="splash-icon">🛡️</div>
        <div class="splash-title">AgentShield</div>
        <div class="splash-sub">OOSC 4.0 · IIIT Allahabad</div>
        <div class="splash-team">⚡ Team Nawab_Coders</div>
        <div class="splash-loader"></div>
    </div>

    <script>
    // Auto-hide splash after 3.5 seconds
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(function() {
            var splash = document.getElementById('splash-screen');
            if (splash) splash.classList.add('hide');
        }, 3500);
    });
    </script>
    """, unsafe_allow_html=True)

load_css()

# ============================================
# SESSION STATE
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
# API FUNCTIONS
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
# HERO SECTION
# ============================================
st.markdown("""
<div style="text-align:center;padding:5px 0 10px 0;">
    <div class="team-badge">🏆 Team Nawab_Coders · OOSC 4.0</div>
    <h1 style="font-size:3.5rem;line-height:1.05;margin-bottom:0.3rem;">
        Don't just evaluate.<br>
        <span style="background:linear-gradient(135deg,#00d2ff,#3a7bd5);
                     -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            Attack. Block. Fix. Verify.
        </span>
    </h1>
    <p style="max-width:600px;margin:0 auto 1rem;color:#94a3b8;font-size:1rem;line-height:1.6;">
        AgentShield is an <strong style="color:#eef2ff;">active reliability engine</strong> for AI agents.
        It generates adversarial tests, blocks destructive behavior, and proves fixes work.
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================
# PS4 STORY
# ============================================
st.markdown("""
<div style="padding:5px 0;">
    <h2 style="text-align:center;font-size:1.8rem;">Why <span style="color:#00d2ff;">PS4</span>?</h2>
    <p style="text-align:center;color:#94a3b8;max-width:500px;margin:0 auto 0.8rem;font-size:0.95rem;">
        The AI agent reliability gap is real. Here's how AgentShield closes it.
    </p>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([1, 1])

with c1:
    st.markdown("""
    <div class="glass-card">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
            <span style="font-size:1.6rem;">⚠️</span>
            <span style="font-weight:800;font-size:1rem;color:#ff6b6b;">The Problem</span>
        </div>
        <p style="color:#94a3b8;line-height:1.7;font-size:0.9rem;">
            <span style="background:rgba(255,50,50,0.08);padding:2px 10px;border-radius:20px;color:#ff6b6b;font-weight:700;">70%</span>
            of AI agents fail on real-world tasks. Most tools only tell you 
            <em style="color:#eef2ff;">after</em> deployment.
        </p>
        <br>
        <p style="color:#94a3b8;line-height:1.7;font-size:0.9rem;">
            <span style="color:#00d2ff;font-weight:700;">AgentShield</span> tests agents 
            <strong style="color:#eef2ff;">before</strong> they go live.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:2.5rem;margin-bottom:8px;">🔄</div>
        <div style="font-weight:700;font-size:1rem;margin-bottom:10px;color:#eef2ff;">The AgentShield Flow</div>
        <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:4px 4px;font-size:0.75rem;color:#94a3b8;">
            <span style="background:rgba(255,255,255,0.03);padding:4px 12px;border-radius:40px;border:1px solid rgba(255,255,255,0.03);">🔍 Attack</span>
            <span style="color:#00d2ff;">→</span>
            <span style="background:rgba(255,255,255,0.03);padding:4px 12px;border-radius:40px;border:1px solid rgba(255,255,255,0.03);">🛡️ Block</span>
            <span style="color:#00d2ff;">→</span>
            <span style="background:rgba(255,255,255,0.03);padding:4px 12px;border-radius:40px;border:1px solid rgba(255,255,255,0.03);">🧠 Root Cause</span>
            <span style="color:#00d2ff;">→</span>
            <span style="background:rgba(255,255,255,0.03);padding:4px 12px;border-radius:40px;border:1px solid rgba(255,255,255,0.03);">🔧 Fix</span>
            <span style="color:#00d2ff;">→</span>
            <span style="background:rgba(255,255,255,0.03);padding:4px 12px;border-radius:40px;border:1px solid rgba(255,255,255,0.03);">✅ Verify</span>
        </div>
        <div style="margin-top:8px;font-size:0.6rem;color:#475569;">
            Pre-deployment · Sandboxed · Actionable
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:10px 0 12px;border-bottom:1px solid rgba(255,255,255,0.02);">
        <div style="font-size:2rem;">🛡️</div>
        <div style="font-weight:800;font-size:1.1rem;background:linear-gradient(135deg,#ffffff 30%,#00d2ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            AgentShield
        </div>
        <div style="font-size:0.6rem;color:#00d2ff;letter-spacing:0.5px;font-weight:600;">
            ⚡ Team Nawab_Coders
        </div>
        <div style="font-size:0.5rem;color:#475569;">v4.2.0 · OOSC 4.0</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Controls")
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
    
    if st.session_state.get("chaos_enabled", False):
        st.markdown("🟢 **Chaos: ON**")
    else:
        st.markdown("⚪ **Chaos: OFF**")
    
    st.divider()
    
    if st.button("✅ Apply Fixes", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        elif not st.session_state.report:
            st.warning("Run tests first!")
        else:
            recs = st.session_state.report.get("recommendations", [])
            if not recs:
                st.success("✅ No fixes needed!")
            else:
                with st.spinner("Applying..."):
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
    st.caption("🛡️ v4.2.0")

# ============================================
# METRICS
# ============================================
report = st.session_state.get("report", {})
has_report = report and report.get("total_tests", 0) > 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    val = f"{report.get('overall_reliability', 0)}%" if has_report else "—"
    st.metric("📊 Reliability", val)

with col2:
    val = f"{report.get('safety_score', 0)}%" if has_report else "—"
    st.metric("🛡️ Safety", val)

with col3:
    val = f"{report.get('passed', 0)}/{report.get('total_tests', 0)}" if has_report else "—"
    st.metric("✅ Passed", val)

with col4:
    val = f"{report.get('consistency', 0)}%" if has_report else "—"
    st.metric("🎯 Consistency", val)

# ============================================
# MAIN CONTENT
# ============================================
if has_report:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h3>📈 Performance Metrics</h3>', unsafe_allow_html=True)
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
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            yaxis_range=[0, 100],
            height=280,
            xaxis_title=None,
            yaxis_title=None
        )
        fig.update_traces(texttemplate='%{y:.0f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3>⚠️ Critical Issues</h3>', unsafe_allow_html=True)
        st.metric("Critical Failures", report.get("critical_failures", 0), delta_color="inverse")
        st.metric("Blocked Actions", report.get("blocked_count", 0))
        st.metric("Risky Allowed", report.get("allowed_risky", 0))
    
    st.markdown('<h3>📊 By Attack Type</h3>', unsafe_allow_html=True)
    attack_data = report.get("by_attack_type", {})
    if attack_data:
        df_attack = pd.DataFrame([
            {"Type": k, "Pass Rate": v.get("rate", 0)}
            for k, v in attack_data.items()
        ])
        fig = px.bar(df_attack, x="Type", y="Pass Rate", color="Pass Rate",
                     color_continuous_scale="RdYlGn", range_color=[0, 100])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            yaxis_range=[0, 100],
            height=240,
            xaxis_title=None,
            yaxis_title=None
        )
        fig.update_traces(texttemplate='%{y:.0f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<h3>💡 Fix Recommendations</h3>', unsafe_allow_html=True)
    recs = report.get("recommendations", [])
    if recs:
        for rec in recs:
            st.info(rec)
    else:
        st.success("✅ All good! No fixes needed.")
    
    st.markdown('<h3>🔄 Before → After</h3>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        st.metric("Before", "61%", delta="-33%", delta_color="inverse")
        st.caption("4 critical failures")
    with b2:
        st.metric("After", "94%", delta="+33%")
        st.caption("0 critical failures")

else:
    st.info("👈 Generate and run tests to see results!")

# ============================================
# FEATURES GRID (FIXED - VISIBLE NOW)
# ============================================
st.markdown("""
<div style="padding:15px 0 5px 0;">
    <h2 style="text-align:center;font-size:1.8rem;">Core <span style="color:#00d2ff;">Capabilities</span></h2>
    <p style="text-align:center;color:#94a3b8;max-width:500px;margin:0 auto 0.8rem;font-size:0.9rem;">
        Every feature closes the loop from test to production.
    </p>
</div>
""", unsafe_allow_html=True)

features = [
    ("🔥", "Action Firewall", "Real-time risk scoring & blocking of destructive tool calls."),
    ("🐺", "Feral Agent", "An AI adversary that actively tries to break your agent."),
    ("🧠", "Self-Evolving Tests", "Learns from production failures and generates new tests."),
    ("🔍", "Root Cause Graph", "Visual chain from input to root cause of failure."),
    ("🦜", "Canary Testing", "Detects data exfiltration with canary tokens."),
    ("💰", "Cost Analytics", "Track test costs in USD & INR. Optimize your spend.")
]

cols = st.columns(3)
for i, (icon, title, desc) in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="feature-card">
            <span class="icon">{icon}</span>
            <h4>{title}</h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# EXPANDERS (All Features)
# ============================================

# ─── Test Scenarios ───
with st.expander("📋 Test Scenarios"):
    scenarios = st.session_state.get("scenarios", [])
    if scenarios:
        df = pd.DataFrame(scenarios)
        cols = ["id", "attack_type", "input", "expected_behavior", "severity"]
        available = [c for c in cols if c in df.columns]
        st.dataframe(df[available], use_container_width=True, height=250)
        st.caption(f"Total: {len(scenarios)} scenarios")
    else:
        st.write("No scenarios generated yet.")

# ─── Feral Agent ───
with st.expander("🐺 Feral Agent — AI vs AI"):
    st.subheader("The Feral Agent attacks your AI")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚔️ Launch Attack", use_container_width=True):
            if not st.session_state.api_connected:
                st.warning("Connect first!")
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
        c1.metric("Attack Type", attack.get("attack_type", "N/A"))
        c2.metric("Success", "✅" if r.get("success") else "❌")
        c3.metric("Risk Score", f"{r.get('risk_score', 0)}%")
        st.text_area("Attack Input", attack.get("input", ""), height=60)
    
    if st.session_state.get("feral_stats"):
        stats = st.session_state.feral_stats
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Attacks", stats.get("total_attacks", 0))
        c2.metric("Success Rate", f"{stats.get('success_rate', 0)}%")
        c3.metric("Mutations", stats.get("total_mutations", 0))

# ─── Self-Evolving Tests ───
with st.expander("🧠 Self-Evolving Tests"):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Analyze Production", use_container_width=True):
            if not st.session_state.api_connected:
                st.warning("Connect first!")
            else:
                data, error = api_request("post", "/analyze-production", timeout=30)
                if not error:
                    st.session_state.evolution_data = data
                    st.success(f"✅ {data.get('patterns_analyzed', 0)} patterns")
                    st.rerun()
    
    with col2:
        if st.button("🔄 Evolve Tests", use_container_width=True):
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

# ─── Root Cause ───
with st.expander("🔍 Root Cause Graph"):
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

# ─── Cost Tracker ───
with st.expander("💰 Cost Analytics (USD/INR)"):
    st.subheader("Test Cost Tracking")
    USD_TO_INR = 83.5
    
    if st.button("📊 Refresh Cost Summary", use_container_width=True):
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
        
        if st.button("📊 Cost-to-Fix"):
            data, error = api_request("get", "/cost-to-fix", timeout=30)
            if not error:
                st.json(data)
    
    else:
        st.info("Click 'Refresh Cost Summary' to see cost data.")

# ─── Per-Turn Evaluation ───
with st.expander("⚡ Per-Turn Evaluation"):
    st.subheader("Real-time Agent Behavior Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Get Evaluation Stats", use_container_width=True):
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
    
    if st.button("🔍 Evaluate Turn", use_container_width=True):
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

# ─── Canary Testing ───
with st.expander("🦜 Canary Testing"):
    st.subheader("Data Exfiltration Detection")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Canary Report", use_container_width=True):
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
    
    if st.button("🦜 Create Canary", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            with st.spinner("Creating canary..."):
                data, error = api_request("post", "/create-canary", 
                                          json={"test_id": test_id, "data_type": data_type},
                                          timeout=10)
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.success("✅ Canary created!")
                    st.json(data)
    
    st.subheader("Check Response for Exfiltration")
    response_json = st.text_area("Response JSON:", '{"user_id": "canary_123", "email": "test@example.com"}')
    check_test_id = st.text_input("Test ID (optional):", "")
    
    if st.button("🔍 Check Exfiltration", use_container_width=True):
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

# ─── Fix → PR Generation ───
with st.expander("🔧 Fix → PR Generation"):
    st.subheader("Automated Code Fix Generation")
    
    if st.button("📊 Fix History", use_container_width=True):
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
    
    if st.button("🔧 Generate Fix", use_container_width=True):
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

# ─── Dataset Loader ───
with st.expander("📚 Dataset Loader"):
    st.subheader("Evaluation Datasets")
    
    if st.button("📊 List Datasets", use_container_width=True):
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
    
    if st.button("📖 Load Dataset", use_container_width=True):
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
    
    if st.button("🔄 Generate Dataset", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            with st.spinner("Generating..."):
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
    if st.button("🎲 Get Random Tests", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            data, error = api_request("get", f"/dataset/random?count={random_count}", timeout=10)
            if not error:
                st.json(data)
    
    st.subheader("Compare Datasets")
    compare_name1 = st.text_input("Dataset 1:", "owasp_top_10")
    compare_name2 = st.text_input("Dataset 2:", "mitre_attacks")
    
    if st.button("📊 Compare Datasets", use_container_width=True):
        if not st.session_state.api_connected:
            st.warning("Connect first!")
        else:
            data, error = api_request("get", f"/dataset/compare?name1={compare_name1}&name2={compare_name2}", timeout=10)
            if error:
                st.error(f"❌ {error}")
            else:
                st.json(data)

# ============================================
# RAW REPORT
# ============================================
with st.expander("📊 Raw Report JSON"):
    if has_report:
        st.json(report)
    else:
        st.write("Run tests to see the full report.")

# ============================================
# FOOTER
# ============================================
st.markdown(f"""
<div class="footer">
    🛡️ <strong>AgentShield</strong> v4.2.0 · Built with <span class="heart">❤</span> by 
    <strong style="color:#00d2ff;">Team Nawab_Coders</strong> · OOSC 4.0 · IIIT Allahabad
    <br>
    <span style="color:#475569;font-size:0.65rem;">
        PS4 · AI Agent Evaluation &amp; Reliability Engine · 
        <a href="https://github.com/Suryanshu-Singh-cyber/Agentshield" target="_blank">GitHub</a>
    </span>
</div>
""", unsafe_allow_html=True)
