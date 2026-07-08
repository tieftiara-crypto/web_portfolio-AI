import streamlit as st
from google import genai
from PIL import Image

st.title("🤖 Asisten Pintar Eftiara")
st.write("Selamat datang di portofolio AI buatan Eftiara! Silakan masukkan kunci untuk mulai.")

api_key = st.text_input("Masukkan Google API Key di sini:", type="password")

if api_key:
    # Bangunin AI-nya
    client = genai.Client(api_key=api_key)
    
    # Fitur upload gambar
    st.write("---")
    uploaded_file = st.file_uploader("📷 Kirim gambar ke AI (Opsional):", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Gambar siap dianalisis", use_container_width=True)
    
    # Kolom chat
    prompt = st.chat_input("Tanya apa saja atau suruh AI jelaskan gambar di atas...")
    
    if prompt:
        st.chat_message("user").write(prompt)
        
        with st.spinner("Asisten sedang berpikir..."):
            try:
                if uploaded_file is not None:
                    # Kalau nanya pakai gambar
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[image, prompt]
                    )
                else:
                    # Kalau cuma nanya teks biasa
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt
                    )
                st.chat_message("ai").write(response.text)
            except Exception as e:
                st.error(f"Waduh ada error: {e}")
else:
    st.info("👆 Masukkan API Key lu di kolom atas supaya asistennya bangun.")
