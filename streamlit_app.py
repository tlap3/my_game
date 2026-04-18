# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="TLAP03 Game Center", page_icon="🎮", layout="wide")

# --- ข้อมูลเกม (เช็ค URL ให้ชัวร์) ---
GAMES_DATA = [
    {
        "title": "🎯 Target Mania: Boss Alert",
        "url": "https://github.io", 
        "desc": "เกมยิงเป้าท้าทายความไว (รันผ่าน GitHub Pages)"
    },
    {
        "title": "📖 Chinese Vocab Master",
        "url": "https://tlap03-chinese-vocab-app.streamlit.app/", 
        "desc": "ฝึกศัพท์จีน AI (รันผ่าน Streamlit Cloud)"
    }
]

st.title("🎮 TLAP03 HUB: ศูนย์รวมแอปและเกม")

# สร้างคอลัมน์ปุ่มเลือกเกม
cols = st.columns(len(GAMES_DATA))

for idx, game in enumerate(GAMES_DATA):
    with cols[idx]:
        if st.button(f"เลือก: {game['title']}", key=f"select_{idx}", use_container_width=True):
            st.session_state.active_game = game["url"]
            st.session_state.active_title = game["title"]

# --- พื้นที่แสดงผลเกม ---
if 'active_game' in st.session_state:
    st.divider()
    st.header(f"🕹️ กำลังโหลด: {st.session_state.active_title}")
    
    # 1. ลองเปิดแบบ Iframe ก่อน
    components.iframe(st.session_state.active_game, height=700, scrolling=True)
    
    # 2. เพิ่มปุ่มทางลัด (กรณีหน้าจอขาว/Iframe ไม่ขึ้น)
    st.info(f"💡 หากหน้าจอขาวค้างเกิน 10 วินาที ให้กดปุ่มเปิดหน้าเต็มด้านล่างครับ")
    st.link_button(f"👉 เปิด {st.session_state.active_title} แบบเต็มหน้าจอ", st.session_state.active_game)
    
    if st.button("❌ ปิดและกลับหน้าหลัก"):
        del st.session_state.active_game
        st.rerun()
