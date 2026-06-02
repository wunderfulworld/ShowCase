import streamlit as st
from datetime import datetime, date, time, timedelta

# --- 1. 頁面配置與高級手帳風視覺 CSS ---
st.set_page_config(page_title="ShowCase", page_icon="🎧", layout="wide", initial_sidebar_state="expanded")

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
    
    /* 限制內容最大寬度，避免卡片過寬 */
    .block-container {
        max-width: 800px !important;
        padding-bottom: 140px;
        padding-top: 40px;
        margin: 0 auto;
    }
    
    /* 懸浮半透明 Tab Bar */
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
    
    /* 極簡極細邊框 Bubble Container */
    .bubble-container {
        background: rgba(255, 255, 255, 0.015);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 14px;
    }
    
    /* 倒數頁專用：原生 Flex 輕量化卡片底色 */
    .countdown-box {
        background: rgba(255, 255, 255, 0.015);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 12px;
        text-align: center;
        min-height: 120px;
    }
    
    /* 數據面板平排 Grid */
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
    
    /* 文青手帳標籤風格 */
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
    
    /* Schedule Book 排版格式 */
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

# --- 2. 2026 香港熱門演出真實數據 (基準日: 2026-06-01) ---
today = date(2026, 6, 1)

VENUE_CONFIG = {
    "🏛️ 香港體育館 (紅館)": {"map": "https://maps.google.com", "rules": "1. 嚴禁攜帶長傘及專業攝影器材入場 \n2. 進場需接受隨身小包安全檢查"},
    "🏟️ 啟德體育園 (主場館)": {"map": "https://maps.google.com", "rules": "1. 現場全面禁帶外來飲食 \n2. 演算法應援燈牌需符合官方規格"},
    "🎪 中環海濱活動空間": {"map": "https://maps.google.com", "rules": "1. 戶外音樂節請自備雨衣，嚴禁撐傘 \n2. 可憑手帶於指定區域重複進出"},
    "🎵 亞洲國際博覽館 Arena": {"map": "https://maps.google.com", "rules": "1. 亞博館場內全面禁煙 \n2. 搖滾區觀眾請依手帶序號排隊入場"}
}

if 'concerts' not in st.session_state:
    st.session_state.concerts = [
        {"name": "五月天 [ 回到那一天 ] 25週年巡回演唱會 - 香港站", "date": date(2026, 7, 3), "time": time(19, 15), "location": "🎪 中環海濱活動空間", "id": "real_1", "heart": 0, "note": "", "seat": "A1區 15行", "price": 1580, "has_diary": False},
        {"name": "Serrini 《Every Our Little Magic》音樂會", "date": date(2026, 7, 18), "time": time(20, 0), "location": "🎵 亞洲國際博覽館 Arena", "id": "real_2", "heart": 0, "note": "", "seat": "Block C 8行", "price": 880, "has_diary": False},
        {"name": "Jay Fung 馮允謙 演唱會 2026", "date": date(2026, 8, 22), "time": time(20, 15), "location": "🏛️ 香港體育館 (紅館)", "id": "real_3", "heart": 0, "note": "", "seat": "段位段 20行", "price": 1080, "has_diary": False},
        {"name": "鄭秀文 You & Mi 世界巡迴演唱會香港站 (補場)", "date": date(2026, 2, 14), "time": time(20, 15), "location": "🏛️ 香港體育館 (紅館)", "id": "real_4", "heart": 5, "note": "Sammi狀態大勇，情人節當晚全場大合唱《終身美麗》超級震撼！", "seat": "黃閘 15行", "price": 980, "has_diary": True},
        {"name": "MC 張天賦 《This is MC 2》演唱會", "date": date(2026, 4, 3), "time": time(20, 15), "location": "🏟️ 啟德體育園 (主場館)", "id": "real_5", "heart": 5, "note": "啟德音響出乎意料地好，現場演繹《記憶棉》實力驚人。", "seat": "內場 B區", "price": 1080, "has_diary": True}
    ]

