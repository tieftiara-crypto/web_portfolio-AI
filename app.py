import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io

st.title("🤖 Asisten Pintar Eftiara")
st.write("Selamat datang! AI ini bisa Chat, Baca Gambar, dan **BIKIN Gambar!**")

api_key = st.text_input("Masukkan Google API Key di sini:", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = []

if api_key:
    client = genai.Client(api_key=api_key)
    
    karakter_ai = """
    Kamu adalah Efti-Bot, asisten pribadi Eftiara yang super gaul dan ramah. 
    Selalu panggil pengguna dengan 'Bro' atau 'Sis'. Gunakan emoji seru!
    """
    
    st.write("---")
    st.info("💡 **Tips:** Kalau mau suruh AI bikin gambar, ketik awalan 'Gambar:' (Contoh: *Gambar: kucing pakai kacamata*)")
    
    uploaded_file = st.file_uploader("📷 Kirim gambar ke AI (Opsional):", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_user = Image.open(uploaded_file)
        st.image(image_user, caption="Gambar siap dianalisis", use_container_width=True)
    
    # Tampilkan memori chat dan gambar
    for msg in st.session_state.messages:
        if msg["role"] == "ai_image":
            st.image(msg["content"])
        else:
            st.chat_message(msg["role"]).write(msg["content"])
    
    prompt = st.chat_input("Tanya apa saja atau suruh AI bikin gambar...")
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        with st.spinner("Efti-Bot lagi kerja keras..."):
            try:
                # Logika sakti: Cek apakah user minta gambar
                if prompt.lower().startswith("gambar:"):
                    deskripsi = prompt[7:].strip()
                    # Perintah AI untuk melukis
                    result = client.models.generate_images(
                        model='imagen-3.0-generate-001',
                        prompt=deskripsi,
                        config=types.GenerateImagesConfig(
                            number_of_images=1,
                            output_mime_type="image/jpeg"
                        )
                    )
                    for generated_image in result.generated_images:
                        image_bytes = generated_image.image.image_bytes
                        st.image(image_bytes, caption=f"Hasil gambar: {deskripsi}")
                        st.session_state.messages.append({"role": "ai_image", "content": image_bytes})
                else:
                    # Chat dan analisa gambar biasa
                    riwayat_obrolan = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages if m['role'] != 'ai_image'])
                    
                    if uploaded_file is not None:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[image_user, riwayat_obrolan],
                            config=types.GenerateContentConfig(system_instruction=karakter_ai)
                        )
                    else:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=riwayat_obrolan,
                            config=types.GenerateContentConfig(system_instruction=karakter_ai)
                        )
                    
                    st.session_state.messages.append({"role": "ai", "content": response.text})
                    st.chat_message("ai").write(response.text)
            except Exception as e:
                st.error(f"Waduh ada error: {e}")
else:
    st.info("👆 Masukkan API Key lu di kolom atas supaya asistennya bangun.")
