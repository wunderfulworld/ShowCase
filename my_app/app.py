import streamlit as st
from datetime import datetime, date, time, timedelta

# --- 1. 頁面配置 ---
st.set_page_config(page_title="ShowCase", page_icon="🎧", layout="wide", initial_sidebar_state="expanded")

# --- 2. 數據初始化 (2026 香港熱門演出真實數據，基準日: 2026-06-01) ---
today = date(2026, 6, 1)

if 'concerts' not in st.session_state:
    st.session_state.concerts = [
        {"name": "五月天 [ 回到那一天 ] 25週年巡回演唱會 - 香港站", "date": date(2026, 7, 3), "time": time(19, 15), "location": "🎪 中環海濱活動空間", "id": "real_1", "heart": 0, "note": "", "seat": "A1區 15行", "price": 1580, "has_diary": False, "rundown": "", "custom_map": ""},
        {"name": "Serrini 《Every Our Little Magic》音樂會", "date": date(2026, 7, 18), "time": time(20, 0), "location": "🎵 亞洲國際博覽館 Arena", "id": "real_2", "heart": 0, "note": "", "seat": "Block C 8行", "price": 880, "has_diary": False, "rundown": "", "custom_map": ""},
        {"name": "Jay Fung 馮允謙 演唱會 2026", "date": date(2026, 8, 22), "time": time(20, 15), "location": "🏛️ 香港體育館 (紅館)", "id": "real_3", "heart": 0, "note": "", "seat": "段位段 20行", "price": 1080, "has_diary": False, "rundown": "", "custom_map": ""},
        {"name": "鄭秀文 You & Mi 世界巡迴演唱會香港站 (補場)", "date": date(2026, 2, 14), "time": time(20, 15), "location": "🏛️ 香港體育館 (紅館)", "id": "real_4", "heart": 5, "note": "Sammi狀態大勇，情人節當晚全場大合唱《終身美麗》超級震撼！", "seat": "黃閘 15行", "price": 980, "has_diary": True, "rundown": "1. 經典序曲\n2. 終身美麗", "custom_map": ""},
        {"name": "MC 張天賦 《This is MC 2》演唱會", "date": date(2026, 4, 3), "time": time(20, 15), "location": "🏟️ 啟德體育園 (主場館)", "id": "real_5", "heart": 5, "note": "啟德音響出乎意料地好，現場演繹《記憶棉》實力驚人。", "seat": "內場 B區", "price": 1080, "has_diary": True, "rundown": "1. 老派約會之必要\n2. 記憶棉", "custom_map": ""}
    ]

if 'sales' not in st.session_state:
    st.session_state.sales = [
        {"name": "Clockenflap 2026 香港音樂及藝術節 (早鳥優惠)", "date": date(2026, 5, 25), "platform": "Ticketflap", "prices": "HK$1680", "id": "sale_1", "handled": False}
    ]

if 'entered' not in st.session_state: st.session_state.entered = False
if 'show_popup' not in st.session_state: st.session_state.show_popup = False

VENUE_CONFIG = {
    "🏛️ 香港體育館 (紅館)": {"map": "https://maps.google.com/?q=香港體育館", "rules": "1. 嚴禁攜帶長傘及專業攝影器材入場 \n2. 進場需接受隨身小包安全檢查"},
    "🏟️ 啟德體育園 (主場館)": {"map": "https://maps.google.com/?q=啟德體育園", "rules": "1. 現場全面禁帶外來飲食 \n2. 演算法應援燈牌需符合官方規格"},
    "🎪 中環海濱活動空間": {"map": "https://maps.google.com/?q=中環海濱活動空間", "rules": "1. 戶外音樂節請自備雨衣，嚴禁撐傘 \n2. 可憑手帶於指定區域重複進出"},
    "🎵 亞洲國際博覽館 Arena": {"map": "https://maps.google.com/?q=亞洲國際博覽館", "rules": "1. 亞博館場內全面禁煙 \n2. 搖滾區觀眾請依手帶序號排隊入場"},
    "✏️ 自定義場地 (手動輸入)": {"map": "", "rules": "自定義場地規範"}
}

# --- 3. 高級手帳風視覺 CSS ---
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
