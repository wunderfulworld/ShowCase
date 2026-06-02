import streamlit as st
from datetime import datetime, date, time, timedelta

# --- 1. 頁面配置 ---
st.set_page_config(page_title="ShowCase", page_icon="🎧", layout="wide", initial_sidebar_state="expanded")

# --- 2. 高級手帳風視覺 CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        background-color: #0d0e11;
        color: #e4e7ec;
        font-family: 'Inter', -apple-system, sans-serif;
        letter-spacing: 0.02em;
    }
    
    hr, [data-testid="ststDivider"] { display: none !important; }
    .stForm { border: none !important; padding: 0 !important; }
    
    .block-container {
        max-width: 800px !important;
        padding-bottom: 140px;
        padding-top: 40px;
        margin: 0 auto;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); width: 90%; max-width: 750px;
        background-color: rgba(23, 25, 30, 0.85);
        backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        z-index: 1000; justify-content: center; border-radius: 24px; padding-bottom: 8px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }
    .stTabs [data-baseweb="tab"] { height: 50px; color: #8892b0; font-weight: 400; font-size: 13px; }
    .stTabs [aria-selected="true"] { color: #deff9a !important; font-weight: 500; }
    
    .bubble-container {
        background: rgba(255, 255, 255, 0.015);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 14px;
    }
    
    .row-countdown-box {
        padding: 14px 18px; 
        border-left: 2px solid #deff9a; 
        background: rgba(255,255,255,0.015); 
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-bottom: 25px;
    }
    .dashboard-stat {
        background: rgba(255, 255, 255, 0.01);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 12px; padding: 14px; text-align: center;
    }
    
    .aesthetic-tag {
        display: inline-block; background: rgba(222, 255, 154, 0.05); color: #deff9a;
        padding: 2px 8px; border-radius: 4px; font-size: 11px; border: 1px solid rgba(222, 255, 154, 0.12);
    }
    .location-tag {
        display: inline-block; background: rgba(255, 255, 255, 0.03); color: #a8b2d1;
        padding: 2px 8px; border-radius: 4px; font-size: 11px; border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .time-tag {
        display: inline-block; background: rgba(222, 255, 154, 0.03); color: #deff9a;
        padding: 2px 8px; border-radius: 4px; font-size: 11px; border: 1px solid rgba(222, 255, 154, 0.08);
    }
    .price-tag {
        display: inline-block; background: rgba(255, 121, 198, 0.05); color: #ff79c6;
        padding: 2px 8px; border-radius: 4px; font-size: 11px; border: 1px solid rgba(255, 121, 198, 0.1);
    }
    
    .schedule-row {
        display: flex;
        align-items: flex-start;
        padding: 15px 5px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }
    .schedule-date-left {
        width: 80px;
        flex-shrink: 0;
        font-size: 14px;
        color: #deff9a;
        font-weight: 500;
        padding-top: 2px;
    }
    .schedule-detail-right {
        flex-grow: 1;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 數據初始化 (2026 香港熱門演出真實數據，基準日: 2026-06-01) ---
today = date(2026, 6, 1)

if 'concerts' not in st.session_state:
    st.session_state.concerts = [
        {"name": "五月天 [ 回到那一天 ] 25週年巡回演唱會 - 香港站", "date": date(2026, 7, 3), "time": time(19, 15), "location": "🎪 中環海濱活動空間", "id": "real_1", "heart": 0, "note": "", "seat": "A1區 15行", "price": 1580, "has_diary": False, "rundown": "", "custom_map": ""},
        {"name": "Serrini 《Every Our Little Magic》音樂會", "date": date(2026, 7, 18), "time": time(20, 0), "location": "🎵 亞洲國際博覽館 Arena", "id": "real_2", "heart": 0, "note": "",
