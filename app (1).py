import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import base64

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌐",
    layout="centered"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f0f4ff; }
    .stTextArea textarea {
        font-size: 16px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-size: 16px;
        width: 100%;
        border: none;
    }
    .stButton>button:hover {
        background-color: #4338ca;
    }
    .result-box {
        background-color: #ffffff;
        border-left: 5px solid #4f46e5;
        padding: 16px 20px;
        border-radius: 10px;
        font-size: 18px;
        margin-top: 10px;
    }
    h1 { color: #1e1b4b; }
</style>
""", unsafe_allow_html=True)

# ─── Language List ─────────────────────────────────────────────────────────────
LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Bengali (Bangla)": "bn",
    "Hindi": "hi",
    "Arabic": "ar",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Portuguese": "pt",
    "Russian": "ru",
    "Turkish": "tr",
    "Italian": "it",
    "Urdu": "ur",
}

TTS_SUPPORTED = ["en", "bn", "hi", "ar", "fr", "es", "de", "zh-CN", "ja", "ko", "pt", "ru", "tr", "it", "ur"]

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🌐 AI Language Translator")
st.markdown("**CodeAlpha AI Internship — Task 1** | Built with Python & Streamlit")
st.divider()

# ─── Input Section ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("🔤 Source Language", list(LANGUAGES.keys()), index=0)
with col2:
    target_lang = st.selectbox("🎯 Target Language", list(LANGUAGES.keys()), index=2)

input_text = st.text_area("✍️ Enter text to translate:", height=160, placeholder="Type your text here...")

# ─── Translate Button ──────────────────────────────────────────────────────────
if st.button("🚀 Translate Now"):
    if not input_text.strip():
        st.warning("⚠️ Please enter some text first.")
    elif LANGUAGES[source_lang] == LANGUAGES[target_lang] and source_lang != "Auto Detect":
        st.info("ℹ️ Source and target languages are the same.")
    else:
        with st.spinner("Translating..."):
            try:
                translated = GoogleTranslator(
                    source=LANGUAGES[source_lang],
                    target=LANGUAGES[target_lang]
                ).translate(input_text)

                st.success("✅ Translation Complete!")
                st.markdown("### 📝 Translated Text:")
                st.markdown(f'<div class="result-box">{translated}</div>', unsafe_allow_html=True)

                # ── Copy button ───────────────────────────────────────────────
                st.code(translated, language=None)
                st.caption("👆 Click the copy icon above to copy translated text")

                # ── Text-to-Speech ────────────────────────────────────────────
                target_code = LANGUAGES[target_lang]
                if target_code in TTS_SUPPORTED and target_code != "auto":
                    st.markdown("### 🔊 Listen to Translation:")
                    try:
                        tts = gTTS(text=translated, lang=target_code)
                        audio_path = "/tmp/translation_audio.mp3"
                        tts.save(audio_path)
                        with open(audio_path, "rb") as f:
                            audio_bytes = f.read()
                        st.audio(audio_bytes, format="audio/mp3")
                    except Exception:
                        st.caption("Audio not available for this language.")

            except Exception as e:
                st.error(f"❌ Translation failed: {str(e)}")

# ─── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<center><small>Made by <b>Md. Limon Hossen</b> | CodeAlpha AI Internship 🤖</small></center>",
    unsafe_allow_html=True
)
