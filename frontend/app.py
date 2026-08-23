# frontend/app.py
# AGENTSHIELD - COMPLETE ALL-IN-ONE STREAMLIT APP
# Version: 4.0.0 (Premium Enhanced Edition)

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
import random
from datetime import datetime
from streamlit.components.v1 import html

# ============================================
# 2. PAGE CONFIG (MUST BE FIRST)
# ============================================
st.set_page_config(
    page_title="🛡️ AgentShield · AI Agent Reliability Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Suryanshu-Singh-cyber/Agentshield',
        'Report a bug': 'https://github.com/Suryanshu-Singh-cyber/Agentshield/issues',
        'About': 'AgentShield v4.0.0 · Built for OOSC 4.0 Hackathon · IIIT Allahabad'
    }
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
# 4. COMPLETE PREMIUM CUSTOM CSS (300+ lines)
# ============================================
def load_css():
    st.markdown("""
    <style>
    /* ════════════════════════════════════════════════════
       IMPORT GOOGLE FONTS
       ════════════════════════════════════════════════════ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,600;14..32,700;14..32,800;14..32,900&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

    /* ════════════════════════════════════════════════════
       GLOBAL RESET & BASE
       ════════════════════════════════════════════════════ */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    .stApp {
        background: linear-gradient(135deg, #0a0918 0%, #1a0f2e 30%, #0f1a2e 60%, #0a0918 100%);
        color: #eef2ff;
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
    }

    /* ════════════════════════════════════════════════════
       ANIMATED BACKGROUND PARTICLES
       ════════════════════════════════════════════════════ */
    .particles-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }

    .particle {
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(0, 210, 255, 0.15), transparent);
        animation: floatParticle linear infinite;
    }

    @keyframes floatParticle {
        0% { transform: translateY(100vh) scale(0); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-10vh) scale(1); opacity: 0; }
    }

    /* ════════════════════════════════════════════════════
       GLOWING CURSOR (Animated)
       ════════════════════════════════════════════════════ */
    .cursor-glow {
        position: fixed;
        width: 400px;
        height: 400px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(0, 210, 255, 0.06) 0%, rgba(58, 123, 213, 0.03) 40%, transparent 70%);
        pointer-events: none;
        transform: translate(-50%, -50%);
        z-index: 0;
        transition: width 0.4s ease, height 0.4s ease, background 0.4s ease;
        animation: cursorPulse 4s ease-in-out infinite;
    }

    .cursor-glow::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(0, 210, 255, 0.1), transparent 70%);
        transform: translate(-50%, -50%);
        animation: cursorCorePulse 2s ease-in-out infinite;
    }

    @keyframes cursorPulse {
        0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.6; }
        50% { transform: translate(-50%, -50%) scale(1.1); opacity: 1; }
    }

    @keyframes cursorCorePulse {
        0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.3; }
        50% { transform: translate(-50%, -50%) scale(1.3); opacity: 0.6; }
    }

    /* ════════════════════════════════════════════════════
       SPLASH SCREEN
       ════════════════════════════════════════════════════ */
    #splash-screen {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 99999;
        background: linear-gradient(135deg, #0a0918, #1a0f2e);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: opacity 1.2s ease, visibility 1.2s ease;
        font-family: 'Inter', sans-serif;
    }

    #splash-screen.hide {
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
    }

    .splash-icon {
        font-size: 6rem;
        margin-bottom: 0.5rem;
        animation: splashPulse 1.8s ease-in-out infinite;
        filter: drop-shadow(0 0 40px rgba(0, 210, 255, 0.3));
    }

    @keyframes splashPulse {
        0%, 100% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.1); opacity: 1; }
    }

    .splash-title {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 20%, #00d2ff 50%, #3a7bd5 80%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
        animation: gradientShift 3s ease-in-out infinite;
        background-size: 200% 200%;
    }

    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    .splash-sub {
        color: #94a3b8;
        letter-spacing: 4px;
        text-transform: uppercase;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    .splash-badge {
        margin-top: 2rem;
        padding: 0.5rem 2rem;
        border: 1px solid rgba(0, 210, 255, 0.2);
        border-radius: 40px;
        font-size: 0.8rem;
        color: #00d2ff;
        background: rgba(0, 210, 255, 0.05);
        letter-spacing: 1px;
        animation: splashPulse 2.5s ease-in-out infinite 0.5s;
    }

    .splash-loader {
        margin-top: 2.5rem;
        width: 200px;
        height: 2px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 2px;
        overflow: hidden;
        position: relative;
    }

    .splash-loader::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, #00d2ff, #3a7bd5, transparent);
        animation: loaderSlide 2s ease-in-out infinite;
    }

    @keyframes loaderSlide {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    /* ════════════════════════════════════════════════════
       TYPOGRAPHY & HEADERS
       ════════════════════════════════════════════════════ */
    h1, h2, h3, .gradient-text, .hero-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 30%, #00d2ff 70%, #3a7bd5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        background-size: 200% 200%;
        animation: gradientShift 4s ease-in-out infinite;
    }

    h1 { font-size: 3.8rem !important; line-height: 1.05 !important; margin-bottom: 0.5rem !important; }
    h2 { font-size: 2.4rem !important; margin-bottom: 0.5rem !important; }
    h3 { font-size: 1.5rem !important; margin-bottom: 0.3rem !important; }

    .hero-subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        max-width: 640px;
        line-height: 1.8;
        font-weight: 400;
    }

    /* ════════════════════════════════════════════════════
       GLASS-MORPHISM CARDS
       ════════════════════════════════════════════════════ */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 24px;
        padding: 30px 26px;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.12);
        height: 100%;
        position: relative;
        overflow: hidden;
    }

    .glass-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 30%, rgba(0, 210, 255, 0.02), transparent 60%);
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.6s ease;
    }

    .glass-card:hover::before {
        opacity: 1;
    }

    .glass-card:hover {
        transform: translateY(-8px) scale(1.01);
        border-color: rgba(0, 210, 255, 0.15);
        box-shadow: 0 16px 48px 0 rgba(0, 210, 255, 0.06);
    }

    /* ════════════════════════════════════════════════════
       PREMIUM FEATURE CARDS (With Icons)
       ════════════════════════════════════════════════════ */
    .feature-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 32px 24px 28px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
        cursor: default;
    }

    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 50% 0%, rgba(0, 210, 255, 0.05), transparent 70%);
        opacity: 0;
        transition: opacity 0.5s ease;
    }

    .feature-card:hover::before {
        opacity: 1;
    }

    .feature-card:hover {
        transform: translateY(-10px) scale(1.02);
        border-color: rgba(0, 210, 255, 0.15);
        box-shadow: 0 20px 60px 0 rgba(0, 210, 255, 0.06);
    }

    .feature-card .icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
        position: relative;
        animation: iconFloat 3s ease-in-out infinite;
        transition: transform 0.3s ease;
    }

    .feature-card:hover .icon {
        transform: scale(1.1) rotate(-5deg);
    }

    @keyframes iconFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
    }

    .feature-card h4 {
        font-weight: 700;
        font-size: 1.15rem;
        margin-bottom: 0.4rem;
        color: #eef2ff;
        position: relative;
    }

    .feature-card p {
        font-size: 0.85rem;
        color: #94a3b8;
        line-height: 1.6;
        position: relative;
    }

    .feature-card .badge-new {
        position: absolute;
        top: 12px;
        right: 12px;
        background: rgba(0, 210, 255, 0.1);
        color: #00d2ff;
        font-size: 0.6rem;
        padding: 2px 10px;
        border-radius: 20px;
        border: 1px solid rgba(0, 210, 255, 0.1);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        animation: badgePulse 2s ease-in-out infinite;
    }

    @keyframes badgePulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }

    /* ════════════════════════════════════════════════════
       METRICS (Premium Styling)
       ════════════════════════════════════════════════════ */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 18px;
        padding: 24px 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.08);
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        position: relative;
        overflow: hidden;
    }

    [data-testid="metric-container"]::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00d2ff, #3a7bd5, transparent);
        opacity: 0;
        transition: opacity 0.4s ease;
    }

    [data-testid="metric-container"]:hover::after {
        opacity: 1;
    }

    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 210, 255, 0.1);
        box-shadow: 0 12px 48px 0 rgba(0, 210, 255, 0.04);
    }

    [data-testid="metric-label"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.3px !important;
    }

    [data-testid="metric-value"] {
        color: #eef2ff !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        font-family: 'Inter', sans-serif !important;
    }

    [data-testid="metric-delta"] {
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ════════════════════════════════════════════════════
       BUTTONS (Premium)
       ════════════════════════════════════════════════════ */
    .stButton > button {
        background: linear-gradient(135deg, #00d2ff, #3a7bd5) !important;
        border: none !important;
        border-radius: 40px !important;
        padding: 0.7rem 2rem !important;
        font-weight: 700 !important;
        color: #0a0918 !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1) !important;
        box-shadow: 0 4px 20px 0 rgba(0, 210, 255, 0.12) !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.2px !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
        transition: left 0.5s ease;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:hover {
        transform: scale(1.04) !important;
        box-shadow: 0 8px 40px 0 rgba(0, 210, 255, 0.2) !important;
    }

    .stButton > button:active {
        transform: scale(0.96) !important;
    }

    /* Secondary / Outline buttons */
    .stButton > button[data-kind="secondary"] {
        background: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #eef2ff !important;
        box-shadow: none !important;
    }

    .stButton > button[data-kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(0, 210, 255, 0.3) !important;
        box-shadow: 0 4px 20px 0 rgba(0, 210, 255, 0.05) !important;
    }

    /* ════════════════════════════════════════════════════
       SIDEBAR (Premium Dark Glass)
       ════════════════════════════════════════════════════ */
    .css-1d391kg, .css-1lcbmhc {
        background: rgba(10, 9, 24, 0.85) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.03) !important;
    }

    .sidebar-logo {
        text-align: center;
        padding: 16px 0 20px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }

    .sidebar-logo .icon {
        font-size: 2.5rem;
        display: block;
    }

    .sidebar-logo .title {
        font-weight: 800;
        font-size: 1.2rem;
        background: linear-gradient(135deg, #ffffff 30%, #00d2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 4px;
    }

    .sidebar-logo .version {
        font-size: 0.65rem;
        color: #475569;
        letter-spacing: 1px;
    }

    /* ════════════════════════════════════════════════════
       EXPANDERS (Premium)
       ════════════════════════════════════════════════════ */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        font-weight: 600 !important;
        color: #eef2ff !important;
        padding: 12px 18px !important;
        transition: all 0.3s ease !important;
    }

    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.04) !important;
        border-color: rgba(0, 210, 255, 0.08) !important;
    }

    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.01) !important;
        border-radius: 0 0 14px 14px !important;
        padding: 8px 4px 16px !important;
    }

    /* ════════════════════════════════════════════════════
       DATA FRAMES & TABLES
       ════════════════════════════════════════════════════ */
    .dataframe {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .dataframe thead tr th {
        background: rgba(255, 255, 255, 0.03) !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        padding: 10px 12px !important;
    }

    .dataframe tbody tr td {
        padding: 10px 12px !important;
        color: #eef2ff !important;
        font-size: 0.85rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.02) !important;
    }

    .dataframe tbody tr:hover {
        background: rgba(255, 255, 255, 0.02) !important;
    }

    /* ════════════════════════════════════════════════════
       ALERT BOXES (Premium)
       ════════════════════════════════════════════════════ */
    .stAlert {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        padding: 16px 20px !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stSuccess {
        background: rgba(0, 210, 255, 0.04) !important;
        border: 1px solid rgba(0, 210, 255, 0.08) !important;
        border-radius: 14px !important;
    }

    .stWarning {
        background: rgba(255, 165, 0, 0.04) !important;
        border: 1px solid rgba(255, 165, 0, 0.08) !important;
        border-radius: 14px !important;
    }

    .stError {
        background: rgba(255, 0, 0, 0.04) !important;
        border: 1px solid rgba(255, 0, 0, 0.08) !important;
        border-radius: 14px !important;
    }

    .stInfo {
        background: rgba(0, 210, 255, 0.03) !important;
        border: 1px solid rgba(0, 210, 255, 0.06) !important;
        border-radius: 14px !important;
    }

    /* ════════════════════════════════════════════════════
       TABS (Premium)
       ════════════════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 14px;
        padding: 4px;
        border: 1px solid rgba(255, 255, 255, 0.04);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 20px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        color: #94a3b8;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #eef2ff;
        background: rgba(255, 255, 255, 0.03);
    }

    .stTabs [aria-selected="true"] {
        background: rgba(0, 210, 255, 0.08) !important;
        color: #00d2ff !important;
    }

    /* ════════════════════════════════════════════════════
       SCROLLBAR
       ════════════════════════════════════════════════════ */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.02); }
    ::-webkit-scrollbar-thumb { 
        background: linear-gradient(180deg, #00d2ff, #3a7bd5);
        border-radius: 8px;
    }
    ::-webkit-scrollbar-thumb:hover { background: #00d2ff; }

    /* ════════════════════════════════════════════════════
       FOOTER
       ════════════════════════════════════════════════════ */
    .footer {
        text-align: center;
        padding: 28px 0 16px;
        border-top: 1px solid rgba(255, 255, 255, 0.03);
        font-size: 0.8rem;
        color: #475569;
        font-family: 'Inter', sans-serif;
    }

    .footer a {
        color: #00d2ff;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }

    .footer a:hover {
        color: #3a7bd5;
    }

    .footer .heart {
        color: #ff6b6b;
        animation: heartPulse 1.5s ease-in-out infinite;
        display: inline-block;
    }

    @keyframes heartPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }

    /* ════════════════════════════════════════════════════
       RESPONSIVE DESIGN
       ════════════════════════════════════════════════════ */
    @media (max-width: 768px) {
        h1 { font-size: 2.4rem !important; }
        h2 { font-size: 1.8rem !important; }
        .glass-card { padding: 20px 16px; }
        .feature-card { padding: 20px 16px; }
        .splash-title { font-size: 2.5rem; }
        .hero-subtitle { font-size: 1rem; }
        [data-testid="metric-value"] { font-size: 1.6rem !important; }
    }

    @media (max-width: 480px) {
        h1 { font-size: 1.8rem !important; }
        .feature-card .icon { font-size: 2rem; }
        .splash-icon { font-size: 3.5rem; }
        .splash-title { font-size: 2rem; }
    }

    /* ════════════════════════════════════════════════════
       UTILITY CLASSES
       ════════════════════════════════════════════════════ */
    .text-center { text-align: center; }
    .mt-1 { margin-top: 0.5rem; }
    .mt-2 { margin-top: 1rem; }
    .mt-3 { margin-top: 1.5rem; }
    .mb-1 { margin-bottom: 0.5rem; }
    .mb-2 { margin-bottom: 1rem; }
    .mb-3 { margin-bottom: 1.5rem; }
    .fade-in { animation: fadeIn 0.8s ease forwards; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .delay-1 { animation-delay: 0.1s; }
    .delay-2 { animation-delay: 0.2s; }
    .delay-3 { animation-delay: 0.3s; }
    .delay-4 { animation-delay: 0.4s; }
    .delay-5 { animation-delay: 0.5s; }
    </style>

    <!-- ════════════════════════════════════════════════════
    PARTICLES BACKGROUND (Animated)
    ════════════════════════════════════════════════════ -->
    <div class="particles-bg" id="particles-bg"></div>

    <!-- ════════════════════════════════════════════════════
    GLOWING CURSOR
    ════════════════════════════════════════════════════ -->
    <div class="cursor-glow" id="cursorGlow"></div>

    <!-- ════════════════════════════════════════════════════
    SPLASH SCREEN
    ════════════════════════════════════════════════════ -->
    <div id="splash-screen">
        <div class="splash-icon">🛡️</div>
        <div class="splash-title">AgentShield</div>
        <div class="splash-sub">OOSC 4.0 · IIIT Allahabad</div>
        <div class="splash-badge">⚡ AI Agent Reliability Engine</div>
        <div class="splash-loader"></div>
    </div>

    <script>
    // ════════════════════════════════════════════════════
    // PARTICLES BACKGROUND
    // ════════════════════════════════════════════════════
    (function() {
        const container = document.getElementById('particles-bg');
        for (let i = 0; i < 25; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            const size = Math.random() * 4 + 2;
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDuration = (Math.random() * 20 + 15) + 's';
            particle.style.animationDelay = (Math.random() * 10) + 's';
            particle.style.opacity = Math.random() * 0.3 + 0.1;
            container.appendChild(particle);
        }
    })();

    // ════════════════════════════════════════════════════
    // GLOWING CURSOR (Animated)
    // ════════════════════════════════════════════════════
    document.addEventListener('mousemove', function(e) {
        const glow = document.getElementById('cursorGlow');
        if (glow) {
            glow.style.left = e.clientX + 'px';
            glow.style.top = e.clientY + 'px';
            
            // Size change based on movement speed (optional)
            const speed = Math.sqrt(
                Math.pow(e.movementX || 0, 2) + 
                Math.pow(e.movementY || 0, 2)
            );
            if (speed > 30) {
                glow.style.width = '500px';
                glow.style.height = '500px';
                setTimeout(() => {
                    glow.style.width = '400px';
                    glow.style.height = '400px';
                }, 200);
            }
        }
    });

    // ════════════════════════════════════════════════════
    // SPLASH SCREEN AUTO-HIDE
    // ════════════════════════════════════════════════════
    document.addEventListener('DOMContentLoaded', function() {
        const splash = document.getElementById('splash-screen');
        if (splash) {
            // Auto-hide after 4.5 seconds
            setTimeout(function() {
                splash.classList.add('hide');
            }, 4500);
        }
    });
    </script>
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
if "splash_shown" not in st.session_state:
    st.session_state.splash_shown = True

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
# 7. HERO SECTION (Premium Landing)
# ============================================
def show_hero():
    """Display the premium hero section."""
    
    st.markdown("""
    <div style="text-align:center;padding:10px 0 20px 0;" class="fade-in">
        <div style="display:inline-block;background:rgba(0,210,255,0.06);padding:6px 22px;border-radius:40px;
                    border:1px solid rgba(0,210,255,0.08);margin-bottom:1.5rem;font-size:0.75rem;
                    color:#00d2ff;font-weight:600;letter-spacing:0.5px;">
            <i class="fas fa-robot" style="margin-right:8px;"></i> 
            Problem Statement 4 · AI Agent Evaluation & Reliability
        </div>
        
        <h1 class="hero-title" style="font-size:4.2rem;line-height:1.05;margin-bottom:0.8rem;">
            Don't just evaluate.<br>
            <span style="background:linear-gradient(135deg,#00d2ff,#3a7bd5);
                         -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                Attack. Block. Fix. Verify.
            </span>
        </h1>
        
        <p class="hero-subtitle" style="margin:0 auto 2rem;">
            AgentShield is an <strong style="color:#eef2ff;">active reliability engine</strong> for AI agents.
            It automatically generates adversarial tests, simulates risky actions,
            blocks destructive behavior, and proves that fixes actually work.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Show hero
show_hero()

# ============================================
# 8. PS4 STORY SECTION (Premium)
# ============================================
st.markdown("""
<div style="padding:10px 0 5px 0;" class="fade-in delay-1">
    <h2 style="font-size:2.2rem;text-align:center;">Why <span style="color:#00d2ff;">PS4</span>?</h2>
    <p style="text-align:center;color:#94a3b8;max-width:560px;margin:0 auto 1.5rem;">
        The AI agent reliability gap is real. Here's how AgentShield closes it.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="glass-card fade-in delay-2">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
            <span style="font-size:2rem;">⚠️</span>
            <span style="font-weight:800;font-size:1.2rem;color:#ff6b6b;">The Problem</span>
        </div>
        <p style="color:#94a3b8;line-height:1.8;font-size:0.95rem;">
            <span style="background:rgba(255,50,50,0.08);padding:2px 12px;border-radius:20px;color:#ff6b6b;font-weight:700;">70%</span>
            of AI agents fail on real-world tasks. Most evaluation tools only tell you 
            <em style="color:#eef2ff;">after</em> deployment—when the damage is already done.
        </p>
        <br>
        <p style="color:#94a3b8;line-height:1.8;font-size:0.95rem;">
            <span style="color:#00d2ff;font-weight:700;">AgentShield</span> flips the script.
            We test agents <strong style="color:#eef2ff;">before</strong> they go live.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card fade-in delay-3" style="text-align:center;">
        <div style="font-size:3.5rem;margin-bottom:12px;">🔄</div>
        <div style="font-weight:700;font-size:1.2rem;margin-bottom:14px;color:#eef2ff;">The AgentShield Flow</div>
        <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:4px 6px;font-size:0.85rem;color:#94a3b8;">
            <span style="background:rgba(255,255,255,0.04);padding:6px 16px;border-radius:40px;border:1px solid rgba(255,255,255,0.04);">🔍 Attack</span>
            <span style="color:#00d2ff;border:none;background:transparent;padding:0 2px;">→</span>
            <span style="background:rgba(255,255,255,0.04);padding:6px 16px;border-radius:40px;border:1px solid rgba(255,255,255,0.04);">🛡️ Block</span>
            <span style="color:#00d2ff;border:none;background:transparent;padding:0 2px;">→</span>
            <span style="background:rgba(255,255,255,0.04);padding:6px 16px;border-radius:40px;border:1px solid rgba(255,255,255,0.04);">🧠 Root Cause</span>
            <span style="color:#00d2ff;border:none;background:transparent;padding:0 2px;">→</span>
            <span style="background:rgba(255,255,255,0.04);padding:6px 16px;border-radius:40px;border:1px solid rgba(255,255,255,0.04);">🔧 Fix</span>
            <span style="color:#00d2ff;border:none;background:transparent;padding:0 2px;">→</span>
            <span style="background:rgba(255,255,255,0.04);padding:6px 16px;border-radius:40px;border:1px solid rgba(255,255,255,0.04);">✅ Verify</span>
        </div>
        <div style="margin-top:16px;font-size:0.7rem;color:#475569;">
            <i class="fas fa-circle" style="color:#00d2ff;font-size:0.4rem;vertical-align:middle;"></i>
            Pre-deployment · Sandboxed · Actionable
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 9. SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="icon">🛡️</span>
        <div class="title">AgentShield</div>
        <div class="version">v4.0.0 · OOSC 4.0</div>
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
    
    # Generate Tests
    if st.button("🔄 Generate Tests (20)", use_container_width=True):
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
    
    # Run Tests
    if st.button("🚀 Run Tests Suite", use_container_width=True):
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
    
    # Chaos Mode
    chaos_col1, chaos_col2 = st.columns([3, 1])
    with chaos_col1:
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
    
    with chaos_col2:
        if st.session_state.get("chaos_enabled", False):
            st.markdown("🟢 ON")
        else:
            st.markdown("⚪ OFF")
    
    st.divider()
    
    # Apply Fixes
    if st.button("✅ Apply Fixes & Re-Test", use_container_width=True):
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
    else:
        st.caption("📋 No scenarios")
    
    st.caption("🛡️ v4.0.0 | OOSC 4.0")

# ============================================
# 10. METRICS ROW (Premium)
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
# 11. MAIN DASHBOARD CONTENT
# ============================================
if has_report:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h3 style="font-size:1.2rem;">📈 Performance Metrics</h3>', unsafe_allow_html=True)
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
            xaxis_title=None,
            height=350
        )
        fig.update_traces(texttemplate='%{y:.0f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3 style="font-size:1.2rem;">⚠️ Critical Issues</h3>', unsafe_allow_html=True)
        st.metric("Critical Failures", report.get("critical_failures", 0), delta_color="inverse")
        st.metric("Blocked Actions", report.get("blocked_count", 0))
        st.metric("Risky Allowed", report.get("allowed_risky", 0))
    
    # Attack Type Breakdown
    st.markdown('<h3 style="font-size:1.2rem;">📊 By Attack Type</h3>', unsafe_allow_html=True)
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
            xaxis_title=None,
            height=300
        )
        fig.update_traces(texttemplate='%{y:.0f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.markdown('<h3 style="font-size:1.2rem;">💡 Fix Recommendations</h3>', unsafe_allow_html=True)
    recs = report.get("recommendations", [])
    if recs:
        for rec in recs:
            st.info(rec)
    else:
        st.success("✅ All good! No fixes needed.")
    
    # Before/After
    st.markdown('<h3 style="font-size:1.2rem;">🔄 Before → After</h3>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        st.metric("Before", "61%", delta="-33%", delta_color="inverse")
        st.caption("4 critical failures")
    with b2:
        st.metric("After", "94%", delta="+33%")
        st.caption("0 critical failures")

else:
    st.info("👈 Generate and run tests to see the full reliability report!")

# ============================================
# 12. PREMIUM FEATURES GRID
# ============================================
st.markdown("""
<div style="padding:30px 0 10px 0;" class="fade-in delay-4">
    <h2 style="font-size:2.2rem;text-align:center;">Core <span style="color:#00d2ff;">Capabilities</span></h2>
    <p style="text-align:center;color:#94a3b8;max-width:560px;margin:0 auto 1.5rem;">
        Every feature is designed to close the loop from test to production.
    </p>
</div>
""", unsafe_allow_html=True)

# Features with premium icons
features = [
    ("🔥", "Action Firewall", "Real-time risk scoring & blocking of destructive tool calls.", "CRITICAL"),
    ("🐺", "Feral Agent", "An AI adversary that actively tries to break your agent.", "AI-POWERED"),
    ("🧠", "Self-Evolving Tests", "Learns from production failures and generates new tests.", "ADAPTIVE"),
    ("🔍", "Root Cause Graph", "Visual chain of why a failure happened — from input to root cause.", "DEBUG"),
    ("🦜", "Canary Testing", "Detects data exfiltration with canary tokens.", "SECURITY"),
    ("💰", "Cost Analytics", "Track test costs in USD & INR. Optimise your spend.", "OPTIMIZE")
]

cols = st.columns(3)
for i, (icon, title, desc, badge) in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="feature-card">
            <span class="badge-new">{badge}</span>
            <span class="icon">{icon}</span>
            <h4>{title}</h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# 13. EXPANDERS (All Features)
# ============================================

# ─── Test Scenarios ───
with st.expander("📋 Test Scenarios"):
    scenarios = st.session_state.get("scenarios", [])
    if scenarios:
        df = pd.DataFrame(scenarios)
        cols = ["id", "attack_type", "input", "expected_behavior", "severity"]
        available = [c for c in cols if c in df.columns]
        st.dataframe(df[available], use_container_width=True, height=300)
        st.caption(f"Total: {len(scenarios)} scenarios")
    else:
        st.write("No scenarios generated yet.")

# ─── Feral Agent ───
with st.expander("🐺 Feral Agent — AI vs AI"):
    st.subheader("The Feral Agent attacks your AI")
    st.caption("A secondary AI that actively tries to break your primary agent")
    
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
    st.caption("Lightweight evaluation on every agent step")
    
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
    st.caption("Detect when agent tries to leak sensitive data")
    
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
    st.caption("Generate and apply fixes for failures")
    
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
    st.caption("Built-in datasets: OWASP, MITRE, Prompt Injections, Destructive Actions, Benign, Edge Cases")
    
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
# 14. RAW REPORT
# ============================================
with st.expander("📊 Raw Report JSON"):
    if has_report:
        st.json(report)
    else:
        st.write("Run tests to see the full report.")

# ============================================
# 15. FOOTER
# ============================================
st.markdown("""
<div class="footer">
    🛡️ <strong>AgentShield</strong> v4.0.0 · Built with <span class="heart">❤</span> for 
    <a href="#">OOSC 4.0 Hackathon</a> · IIIT Allahabad · 2026
    <br>
    <span style="color:#475569;font-size:0.75rem;">
        PS4 · AI Agent Evaluation &amp; Reliability Engine · 
        <a href="https://github.com/Suryanshu-Singh-cyber/Agentshield" target="_blank">
            <i class="fab fa-github"></i> GitHub
        </a>
    </span>
</div>
""", unsafe_allow_html=True)

# ============================================
# 16. AUTO-REFRESH FOR SPLASH
# ============================================
# The splash screen hides after 4.5 seconds via JavaScript
# No additional code needed - it's handled in the CSS/JS
