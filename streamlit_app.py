# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components

# --- 1. ตั้งค่าหน้าเว็บ Hub ---
st.set_page_config(
    page_title="TLAP03 Game & Study Hub", 
    page_icon="🎮", 
    layout="wide"
)

# --- 2. ฐานข้อมูลแอปและเกม (ตัวล่าสุดอยู่บนสุด) ---
# หมายเหตุ: URL ของ Streamlit (.streamlit.app) จะเปิดใน iframe ไม่ได้ต้องใช้ปุ่มลิงก์
GAMES_DATA = [
    {
        "title": "🎯 Target Mania: Boss Alert",
        "url": "https://tlap3.github.io/my_game/Target-Mania-Boss-Alert/", 
        "image": "https://placeholder.com",
        "desc": "เกมยิงเป้าท้าทายความไว พร้อมบอสสุดโหด! (รันผ่าน GitHub Pages)",
        "type": "game"
    },
    {
        "title": "📖 Chinese Vocab Master",
        "url": "https://tlap03-chinese-vocab-app.streamlit.app/", 
        "image": "https://placeholder.com",
        "desc": "ฝึกศัพท์จีนด้วยเสียงอ่านจาก AI พร้อมโหมดสะกด (รันผ่าน Streamlit Cloud)",
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
            st.image(item["image"], use_container_width=True)
            st.subheader(item["title"])
            st.write(item["desc"])
            
            # ปุ่มเลือกใช้งาน
            if st.button(f"🚀 เลือก: {item['title']}", key=f"select_{idx}", use_container_width=True):
                st.session_state.active_url = item["url"]
                st.session_state.active_title = item["title"]
                st.session_state.active_type = item["type"]

# --- 5. พื้นที่รันแอป/เกม (จะแสดงเมื่อมีการกดเลือก) ---
if 'active_url' in st.session_state:
    st.write("---")
    st.header(f"🕹️ กำลังโหลด: {st.session_state.active_title}")
    
    # กรณีเป็นแอป Streamlit (ต้องใช้ปุ่มกดเปิดหน้าใหม่)
    if ".streamlit.app" in st.session_state.active_url:
        st.warning("⚠️ แอป Streamlit ไม่รองรับการแสดงผลซ้อนในหน้านี้ (Security Policy)")
        st.write("กรุณากดปุ่มสีฟ้าด้านล่างเพื่อเข้าสู่แอปโดยตรงครับ")
        st.link_button(f"👉 คลิกเพื่อเปิดแอป {st.session_state.active_title}", st.session_state.active_url, use_container_width=True)
        
        # แสดงหน้าต่างเปล่าๆ ไว้เพื่อให้รู้ว่ามีแอปอยู่
        st.info("แอปนี้จะเปิดขึ้นในแท็บใหม่ของ Browser ของคุณ")
        
    # กรณีเป็นเกมจาก GitHub Pages (รันผ่าน iframe ได้)
    else:
        # ปุ่มทางเลือกเผื่อ iframe ไม่รัน
        st.link_button("🌐 หากเกมไม่โหลด (หรือต้องการเล่นแบบเต็มหน้าจอ) คลิกที่นี่", st.session_state.active_url)
        
        # แสดงผลผ่าน Iframe
        components.iframe(st.session_state.active_url, height=750, scrolling=True)

    # ปุ่มปิดเพื่อกลับหน้าหลัก
    if st.button("❌ ปิดหน้าต่างนี้และกลับหน้าเมนูหลัก"):
        del st.session_state.active_url
        del st.session_state.active_title
        del st.session_state.active_type
        st.rerun()

# --- 6. ส่วนท้ายหน้าเว็บ ---
st.sidebar.title("📌 เกี่ยวกับ")
st.sidebar.info("นี่คือศูนย์กลางการเรียนรู้และเกมที่พัฒนาโดย TLAP03")
st.sidebar.write(f"จำนวนรายการทั้งหมด: {len(GAMES_DATA)}")