if 'sales' not in st.session_state:
    st.session_state.sales = [
        {"name": "Clockenflap 2026 香港音樂及藝術節 (早鳥優惠)", "date": date(2026, 5, 25), "platform": "Ticketflap", "prices": "HK$1680", "id": "sale_1", "handled": False}
    ]

if 'entered' not in st.session_state: st.session_state.entered = False
if 'show_popup' not in st.session_state: st.session_state.show_popup = False

# --- 🚪 歡迎入口首頁 ---
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

# --- 🏠 主程式界面 ---
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
                m_price = st.number_input("票價 (HKD)", value=0, step=50)
                m_seat = st.text_input("觀看座位", placeholder="例：Block A 15行")
                
                if st.form_submit_button("登記行程"):
                    if m_name:
                        st.session_state.concerts.append({
                            "name": m_name, "date": m_date, "time": m_time, "location": m_loc, 
                            "id": f"show_{len(st.session_state.concerts) + 1}", "heart": 0, "note": "", 
                            "seat": m_seat, "price": int(m_price), "has_diary": False
                        })
                        st.rerun()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 我的 ShowCase", "⏳ 實時倒數", "📅 我的日程", "🎁 回憶盒子", "🚨 搶飛提醒"])

    upcoming_shows = sorted([c for c in st.session_state.concerts if c["date"] >= today], key=lambda x: x["date"])
    past_shows = sorted([c for c in st.session_state.concerts if c["date"] < today], key=lambda x: x["date"], reverse=True)
    diary_shows = [c for c in st.session_state.concerts if c["has_diary"]]
    total_spent = sum([c["price"] for c in st.session_state.concerts])

    # --- Tab 1: 🏠 我的 ShowCase ---
    with tab1:
        st.markdown("<h2 style='font-size: 20px; font-weight: 400; margin-top:0;'>🏠 我的 ShowCase</h2>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='dashboard-grid'>
            <div class='dashboard-stat'><span style='color:#a8b2d1; font-size:12px;'>已觀看現場</span><br><b style='color:#9effeb; font-size:22px; font-weight:400;'>{len(past_shows)}</b> <span style='font-size:11px;color:#666;'>場</span></div>
            <div class='dashboard-stat'><span style='color:#a8b2d1; font-size:12px;'>已預訂日程</span><br><b style='color:#deff9a; font-size:22px; font-weight:400;'>{len(upcoming_shows)}</b> <span style='font-size:11px;color:#666;'>場</span></div>
            <div class='dashboard-stat'><span style='color:#a8b2d1; font-size:12px;'>累積消費總額</span><br><b style='color:#ff79c6; font-size:22px; font-weight:400;'>${total_spent}</b> <span style='font-size:11px;color:#666;'>HKD</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        if upcoming_shows:
            next_show = upcoming_shows[0]
            days_left = (next_show["date"] - today).days
            st.markdown(f"""
            <div style='padding: 14px 18px; border-left: 2px solid #deff9a; background: rgba(255,255,255,0.01); margin-bottom: 20px;'>
                <span style='color:#deff9a; font-size:11px; font-weight:600;'>NEXT EVENT</span>
                <span style='color:#fff; font-size:14px; margin-left: 15px;'>{next_show['name']}</span>
                <span style='color:#8892b0; font-size:12px; margin-left: 15px;'>距離相遇還有 {days_left} 天</span>
            </div>
            """, unsafe_allow_html=True)
            
        if st.button("📋 複製我的專屬日程分享連結", use_container_width=True):
            st.toast("✨ 連結已複製！")

    # --- Tab 2: ⏳ 實時倒數 ---
    with tab2:
        st.markdown("<h2 style='font-size: 20px; font-weight: 400; margin-top:0;'>⏳ 實時倒數</h2>", unsafe_allow_html=True)
        if upcoming_shows:
            for i in range(0, len(upcoming_shows), 3):
                row_items = upcoming_shows[i:i+3]
                cols = st.columns(3)
                for idx, c in enumerate(row_items):
                    days = (c["date"] - today).days
                    with cols[idx]:
                        st.markdown(f"""
                        <div class='countdown-box'>
                            <p style='color:#fff; font-size:13px; font-weight:400; margin:0 0 10px 0; line-height:1.4;'>{c['name']}</p>
                            <div style='margin-bottom:6px;'><span class='location-tag' style='font-size:10px;'>{c['location'].split(' ')[1]}</span></div>
                            <b style='color:#deff9a; font-size:22px; font-weight:300;'>{days}</b> <span style='font-size:10px; color:#666;'>Days</span>
                        </div>
                        """, unsafe_allow_html=True)

    # --- Tab 3: 📅 我的日程 ---
    with tab3:
        st.markdown("<h2 style='font-size: 20px; font-weight: 400; margin-top:0;'>📅 我的日程</h2>", unsafe_allow_html=True)
        
        for c in upcoming_shows:
            idx = st.session_state.concerts.index(c)
            
            st.markdown(f"""
            <div class='schedule-row'>
                <div class='schedule-date-left'>
                    {c['date'].strftime('%m.%d')}<br>
                    <span style='font-size:11px; color:#444;'>2026</span>
                </div>
                <div class='schedule-detail-right'>
                    <h4 style='margin:0 0 10px 0; color:#fff; font-weight:400; font-size:15px;'>{c['name']}</h4>
                    <div style='display:flex; gap:8px; align-items:center;'>
                        <span class='time-tag'>⏱️ {c['time'].strftime('%H:%M')}</span>
                        <span class='location-tag'>{c['location']}</span>
                        {f"<span class='price-tag'>💰 ${c['price']} ({c['seat']})</span>" if c['price'] > 0 else ""}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📝 檢視備忘與場館指南"):
                col_det1, col_det2 = st.columns(2)
                venue_data = VENUE_CONFIG.get(c["location"], {"map": "#", "rules": "暫無資料"})
                with col_det1:
                    user_note = st.text_input("個人隨記備忘：", value=c.get('note', ''), key=f"note_input_{c['id']}")
                    if user_note != c.get('note', ''): 
                        st.session_state.concerts[idx]['note'] = user_note
                with col_det2:
                    st.caption(venue_data['rules'])
            st.write("")

    # --- Tab 4: 🎁 回憶盒子 ---
    with tab4:
        st.markdown("<h2 style='font-size: 20px; font-weight: 400; margin-top:0;'>🎁 回憶盒子</h2>", unsafe_allow_html=True)
        
        for i, p in enumerate(past_shows, 1):
            idx = st.session_state.concerts.index(p)
            st.markdown(f"""
            <div class='bubble-container' style='margin-bottom:6px; padding:12px 18px;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <span style='color:#444; font-size:11px; font-weight:bold; margin-right:10px;'>#MEMO-{str(i).zfill(2)}</span>
                        <span style='color:#a8b2d1; font-size:12px;'>{p['date'].strftime('%Y.%m.%d')}</span>
                        <span style='color:#fff; font-size:14px; margin-left:15px;'>{p['name']}</span>
                    </div>
                    <div>
                        <span class='price-tag'>${p['price']}</span>
                        <span class='location-tag' style='font-size:10px;'>{p['seat']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander(f"🖋️ 留下一點當晚的隨筆"):
                has_diary = st.checkbox("在回憶盒子裡收藏這篇日記", value=p.get('has_diary', False), key=f"has_diary_{p['id']}")
                if has_diary != p.get('has_diary', False):
                    st.session_state.concerts[idx]['has_diary'] = has_diary
                    st.rerun()
                    
                if has_diary:
                    col_box1, col_box2 = st.columns([2, 1.5])
                    with col_box1:
                        user_story = st.text_area("當晚的碎碎念與感動...", value=p.get('note', ''), key=f"past_note_{p['id']}", height=80)
                        if user_story != p.get('note', ''): st.session_state.concerts[idx]['note'] = user_story
                    with col_box2:
                        st.write("情感刻度：")
                        btn_cols = st.columns(5)
                        chosen_score = p.get('heart', 0)
                        for score_idx in range(1, 6):
                            icon = "❤️" if chosen_score >= score_idx else "🤍"
                            if btn_cols[score_idx-1].button(icon, key=f"btn_{p['id']}_{score_idx}"):
                                st.session_state.concerts[idx]['heart'] = score_idx
                                rerun()

    # --- Tab 5: 🚨 搶飛提醒 ---
    with tab5:
        st.markdown("<h2 style='font-size: 20px; font-weight: 400; margin-top:0;'>🚨 搶飛提醒</h2>", unsafe_allow_html=True)
        
        active_sales = [s for s in st.session_state.sales if s["date"] >= today]
        passed_sales = [s for s in st.session_state.sales if s["date"] < today and not s["handled"]]
        
        if passed_sales:
            for ps in passed_sales:
                s_idx = st.session_state.sales.index(ps)
                st.markdown(f"""
                <div style='padding:12px; border-left: 2px solid #ff79c6; background:rgba(255, 121, 198, 0.01); margin-bottom:14px;'>
                    <h3 style='color:#fff; font-size:16px; font-weight:600; margin:0 0 6px 0;'>{ps['name']}</h3>
                    <span style='color:#ff79c6; font-size:11px;'>開售日：{ps['date'].strftime('%m.%d')}</span>
                    <span style='color:#8892b0; font-size:11px; margin-left:10px;'>購票結果確認：</span>
                </div>
                """, unsafe_allow_html=True)
                
                q_col1, q_col2 = st.columns(2)
                with q_col1:
                    if st.button("🎉 成功成功", key=f"yes_{ps['id']}", use_container_width=True):
                        st.session_state.sales[s_idx]['success_flow'] = True
                with q_col2:
                    if st.button("😢 未成功", key=f"no_{ps['id']}", use_container_width=True):
                        st.session_state.sales[s_idx]['handled'] = True
                        st.rerun()
                
                if ps.get('success_flow', False):
                    st.markdown("<div class='bubble-container'>", unsafe_allow_html=True)
                    with st.form(f"auto_add_{ps['id']}"):
                        f_date = st.date_input("演出日期", value=date(2026, 11, 27)) 
                        f_time = st.time_input("開演時間", value=time(16, 0))
                        f_loc = st.selectbox("演出場地", list(VENUE_CONFIG.keys()), index=2)
                        f_price = st.number_input("實質買到票價 (HKD)", value=1680)
                        f_seat = st.text_input("座位/行數", value="三日票 Free Standing")
                        
                        if st.form_submit_button("登記並歸入日程"):
                            st.session_state.concerts.append({
                                "name": "Clockenflap 2026 香港音樂及藝術節",
                                "date": f_date, "time": f_time, "location": f_loc,
                                "id": f"auto_gen_{len(st.session_state.concerts)+1}",
                                "heart": 0, "note": "", "seat": f_seat, "price": int(f_price), "has_diary": False
                            })
                            st.session_state.sales[s_idx]['handled'] = True
                            st.toast("🎉 新行程已建立！")
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

        for s in active_sales:
            st.markdown(f"""
            <div class='bubble-container' style='padding: 14px 18px;'>
                <h3 style='color:#fff; font-size:16px; font-weight:600; margin:0 0 8px 0;'>{s['name']}</h3>
                <div style='display:flex; gap:12px; align-items:center;'>
                    <span style='color:#8892b0; font-size:11px;'>📅 開售：{s['date'].strftime('%m.%d')}</span>
                    <span class='location-tag' style='font-size:10px;'>{s['platform']}</span>
                    <span class='price-tag' style='font-size:10px;'>{s['prices']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)