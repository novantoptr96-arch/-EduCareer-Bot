import streamlit as st
from google import genai
from google.genai import types

# =============================
# KONFIGURASI HALAMAN
# =============================
st.set_page_config(
    page_title="EduCareer Bot",
    page_icon="🤖",
    layout="centered"
)

# =============================
# FUNGSI UTAMA GEMINI
# =============================
def get_gemini_client():
    """Membuat client Gemini dari Streamlit Secrets."""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except KeyError:
        st.error(
            "GEMINI_API_KEY belum ditemukan. Isi dulu file .streamlit/secrets.toml "
            "atau masukkan Secrets di Streamlit Cloud."
        )
        st.stop()

    return genai.Client(api_key=api_key)


def build_system_instruction(domain, style, detail_level, coach_mode):
    """Membuat instruksi perilaku chatbot sesuai parameter kreatif."""
    coach_instruction = (
        "Gunakan gaya coach: beri arahan bertahap, koreksi jawaban user, "
        "dan berikan contoh jawaban yang lebih baik."
        if coach_mode
        else "Berikan jawaban langsung, jelas, dan praktis."
    )

    return f"""
Kamu adalah EduCareer Bot, chatbot AI berbahasa Indonesia.
Use case utama kamu adalah membantu pengguna belajar, mempersiapkan karier, dan latihan interview.

Domain fokus: {domain}
Gaya bahasa: {style}
Level detail: {detail_level}
Mode coaching: {coach_instruction}

Aturan jawaban:
1. Jawab dalam bahasa Indonesia yang natural.
2. Buat jawaban praktis dan mudah dipahami.
3. Jika user latihan interview, gunakan metode STAR jika cocok.
4. Jika user bertanya warehouse/logistik, hubungkan dengan akurasi stok, picking, packing, scanner barcode, safety, 5R/5S, dan teamwork.
5. Jangan mengarang pengalaman pribadi user. Jika perlu, berikan template yang bisa disesuaikan.
6. Jika pertanyaan berisiko tinggi seperti medis, hukum, atau finansial, beri arahan umum dan sarankan konsultasi profesional.
"""


def make_prompt_with_memory(system_instruction, messages, user_message):
    """Menggabungkan system instruction, memory chat, dan pesan terbaru."""
    conversation_text = ""
    for msg in messages[-8:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation_text += f"{role}: {msg['content']}\n"

    return f"""
{system_instruction}

Riwayat percakapan terbaru:
{conversation_text}

Pesan user terbaru:
User: {user_message}

Jawaban assistant:
"""


def ask_gemini(client, prompt, model, temperature, max_output_tokens):
    """Mengirim prompt ke Gemini dan mengambil jawaban teks."""
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )
    return response.text


# =============================
# SESSION STATE
# =============================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0


# =============================
# SIDEBAR PARAMETER KREATIF
# =============================
st.sidebar.title("⚙️ Konfigurasi Bot")

model = st.sidebar.selectbox(
    "Model Gemini",
    [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.0-flash",
    ],
    index=0,
)

domain = st.sidebar.selectbox(
    "Domain Pengetahuan",
    [
        "Karier dan Interview Kerja",
        "Warehouse dan Logistik",
        "Belajar Bahasa Inggris Kerja",
        "Produktivitas Personal",
        "Customer Service",
        "Administrasi dan HRD",
        "Finance",
        "Edukasi Umum",
    ],
)

style = st.sidebar.radio(
    "Gaya Bahasa",
    ["Formal", "Santai", "Motivator"],
    index=1,
)

detail_level = st.sidebar.slider(
    "Level Detail Jawaban",
    min_value=1,
    max_value=5,
    value=3,
    help="1 = sangat singkat, 5 = sangat detail"
)

temperature = st.sidebar.slider(
    "Kreativitas / Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.6,
    step=0.1,
)

