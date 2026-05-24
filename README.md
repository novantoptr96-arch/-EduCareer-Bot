# EduCareer Gemini Bot

Chatbot AI berbasis Streamlit dan Google Gemini API.

## Use Case

Education & Career Assistant untuk:

- Latihan interview kerja
- Belajar skill warehouse/logistik
- Membuat jawaban HRD
- Belajar Bahasa Inggris kerja
- Membuat rencana belajar dan produktivitas

## Fitur

- Streamlit chat UI
- Google Gemini API
- Pilihan model Gemini
- Pilihan domain pengetahuan
- Gaya bahasa formal/santai/motivator
- Level detail jawaban
- Temperature
- Memory percakapan
- Mode coaching
- Download riwayat chat

## Cara Menjalankan Lokal

1. Install Python.
2. Buka terminal di folder project.
3. Install dependency:

```bash
py -m pip install -r requirements.txt
```

4. Copy file secret:

```bash
copy .streamlit\secrets.example.toml .streamlit\secrets.toml
```

5. Isi `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "API_KEY_GEMINI_KAMU"
```

6. Jalankan aplikasi:

```bash
py -m streamlit run app.py
```

## Deploy ke Streamlit Cloud

1. Upload project ke GitHub.
2. Buka Streamlit Community Cloud.
3. Create app dari repository GitHub.
4. Main file path: `app.py`.
5. Isi Secrets:

```toml
GEMINI_API_KEY = "API_KEY_GEMINI_KAMU"
```

6. Deploy.

## Catatan Keamanan

Jangan upload file `.streamlit/secrets.toml` ke GitHub.
