import streamlit as st
from google import genai

st.set_page_config(page_title="Web AI Eftiara", page_icon="🤖")

st.title("🤖 Asisten Pintar Eftiara")
st.write("Selamat datang di portofolio AI buatan Eftiara! Silakan masukkan kunci untuk mulai.")

# Trik aman: Minta API Key lewat tampilan web (jadi kode lu 100% aman ditaruh di mana aja!)
api_key = st.text_input("Masukkan Google API Key di sini:", type="password")

if api_key:
    klien_ai = genai.Client(api_key=api_key)
    
    user_input = st.chat_input("Tanya apa saja ke asisten ini...")
    
    if user_input:
        # Menampilkan pertanyaan lu
        st.chat_message("user").write(user_input)
        
        # Menampilkan jawaban AI
        with st.chat_message("assistant"):
            try:
                respons = klien_ai.models.generate_content(
                    model='gemini-2.5-flash', 
                    contents=user_input
                )
                st.write(respons.text)
            except Exception as e:
                st.error("Waduh, ada yang error. Coba cek lagi API Key-nya udah bener belum ya?")
else:
    st.info("👆 Masukkan API Key lu di kolom atas supaya asistennya bangun.")