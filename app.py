import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# 1. SETUP HALAMAN (Paling Atas)
st.set_page_config(page_title="Asisten Pintar Eftiara", page_icon="🤖", layout="centered")

# 2. CUSTOM TAMPILAN (CSS biar Cerah & Jelas)
st.markdown(
    """
    <style>
    /* Background Putih Bersih */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Warna Teks Hitam Jelas */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        color: #000000 !important;
    }
    
    /* Rapihin Kotak Input Chat biar kelihatan */
    .stChatInput {
        border: 2px solid #DDDDDD !important;
        border-radius: 10px !important;
    }
    
    /* Bikin Judul & Gambar jadi satu baris rapi */
    .header-container {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    .header-container img {
        margin-right: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. HEADER DENGAN GAMBAR LUCU
st.markdown(
    """
    <div class="header-container">
        <img src="https://img.icons8.com/fluent/96/robot-3.png" width="80" alt="Cute Robot"/>
        <h1>Asisten Pintar Eftiara</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# 4. HALAMAN UTAMA & INPUT API KEY (Kembali ke Atas)
st.write("Selamat datang! Asisten unyu ini siap membantu, membaca gambar, dan melukis untukmu.")

st.markdown("---")
st.write("🔧 **Pengaturan:** Masukkan kunci rahasia lu di bawah ini untuk mengaktifkan AI.")
api_key = st.text_input("Google API Key:", type="password", help="Dapatkan kunci di Google AI Studio")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

if api_key:
    client = genai.Client(api_key=api_key)
    
    karakter_ai = """
    Kamu adalah Efti-Bot, asisten pribadi Eftiara yang super gaul, ramah, dan lucu. 
    Selalu panggil pengguna dengan 'Bro' atau 'Sis'. Gunakan emoji unyu!
    """
    
    uploaded_file = st.file_uploader("📷 Upload gambar untuk dianalisis (Opsional):", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_user = Image.open(uploaded_file)
        st.image(image_user, caption="Gambar siap dianalisis", width=300)
    
    # Menampilkan riwayat chat dan gambar dari memori
    for msg in st.session_state.messages:
        if msg["role"] == "ai_image":
            st.image(msg["content"], caption="Hasil lukisan Efti-Bot")
        else:
            st.chat_message(msg["role"]).write(msg["content"])
    
    # Kolom input chat bawaan Streamlit
    prompt = st.chat_input("Tanya apa saja atau ketik 'Gambar: [deskripsi]'...")
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        with st.spinner("Efti-Bot lagi kerja keras..."):
            try:
                # Logika Fitur 3: Bikin Gambar (Text-to-Image)
                if prompt.lower().startswith("gambar:"):
                    deskripsi = prompt[7:].strip()
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
                    # Logika Fitur 1 & 2: Chat biasa & Baca gambar (Vision) + Mengingat riwayat
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
    st.info("👆 Masukkan API Key lu di kolom atas supaya asisten unyu ini bangun.")
