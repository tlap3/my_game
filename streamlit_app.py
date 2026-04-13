import streamlit as st
import random
import os
import asyncio
from edge_tts import Communicate

# --- 1. ตั้งค่าชื่อไฟล์ ---
MAIN_FILE = "vocabulary_China_game.txt"
CORRECT_FILE = "correct_china.txt"
WRONG_FILE = "wrong_china.txt"
TEMP_AUDIO = "temp_voice_china.mp3"

# --- 2. ฟังก์ชันจัดการข้อมูล ---
def load_data(path):
    data = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                p = line.strip().split(',')
                if len(p) == 3:
                    data.append({"word": p[0].strip(), "pinyin": p[1].strip(), "mean": p[2].strip()})
    return data

def save_to_file(item, target):
    existing = [v['word'] for v in load_data(target)]
    if item['word'] not in existing:
        with open(target, 'a', encoding='utf-8') as f:
            f.write(f"{item['word']},{item['pinyin']},{item['mean']}\n")

# ฟังก์ชันเล่นเสียง (เพิ่มระบบ Slow Rate)
async def get_voice(text, voice_type, slow=False):
    voice = "zh-CN-XiaoxiaoNeural" if voice_type == "f" else "zh-CN-YunxiNeural"
    # ปรับความเร็วเสียง: ถ้าช้าให้ใช้ -25%
    rate = "-25%" if slow else "+0%"
    comm = Communicate(text, voice, rate=rate)
    await comm.save(TEMP_AUDIO)

# --- 3. ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="Chinese Vocab Master", page_icon="🇨🇳")
st.title("🇨🇳 Chinese Vocab Master")

if 'game_data' not in st.session_state:
    st.session_state.game_data = load_data(MAIN_FILE)
    random.shuffle(st.session_state.game_data)
    st.session_state.current_item = None
    st.session_state.options = []
    st.session_state.voice_type = "f"
    st.session_state.mode = "choice"
    st.session_state.show_hint = False

def next_question():
    if st.session_state.game_data:
        st.session_state.current_item = st.session_state.game_data.pop()
        all_words = load_data(MAIN_FILE)
        all_means = list(set([v['mean'] for v in all_words]))
        wrong = [m for m in all_means if m != st.session_state.current_item['mean']]
        st.session_state.options = random.sample(wrong, min(len(wrong), 4)) + [st.session_state.current_item['mean']]
        random.shuffle(st.session_state.options)
        st.session_state.mode = "choice"
        st.session_state.show_hint = False
    else:
        st.success("ยินดีด้วย! คุณเรียนครบทุกคำแล้ว")

if st.session_state.current_item is None:
    next_question()

# --- 4. การแสดงผล UI ---
item = st.session_state.current_item

if item:
    # แสดงตัวจีนและพินอิน
    display_word = item['word'] if st.session_state.show_hint else "???"
    display_pinyin = item['pinyin'] if st.session_state.show_hint else "???"
    
    st.markdown(f"<h1 style='text-align: center; color: #d32f2f; font-size: 80px;'>{display_word}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 24px; font-style: italic;'>{display_pinyin}</p>", unsafe_allow_html=True)

    # --- ปุ่มฟังเสียง (ปกติ และ ช้า) ---
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        if st.button("🔊 ฟังปกติ (R)", use_container_width=True):
            asyncio.run(get_voice(item['word'], st.session_state.voice_type, slow=False))
            st.audio(TEMP_AUDIO, format="audio/mp3", autoplay=True)
    with col_v2:
        if st.button("🐢 ฟังช้าๆ (S)", use_container_width=True):
            asyncio.run(get_voice(item['word'], st.session_state.voice_type, slow=True))
            st.audio(TEMP_AUDIO, format="audio/mp3", autoplay=True)

    st.divider()

    # โหมดเลือกคำตอบ
    if st.session_state.mode == "choice":
        st.write("เลือกความหมายที่ถูกต้อง:")
        for idx, opt in enumerate(st.session_state.options):
            if st.button(f"{idx+1}. {opt}", key=f"opt_{idx}", use_container_width=True):
                if opt == item['mean']:
                    st.balloons()
                    st.session_state.mode = "spell"
                    st.session_state.show_hint = True
                    st.rerun()
                else:
                    st.error(f"ยังไม่ถูก! ลองฟังเสียงอีกครั้ง")
                    save_to_file(item, WRONG_FILE)

    # โหมดฝึกสะกด
    if st.session_state.mode == "spell":
        st.success(f"ถูกต้อง! ความหมายคือ: {item['mean']}")
        st.info(f"ฝึกพิมพ์สะกด: {item['word']} หรือ {item['pinyin']}")
        ans = st.text_input("พิมพ์ตัวจีนหรือพินอินตรงนี้แล้วกด Enter", key="spell_input")
        if ans:
            if ans.strip() in [item['word'], item['pinyin']]:
                save_to_file(item, CORRECT_FILE)
                if st.button("เก่งมาก! ไปข้อถัดไป ➡️"):
                    next_question()
                    st.rerun()
            else:
                st.warning("สะกดยังไม่ตรงครับ ลองดูคำใบ้ด้านบน")

    # แถบควบคุมด้านข้าง
    with st.sidebar:
        st.header("การตั้งค่า")
        st.session_state.voice_type = st.radio("เลือกเสียง", ("f", "m"), format_func=lambda x: "ผู้หญิง" if x=="f" else "ผู้ชาย")
        if st.button("👁️ แสดงคำใบ้ (H)"):
            st.session_state.show_hint = True
            st.rerun()
        if st.button("⏭️ ข้ามคำนี้"):
            next_question()
            st.rerun()
        st.divider()
        st.write("สถิติไฟล์จะถูกบันทึกชั่วคราวบน Server")
