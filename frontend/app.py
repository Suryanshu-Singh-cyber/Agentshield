# frontend/app.py
# AGENTSHIELD - COMPLETE ALL-IN-ONE STREAMLIT APP
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
# 4. COMPLETE CUSTOM CSS (Matches index.html)
# ============================================
def load_css():
    st.markdown("""
    <style>
    /* ─── Import Google Font ─── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,600;14..32,700;14..32,800&display=swap');

    /* ─── Global Styles ─── */
    .stApp {
        background: linear-gradient(135deg, #0b0a1a, #1a1a3e, #0b0a1a);
        color: #eef2ff;
        font-family: 'Inter', sans-serif;
    }

    /* ─── Glowing Cursor Effect ─── */
    .cursor-glow {
        position: fixed;
        width: 320px;
        height: 320px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(0, 210, 255, 0.06) 0%, transparent 70%);
        pointer-events: none;
        transform: translate(-50%, -50%);
        z-index: 0;
        transition: width 0.2s, height 0.2s;
    }

    /* ─── Headers with Gradient ─── */
    h1, h2, h3, .gradient-text {
        font-weight: 800 !important;
        background: linear-gradient(135deg, #ffffff 40%, #00d2ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Inter', sans-serif;
    }

    h1 {
        font-size: 3.5rem !important;
        line-height: 1.1 !important;
        margin-bottom: 0.5rem !important;
    }

    /* ─── Glass-morphism Cards ─── */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 24px;
        padding: 28px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        height: 100%;
    }

    .glass-card:hover {
        transform: translateY(-6px);
        border-color: rgba(0, 210, 255, 0.2);
        box-shadow: 0 12px 48px 0 rgba(0, 210, 255, 0.08);
    }

    /* ─── Feature Cards (3D Tilt Effect via hover) ─── */
    .feature-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 28px 22px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }

    .feature-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(0, 210, 255, 0.2);
        box-shadow: 0 12px 40px rgba(0, 210, 255, 0.08);
    }

    .feature-card .icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
        display: block;
    }

    .feature-card h4 {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.3rem;
        color: #eef2ff;
    }

    .feature-card p {
        font-size: 0.85rem;
        color: #94a3b8;
        line-height: 1.5;
    }

    /* ─── Badges ─── */
    .badge-primary {
        display: inline-block;
        background: rgba(0, 210, 255, 0.08);
        padding: 6px 20px;
        border-radius: 40px;
        font-size: 0.75rem;
        font-weight: 600;
        color: #00d2ff;
        border: 1px solid rgba(0, 210, 255, 0.12);
    }

    .stat-badge {
        display: inline-block;
        background: rgba(255, 50, 50, 0.08);
        padding: 4px 14px;
        border-radius: 40px;
        font-size: 0.75rem;
        font-weight: 700;
        color: #ff6b6b;
        border: 1px solid rgba(255, 50, 50, 0.12);
        margin-right: 6px;
    }

    /* ─── Metrics ─── */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        transition: all 0.3s ease;
    }

    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 210, 255, 0.15);
        box-shadow: 0 12px 40px 0 rgba(0, 210, 255, 0.05);
    }

    /* ─── Buttons ─── */
    .stButton > button {
        background: linear-gradient(135deg, #00d2ff, #3a7bd5) !important;
        border: none !important;
        border-radius: 40px !important;
        padding: 0.6rem 1.8rem !important;
        font-weight: 600 !important;
        color: #0b0a1a !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px 0 rgba(0, 210, 255, 0.15);
        font-family: 'Inter', sans-serif;
    }

    .stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 8px 30px 0 rgba(0, 210, 255, 0.25);
    }

    /* ─── Sidebar ─── */
    .css-1d391kg {
        background: rgba(15, 12, 41, 0.8) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.04);
    }

    /* ─── Expanders ─── */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(4px);
        font-weight: 600;
    }

    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.04) !important;
        border-color: rgba(0, 210, 255, 0.1);
    }

    /* ─── Dataframes ─── */
    .dataframe {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.04);
    }

    /* ─── Alert Boxes ─── */
    .stAlert {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(4px);
    }

    .stSuccess {
        background: rgba(0, 210, 255, 0.05) !important;
        border: 1px solid rgba(0, 210, 255, 0.1);
        border-radius: 12px !important;
    }

    .stWarning {
        background: rgba(255, 165, 0, 0.05) !important;
        border: 1px solid rgba(255, 165, 0, 0.1);
        border-radius: 12px !important;
    }

    .stError {
        background: rgba(255, 0, 0, 0.05) !important;
        border: 1px solid rgba(255, 0, 0, 0.1);
        border-radius: 12px !important;
    }

    /* ─── Tabs ─── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 4px;
        border: 1px solid rgba(255, 255, 255, 0.04);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
        color: #94a3b8;
        transition: all 0.2s;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(0, 210, 255, 0.1);
        color: #00d2ff;
    }

    /* ─── Footer ─── */
    .footer {
        text-align: center;
        padding: 24px 0;
        border-top: 1px solid rgba(255, 255, 255, 0.04);
        font-size: 0.8rem;
        color: #475569;
    }

    .footer a {
        color: #00d2ff;
        text-decoration: none;
    }

    /* ─── Scrollbar ─── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0b0a1a; }
    ::-webkit-scrollbar-thumb { background: #00d2ff; border-radius: 8px; }

    /* ─── Splash Screen Animation ─── */
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); opacity: 0.7; }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in-up {
        animation: fadeInUp 0.8s ease forwards;
    }

    /* ─── Responsive ─── */
    @media (max-width: 640px) {
        h1 { font-size: 2.2rem !important; }
        .glass-card { padding: 20px 16px; }
        .feature-card { padding: 20px 16px; }
    }
    </style>

    <!-- Glowing Cursor HTML -->
    <div class="cursor-glow" id="cursorGlow"></div>

    <script>
    // Glowing Cursor
    document.addEventListener('mousemove', function(e) {
        const glow = document.getElementById('cursorGlow');
        if (glow) {
            glow.style.left = e.clientX + 'px';
            glow.style.top = e.clientY + 'px';
        }
    });
    </script>
    """, unsafe_allow_html=True)

