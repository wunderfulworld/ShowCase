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

# --- 3. 數據初始化 (基準日: 2026-06-01) ---
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
        {"name": "Clockenflap 2026 香港音樂及藝術節 (早鳥優惠)", "date": date(2026, 5, 25), "platform": "Ticketflap", "prices": "HK$1680", "id": "sale_1", "handled": False},
        {"name": "Coldplay 2026 世界巡迴演唱會 - 香港站開售", "date": date(2026, 6, 15), "platform": "Cityline", "prices": "HK$380 - HK$1380", "id": "sale_2", "handled": False}
    ]

if 'entered' not in st.session_state: st.session_state.entered = False
if 'show_popup' not in st.session_state: st.session_state.show_popup = False

if 'diary_selector_state' not in st.session_state:
    st.session_state.diary_selector_state = "None"

VENUE_CONFIG = {
    "🏛️ 香港體育館 (紅館)": {"map": "https://maps.google.com/?q=香港體育館", "rules": "1. 嚴禁攜帶長傘及專業攝影器材入場 \n2. 進場需接受隨身小包安全檢查"},
    "🏟️ 啟德體育園 (主場館)": {"map": "https://maps.google.com/?q=啟德體育園", "rules": "1. 現場全面禁帶外來飲食 \n2. 演算法應援燈牌需符合官方規格"},
    "🎪 中環海濱活動空間": {"map": "https://maps.google.com/?q=中環海濱活動空間", "rules": "1. 戶外音樂節請自備雨衣，嚴禁撐傘 \n2. 可憑手帶於指定區域重複進出"},
    "🎵 亞洲國際博覽館 Arena": {"map": "https://maps.google.com/?q=亞洲國際博覽館", "rules": "1. 亞博館場內全面禁煙 \n2. 搖滾區觀眾請依手帶序號排隊入場"},
    "✏️ 自定義場地 (手動輸入)": {"map": "", "rules": "自定義場地規範"}
}

# --- 4. 🚪 歡迎入口首頁 ---
if not st.session_state.entered:
    st.write(""); st.write(""); st.write("")
    st.markdown("<h1 style='text-align: center; color: #deff9a; font-size: 46px; font-weight:400; margin-bottom:10px; letter-spacing:0.05em;'>✨ ShowCase</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8892b0; font-size: 15px; margin-bottom:50px;'>將你看的每場演出收藏在你的ShowCase</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button("🎵 進入你的ShowCase", use_container_width=True):
            st.session_state.entered = True
            st.session_state.show_popup = True  
            st.rerun()

# --- 5. 🏠 主程式界面 ---
else:
    if st.session_state.show_popup:
        today_shows = [c for c in st.session_state.concerts if c["date"] == today]
        three_days_later = today + timedelta(days=3)
        near_shows = [c for c in st.session_state.concerts if today < c["date"] <= three_days_later]
        near_sales = [s for s in st.session_state.sales if today < s["date"] <= three_days_later and not s["handled"]]
        
        if today_shows:
            for ts in today_shows:
                st.toast(f"🚨 今日重要提醒：就是今天！《{ts['name']}》即將開演，記得帶齊門票！")
        elif near_shows or near_sales:
            for ns in near_shows:
                st.toast(f"⏳ 3日內事件提醒：演出《{ns['name']}》即將在 {ns['date'].strftime('%m月%d日')} 到來！")
            for nsa in near_sales:
                st.toast(f"🎟️ 3內日搶飛提醒：{nsa['name']} 將於 {nsa['date'].strftime('%m月%d日')} 開售！")
        else:
            st.toast("✨ 今日無特別事。今天也是被音樂治癒的一天。")
        st.session_state.show_popup = False 
        
    with st.sidebar:
        st.markdown("<div style='text-align:center; padding: 20px 0 10px 0;'><p style='color:#deff9a; font-size:11px; letter-spacing:0.1em; margin:0;'>MY PLANNER</p><h2 style='color:#fff; margin:5px 0 15px 0; font-size:19px; font-weight:400;'>音樂漫遊者</h2><span class='aesthetic-tag'>隨身離線版</span></div>", unsafe_allow_html=True)
        st.write("")
        
        with st.expander("➕ 記錄演出行程"):
            with st.form("mini_add", clear_on_submit=True):
                m_name = st.text_input("演出名稱")
                m_date = st.date_input("演出日期", value=today)
                m_time = st.time_input("開演時間", value=time(20, 0))
                m_loc = st.selectbox("演出場地", list(VENUE_CONFIG.keys()))
                m_price =