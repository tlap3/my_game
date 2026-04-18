# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="TLAP03 Game & Study Center", page_icon="🎮", layout="wide")

# --- ฐานข้อมูลเกม (เอาตัวใหม่ไว้บนสุด) ---
GAMES_DATA = [
    {
        "title": "🎯 Target Mania: Boss Alert",
        "url": "https://github.io",  # ลิงก์ GitHub Pages ของคุณ
        "desc": "เกมยิงเป้าท้าทายความไว พร้อมบอสสุดโหด! (ใหม่ล่าสุด)"
    },
    {
        "title": "📖 Chinese Vocab Master",
        "url": "https://tlap03.streamlit.app/", # !!! เปลี่ยนเป็น URL จริงของแอปศัพท์จีนที่คุณเพิ่งรัน !!!
        "desc": "ฝึกศัพท์จีนด้วยเสียงอ่านจาก AI พร้อมโหมดสะกด"
    }
]

st.title("🎮 TLAP03 HUB: ศูนย์รวมแอปและเกม")
st.write("เลือกรายการที่คุณต้องการเล่นหรือเรียนรู้ด้านล่างนี้:")

# สร้างแถวสำหรับการแสดงผลรายการ (แสดง 2 คอลัมน์)
cols = st.columns(2)

for idx, game in enumerate(GAMES_DATA):
    with cols[idx % 2]:
        with st.container(border=True):
            st.subheader(game["title"])
            st.write(game["desc"])
            
            # ปุ่มเข้าเล่น
            if st.button(f"เข้าเล่น {game['title']}", key=f"btn_{idx}", use_container_width=True):
                st.session_state.active_game = game["url"]
                st.session_state.active_title = game["title"]

# --- พื้นที่แสดงผลเกม (Iframe) ---
if 'active_game' in st.session_state:
    st.divider()
    st.header(f"🕹️ กำลังรัน: {st.session_state.active_title}")
    
    # ดึงหน้าเกมหรือแอปมาแสดง
    components.iframe(st.session_state.active_game, height=750, scrolling=True)
    
    if st.button("❌ ปิดหน้าต่างนี้"):
        del st.session_state.active_game
        st.rerun()