load_css()

# ============================================
# 5. SPLASH SCREEN (5-second intro)
# ============================================
def show_splash():
    """Display a 5-second splash screen on first load."""
    if "splash_shown" not in st.session_state:
        st.session_state.splash_shown = True
        
        splash_html = """
        <div style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:9999;
                    background:#0b0a1a;display:flex;flex-direction:column;
                    align-items:center;justify-content:center;">
            <div style="font-size:4.5rem;animation:pulse 1.8s ease-in-out infinite;">🛡️</div>
            <div style="font-size:3.2rem;font-weight:800;
                        background:linear-gradient(135deg,#ffffff 40%,#00d2ff 100%);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        font-family:'Inter',sans-serif;">
                AgentShield
            </div>
            <div style="color:#94a3b8;letter-spacing:3px;text-transform:uppercase;font-size:1rem;
                        margin-top:0.5rem;">
                OOSC 4.0 · IIIT Allahabad
            </div>
            <div style="margin-top:2rem;padding:0.4rem 1.6rem;
                        border:1px solid rgba(0,210,255,0.2);
                        border-radius:40px;font-size:0.8rem;color:#00d2ff;
                        background:rgba(0,210,255,0.05);">
                ⚡ AI Agent Reliability Engine
            </div>
        </div>
        """
        st.markdown(splash_html, unsafe_allow_html=True)
        time.sleep(4)
        st.rerun()

# Show splash on first load
show_splash()

