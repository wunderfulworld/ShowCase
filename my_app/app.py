if st.button("❌ 關閉日誌並返回總目錄", use_container_width=True):
    st.session_state.diary_selector_state = "None"
    st.rerun()