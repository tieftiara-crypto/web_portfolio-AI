import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

st.title("🤖 Asisten Pintar Eftiara")
st.write("Selamat datang di portofolio AI buatan Eftiara! Silakan masukkan kunci untuk mulai.")

api_key = st.text_input("Masukkan Google API Key di sini:", type="password")

# ==========================================
# FITUR MEMORI: Bikin tempat nyimpen obrolan
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if api_key:
    client = genai.Client(api_key=api_key)
    
    # ==========================================
    # FITUR PERSONA: Setting kepribadian AI
    # ==========================================
    karakter_ai = """
    Kamu adalah Efti-Bot, asisten pribadi Eftiara yang super gaul, ramah, dan pintar. 
    Kamu selalu memanggil pengguna dengan sapaan 'Bro' atau 'Sis'. 
    Gunakan gaya bahasa santai ala anak Jakarta, tapi tetap sopan. 
    Selalu gunakan emoji yang seru di setiap jawabanmu!
    """
    
    st.write("---")
    uploaded_file = st.file_uploader("📷 Kirim gambar ke AI (Opsional):", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Gambar siap dianalisis", use_container_width=True)
    
    # Tampilkan semua riwayat chat dari memori
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    # Kolom ketik chat
    prompt = st.chat_input("Tanya apa saja ke Efti-Bot...")
    
    if prompt:
        # Simpan pertanyaan user ke memori dan tampilkan di layar
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        with st.spinner("Efti-Bot lagi ngetik nih..."):
            try:
                # Gabungkan semua riwayat chat jadi satu teks buat dikasih ke AI biar dia ingat
                riwayat_obrolan = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                
                if uploaded_file is not None:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[image, riwayat_obrolan],
                        config=types.GenerateContentConfig(system_instruction=karakter_ai)
                    )
                else:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=riwayat_obrolan,
                        config=types.GenerateContentConfig(system_instruction=karakter_ai)
                    )
                
                # Simpan jawaban AI ke memori dan tampilkan di layar
                st.session_state.messages.append({"role": "ai", "content": response.text})
                st.chat_message("ai").write(response.text)
            except Exception as e:
                st.error(f"Waduh ada error: {e}")
else:
    st.info("👆 Masukkan API Key lu di kolom atas supaya asistennya bangun.")