# ============================================
# 6. SESSION STATE
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
# 7. API FUNCTIONS
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
# 8. LANDING PAGE HERO SECTION (Inside Streamlit)
# ============================================
def show_landing_hero():
    """Display the hero section matching index.html design."""
    
    st.markdown("""
    <div style="text-align:center;padding:20px 0 30px 0;" class="fade-in-up">
        <div class="badge-primary" style="margin-bottom:1.5rem;">
            <i class="fas fa-robot" style="margin-right:8px;"></i> PS4 · AI Agent Evaluation & Reliability
        </div>
        <h1>Don't just evaluate.<br>Attack. Block. Fix. Verify.</h1>
        <p style="max-width:640px;margin:1rem auto 2rem;color:#94a3b8;font-size:1.15rem;line-height:1.7;">
            AgentShield is an <strong style="color:#fff;">active reliability engine</strong> for AI agents.
            It automatically generates adversarial tests, simulates risky actions,
            blocks destructive behavior, and proves that fixes actually work.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Show landing hero
show_landing_hero()

# ============================================
# 9. SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding-bottom:16px;border-bottom:1px solid rgba(255,255,255,0.04);">
        <div style="font-size:2rem;">🛡️</div>
        <div style="font-weight:700;font-size:1.1rem;background:linear-gradient(135deg,#ffffff 40%,#00d2ff 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            AgentShield
        </div>
        <div style="font-size:0.7rem;color:#475569;">v3.0.0 · OOSC 4.0</div>
    </div>
    """, unsafe_allow_html=True)
    
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
# 10. METRICS ROW (Glass Cards)
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
# 11. PS4 STORY SECTION (Glass Cards)
# ============================================
st.markdown("""
<div style="padding:20px 0 10px 0;">
    <h2 style="font-size:2rem;">Why <span style="color:#00d2ff;background:linear-gradient(135deg,#00d2ff,#3a7bd5);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">PS4</span>?</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="glass-card">
        <span class="stat-badge">⚠️ 70%</span> of AI agents fail on real-world tasks.
        Most evaluation tools only tell you <em>after</em> deployment—
        when the damage is already done.
        <br><br>
        <span style="color:#00d2ff;font-weight:600;">AgentShield</span> flips the script.
        We test agents <strong>before</strong> they go live,
        using a <span style="color:#00d2ff;">Feral Agent</span> that actively tries to break them,
        a <span style="color:#00d2ff;">Firewall</span> that blocks dangerous actions,
        and a <span style="color:#00d2ff;">Fix → Verify</span> loop that proves improvements.
        <br><br>
        <span style="font-size:0.85rem;color:#64748b;">
            <i class="fas fa-arrow-right" style="color:#00d2ff;margin-right:6px;"></i>
            Built for the OOSC 4.0 Hackathon · Problem Statement 4
        </span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:3.5rem;margin-bottom:12px;">⚡</div>
        <div style="font-weight:700;font-size:1.2rem;margin-bottom:12px;color:#eef2ff;">The AgentShield Flow</div>
        <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:4px 8px;font-size:0.85rem;color:#94a3b8;">
            <span style="background:rgba(255,255,255,0.04);padding:6px 14px;border-radius:40px;border:1px solid rgba(255,255,255,0.04);">🔍 Attack</span>
            <span style="color:#00d2ff;border:none;background:transparent;padding:0 4px;">→</span>
            <span style="background:rgba(255,255,255,0.04);padding:6px 14px;border-radius:40px;border:1px solid rgba(255,255,255,0.04);">🛡️ Block</span>
            <span style="color:#00d2ff;border:none;background:transparent;padding:0 4px;">→</span>
            <span style="background:rgba(255,255,255,0.04);padding:6px 14px;border-radius:40px;border:1px solid rgba(255,255,255,0.04);">🧠 Root Cause</span>
            <span style="color:#00d2ff;border:none;background:transparent;padding:0 4px;">→</span>
            <span style="background:rgba(255,255,255,0.04);padding:6px 14px;border-radius:40px;border:1px solid rgba(255,255,255,0.04);">🔧 Fix</span>
            <span style="color:#00d2ff;border:none;background:transparent;padding:0 4px;">→</span>
            <span style="background:rgba(255,255,255,0.04);padding:6px 14px;border-radius:40px;border:1px solid rgba(255,255,255,0.04);">✅ Verify</span>
        </div>
        <div style="margin-top:16px;font-size:0.75rem;color:#64748b;">
            <i class="fas fa-circle" style="color:#00d2ff;font-size:0.4rem;vertical-align:middle;"></i>
            Pre-deployment · Sandboxed · Actionable
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 12. MAIN CONTENT - REPORT
# ============================================
if has_report:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h3 style="font-size:1.3rem;">📊 Performance Metrics</h3>', unsafe_allow_html=True)
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
            yaxis_title=None,
            xaxis_title=None
        )
        fig.update_traces(texttemplate='%{y:.0f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3 style="font-size:1.3rem;">⚠️ Critical Issues</h3>', unsafe_allow_html=True)
        st.metric("Critical Failures", report.get("critical_failures", 0), delta_color="inverse")
        st.metric("Blocked Actions", report.get("blocked_count", 0))
        st.metric("Risky Allowed", report.get("allowed_risky", 0))
    
    # Attack Type Breakdown
    st.markdown('<h3 style="font-size:1.3rem;">📊 By Attack Type</h3>', unsafe_allow_html=True)
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
            yaxis_title=None,
            xaxis_title=None
        )
        fig.update_traces(texttemplate='%{y:.0f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.markdown('<h3 style="font-size:1.3rem;">💡 Fix Recommendations</h3>', unsafe_allow_html=True)
    recs = report.get("recommendations", [])
    if recs:
        for rec in recs:
            st.info(rec)
    else:
        st.success("✅ All good!")
    
    # Before/After
    st.markdown('<h3 style="font-size:1.3rem;">🔄 Before → After</h3>', unsafe_allow_html=True)
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
# 13. FEATURES GRID (Glass Cards)
# ============================================
st.markdown("""
<div style="padding:30px 0 10px 0;">
    <h2 style="font-size:2rem;text-align:center;">Core <span style="color:#00d2ff;background:linear-gradient(135deg,#00d2ff,#3a7bd5);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Capabilities</span></h2>
    <p style="text-align:center;color:#94a3b8;max-width:560px;margin:0 auto 2rem;">Every feature is designed to close the loop from test to production.</p>
</div>
""", unsafe_allow_html=True)

cols = st.columns(3)

features = [
    ("🔥", "Action Firewall", "Real-time risk scoring & blocking of destructive tool calls."),
    ("🐺", "Feral Agent", "An AI adversary that actively tries to break your agent."),
    ("🧠", "Self-Evolving Tests", "Learns from production failures and generates new tests."),
    ("🔍", "Root Cause Graph", "Visual chain of why a failure happened — from input to root cause."),
    ("🦜", "Canary Testing", "Detects data exfiltration with canary tokens."),
    ("💰", "Cost Analytics", "Track test costs in USD & INR. Optimise your spend.")
]

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
# 14. EXPANDERS FOR DETAILED FEATURES
# ============================================

# Test Scenarios
with st.expander("📋 Test Scenarios"):
    scenarios = st.session_state.get("scenarios", [])
    if scenarios:
        df = pd.DataFrame(scenarios)
        cols = ["id", "attack_type", "input", "expected_behavior", "severity"]
        available = [c for c in cols if c in df.columns]
        st.dataframe(df[available], use_container_width=True, height=250)
    else:
        st.write("No scenarios yet")

# Feral Agent
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

# Self-Evolving Tests
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

# Root Cause
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

# Cost Tracker
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
        
        if st.button("📊 Cost-to-Fix"):
            data, error = api_request("get", "/cost-to-fix", timeout=30)
            if not error:
                st.json(data)
    
    else:
        st.info("Click 'Refresh Cost Summary' to see cost data.")

# Per-Turn Evaluation
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

# Canary Testing
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

# Fix → PR Generation
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

# Dataset Loader
with st.expander("📚 Dataset Loader"):
    st.subheader("Evaluation Datasets")
    st.caption("Built-in datasets: OWASP, MITRE, Prompt Injections, Destructive Actions, Benign, Edge Cases")
    
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
# 15. RAW REPORT
# ============================================
with st.expander("📊 Raw Report"):
    if has_report:
        st.json(report)
    else:
        st.write("Run tests to see report")

# ============================================
# 16. FOOTER
# ============================================
st.markdown("""
<div class="footer">
    🛡️ AgentShield v3.0.0 · Built for <a href="#">OOSC 4.0</a> · IIIT Allahabad · 2026
    <br>
    <span style="color:#475569;">PS4 · AI Agent Evaluation &amp; Reliability Engine</span>
</div>
""", unsafe_allow_html=True)
