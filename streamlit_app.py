# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components

# --- 1. ตั้งค่าหน้าเว็บ Hub ---
st.set_page_config(
    page_title="TLAP03 Game & Study Hub", 
    page_icon="🎮", 
    layout="wide"
)

# --- 2. ฐานข้อมูลแอปและเกม ---
# ให้คุณนำ URL รูปภาพจริงๆ และลิงก์ YouTube มาใส่ในช่องด้านล่างนี้ครับ
GAMES_DATA = [
    {
        "title": "🎯 Target Mania: Boss Alert",
        "url": "https://tlap3.github.io/my_game/Target-Mania-Boss-Alert/", 
        "image": "https://img.itch.zone/aW1hZ2UvNDQ4MTIyMS8yNjcxOTg5OC5qcGc=/original/8X1OnI.jpg", # <--- ใส่ URL รูปภาพหน้าปกเกมของคุณ
        "youtube": "https://youtu.be/oSYGz4ACYXY?si=_iZkxx6l2ht9Ccyv", # <--- ใส่ลิงก์ YouTube ของเกมนี้
        "desc": "เกมยิงเป้าท้าทายความไว พร้อมบอสสุดโหด!",
        "type": "game"
    },
    {
        "title": "📖 Chinese Vocab Master",
        "url": "https://tlap03-chinese-vocab-app.streamlit.app/", 
        "image": "https://githubusercontent.com", # <--- ใส่ URL รูปภาพหน้าปกแอปศัพท์จีน
        "youtube": "https://youtube.com", # <--- ใส่ลิงก์ YouTube ของแอปนี้
        "desc": "ฝึกศัพท์จีนด้วยเสียงอ่านจาก AI พร้อมโหมดสะกด",
        "type": "app"
    }
]

# --- 3. ส่วนหัวของหน้าเว็บ ---
st.title("🎮 TLAP03 HUB: ศูนย์รวมแอปและเกม")
st.write("ยินดีต้อนรับ! เลือกแอปหรือเกมที่ต้องการใช้งานด้านล่างนี้")
st.divider()

# --- 4. การแสดงผลรายการในรูปแบบ Grid ---
cols = st.columns(2)

for idx, item in enumerate(GAMES_DATA):
    with cols[idx % 2]:
        with st.container(border=True):
            # แสดงรูปหน้าปก (ถ้ายังไม่มีรูปจริง จะใช้ Placeholder ไปก่อน)
            st.image(item["image"], use_container_width=True, caption=item["title"])
            
            st.subheader(item["title"])
            st.write(item["desc"])
            
            # สร้างคอลัมน์เล็กๆ สำหรับปุ่มเล่นเกมและปุ่ม YouTube
            btn_col1, btn_col2 = st.columns([2, 1])
            
            with btn_col1:
                if st.button(f"🚀 เลือก: {item['title']}", key=f"select_{idx}", use_container_width=True):
                    st.session_state.active_url = item["url"]
                    st.session_state.active_title = item["title"]
                    st.session_state.active_type = item["type"]
            
            with btn_col2:
                # ปุ่มลิงก์ไป YouTube
                st.link_button("📺 ดูวิธีเล่น", item["youtube"], use_container_width=True)

# --- 5. พื้นที่รันแอป/เกม (จะแสดงเมื่อมีการกดเลือก) ---
if 'active_url' in st.session_state:
    st.write("---")
    st.header(f"🕹️ กำลังโหลด: {st.session_state.active_title}")
    
    if ".streamlit.app" in st.session_state.active_url:
        st.warning("⚠️ แอป Streamlit ไม่รองรับการแสดงผลซ้อนในหน้านี้")
        st.link_button(f"👉 คลิกเพื่อเปิดแอป {st.session_state.active_title}", st.session_state.active_url, use_container_width=True)
        st.info("แอปนี้จะเปิดขึ้นในแท็บใหม่ของ Browser")
        
    else:
        st.link_button("🌐 หากเกมไม่โหลด (หรือต้องการเล่นแบบเต็มหน้าจอ) คลิกที่นี่", st.session_state.active_url)
        components.iframe(st.session_state.active_url, height=750, scrolling=True)

    if st.button("❌ ปิดหน้าต่างนี้และกลับหน้าเมนูหลัก"):
        del st.session_state.active_url
        del st.session_state.active_title
        del st.session_state.active_type
        st.rerun()

# --- 6. Sidebar ---
with st.sidebar:
    st.title("📌 เกี่ยวกับ")
    st.info("นี่คือศูนย์กลางการเรียนรู้และเกมที่พัฒนาโดย TLAP03")
    st.write(f"จำนวนรายการทั้งหมด: {len(GAMES_DATA)}")