max_output_tokens = st.sidebar.slider(
    "Panjang Maksimal Jawaban",
    min_value=256,
    max_value=2048,
    value=1024,
    step=128,
)

coach_mode = st.sidebar.toggle("Mode Coaching Aktif", value=True)
use_memory = st.sidebar.toggle("Gunakan Memory Percakapan", value=True)

if st.sidebar.button("🧹 Reset Chat"):
    st.session_state.messages = []
    st.session_state.total_questions = 0
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(
    "Bot ini menggunakan Gemini API. Simpan API key di `.streamlit/secrets.toml` "
    "dengan nama `GEMINI_API_KEY`."
)


# =============================
# TAMPILAN UTAMA
# =============================
st.title("🤖 EduCareer Bot")
st.caption("Chatbot AI berbasis Google Gemini untuk belajar, karier, dan latihan interview.")

with st.expander("📌 Tentang Use Case & Fitur"):
    st.markdown(
        """
        **Use Case:** Education & Career Assistant  
        Chatbot ini membantu pengguna untuk:
        - Latihan interview kerja
        - Belajar skill 
        - Membuat jawaban HRD yang lebih profesional
        - Belajar Bahasa Inggris kerja
        - Membuat rencana belajar atau produktivitas

        **Parameter Kreatif:**
        - Pilihan domain pengetahuan
        - Gaya bahasa formal/santai/motivator
        - Level detail jawaban
        - Temperature untuk mengatur kreativitas
        - Memory percakapan
        - Mode coaching
        """
    )

# Rekomendasi prompt cepat
st.markdown("### 🚀 Contoh Prompt Cepat")
col1, col2 = st.columns(2)

with col1:
    if st.button("Latihan interview"):
        st.session_state.quick_prompt = "Tolong latih saya interview. Berikan pertanyaan dan koreksi jawaban saya."
    if st.button("Buat jawaban perkenalan diri"):
        st.session_state.quick_prompt = "Buatkan jawaban perkenalan diri untuk interview kerja."

with col2:
    if st.button("Belajar menjadi admin"):
        st.session_state.quick_prompt = "Jelaskan cara kerja admin dan contoh penggunaannya."
    if st.button("Rencana belajar 7 hari"):
        st.session_state.quick_prompt = "Buatkan rencana belajar 7 hari untuk meningkatkan skill."

# Tampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input user
quick_prompt = st.session_state.pop("quick_prompt", None) if "quick_prompt" in st.session_state else None
user_input = quick_prompt or st.chat_input("Tulis pertanyaan kamu di sini...")

if user_input:
    st.session_state.total_questions += 1

    with st.chat_message("user"):
        st.markdown(user_input)

    client = get_gemini_client()
    system_instruction = build_system_instruction(domain, style, detail_level, coach_mode)

    if use_memory:
        prompt = make_prompt_with_memory(system_instruction, st.session_state.messages, user_input)
    else:
        prompt = f"{system_instruction}\n\nUser: {user_input}\nAssistant:"

    with st.chat_message("assistant"):
        with st.spinner("Gemini sedang membuat jawaban..."):
            try:
                answer = ask_gemini(
                    client=client,
                    prompt=prompt,
                    model=model,
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                )
                st.markdown(answer)
            except Exception as e:
                answer = f"Terjadi error saat memanggil Gemini API: {e}"
                st.error(answer)

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": answer})


# =============================
# PANEL STATISTIK & EXPORT
# =============================
st.markdown("---")
st.subheader("📊 Statistik Sesi")

col_a, col_b = st.columns(2)
col_a.metric("Jumlah Pertanyaan", st.session_state.total_questions)
col_b.metric("Jumlah Pesan", len(st.session_state.messages))

if st.session_state.messages:
    chat_export = "\n\n".join(
        [f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages]
    )
    st.download_button(
        label="⬇️ Download Riwayat Chat (.txt)",
        data=chat_export,
        file_name="riwayat_chat_educareer.txt",
        mime="text/plain",
    )
