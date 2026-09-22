import requests
import streamlit as st

# ---------- Backend URL ----------
BACKEND_URL = "https://verba-translator.onrender.com/chain/invoke"

# ---------- Languages ----------
LANGUAGES = {
    "🇫🇷 French": "French",
    "🇪🇸 Spanish": "Spanish",
    "🇩🇪 German": "German",
    "🇮🇹 Italian": "Italian",
    "🇵🇹 Portuguese": "Portuguese",
    "🇷🇺 Russian": "Russian",
    "🇯🇵 Japanese": "Japanese",
    "🇰🇷 Korean": "Korean",
    "🇨🇳 Chinese": "Chinese",
    "🇸🇦 Arabic": "Arabic",
    "🇮🇳 Hindi": "Hindi",
    "🇧🇩 Bengali": "Bengali",
    "🇺🇷 Urdu": "Urdu",
    "🇹🇷 Turkish": "Turkish",
    "🇳🇱 Dutch": "Dutch",
    "🇸🇪 Swedish": "Swedish",
    "🇵🇱 Polish": "Polish",
    "🇬🇷 Greek": "Greek",
    "🇹🇭 Thai": "Thai",
    "🇻🇳 Vietnamese": "Vietnamese",
    "🇮🇩 Indonesian": "Indonesian",
    "🇮🇱 Hebrew": "Hebrew",
    "🇺🇦 Ukrainian": "Ukrainian",
    "🇷🇴 Romanian": "Romanian",
    "🇨🇿 Czech": "Czech",
}


def get_groq_response(input_text, language="French"):
    json_body = {
        "input": {"language": language, "text": input_text},
        "config": {},
        "kwargs": {},
    }
    try:
        response = requests.post(BACKEND_URL, json=json_body, timeout=30)

        print("=" * 60)
        print("STATUS:", response.status_code)
        print("RAW:", repr(response.text))
        print("=" * 60)

        if not response.text.strip():
            return {"error": "Empty response from server"}
        if response.status_code != 200:
            return {"error": f"Server error ({response.status_code})",
                    "detail": response.text}
        data = response.json()
        return data.get("output", data) if isinstance(data, dict) else data
    except requests.exceptions.ConnectionError:
        return {"error": "Backend offline", "hint": "Run `python serve.py`"}
    except Exception as e:
        return {"error": str(e)}


# ---------- Page Config ----------
st.set_page_config(
    page_title="Verba — Translator",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- CSS ----------
st.markdown("""
<style>
    .stApp {
        background: #FAFAF7;
        font-family: 'Georgia', 'Times New Roman', serif;
    }
    .masthead {
        text-align: center;
        padding: 2rem 0 0.5rem 0;
        border-bottom: 3px double #1F2937;
        margin-bottom: 1.5rem;
    }
    .masthead h1 {
        font-family: 'Georgia', serif;
        font-size: 3.2rem;
        font-weight: 900;
        letter-spacing: -2px;
        color: #1F2937;
        margin: 0;
    }
    .masthead .tagline {
        font-family: 'Helvetica', sans-serif;
        font-size: 0.85rem;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: #9CA3AF;
        margin-top: 0.5rem;
    }
    .ribbon {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.4rem;
        padding: 1rem 0;
        border-bottom: 1px solid #E5E7EB;
        margin-bottom: 2rem;
    }
    .ribbon span {
        font-family: 'Helvetica', sans-serif;
        font-size: 0.8rem;
        padding: 0.3rem 0.8rem;
        background: #F3F4F6;
        color: #374151;
        border-radius: 4px;
        border: 1px solid #E5E7EB;
    }
    .ribbon span.active {
        background: #1F2937;
        color: #FBBF24;
        border-color: #1F2937;
        font-weight: 700;
    }
    .panel-label {
        font-family: 'Helvetica', sans-serif;
        font-size: 0.7rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #6B7280;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }

    /* Input textarea */
    .stTextArea textarea {
        min-height: 320px !important;
        height: 320px !important;
        font-family: 'Georgia', serif !important;
        font-size: 1.15rem !important;
        line-height: 1.6 !important;
        background: #FFFFFF !important;
        border: 2px solid #1F2937 !important;
        border-radius: 4px !important;
        color: #1F2937 !important;
        padding: 1rem !important;
        resize: none !important;
    }
    .stTextArea textarea:focus {
        border-color: #F59E0B !important;
        box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.15) !important;
    }

    /* Output display box (custom HTML div) */
    .output-box {
        min-height: 320px;
        height: 320px;
        font-family: 'Georgia', serif;
        font-size: 1.15rem;
        line-height: 1.6;
        background: #FFFBEB;
        border: 2px solid #1F2937;
        border-radius: 4px;
        color: #1F2937;
        padding: 1rem;
        box-sizing: border-box;
        overflow-y: auto;
        white-space: pre-wrap;
    }
    .output-box.empty {
        color: #9CA3AF;
        font-style: italic;
    }

    .stButton>button {
        font-family: 'Helvetica', sans-serif;
        background: #1F2937;
        color: #FBBF24;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-size: 0.85rem;
        border-radius: 4px;
        border: none;
        padding: 0.9rem 2rem;
        width: 100%;
        transition: 0.15s;
    }
    .stButton>button:hover {
        background: #F59E0B;
        color: #1F2937;
    }

    .stSelectbox label {
        font-family: 'Helvetica', sans-serif !important;
        font-size: 0.7rem !important;
        letter-spacing: 3px !important;
        text-transform: uppercase !important;
        color: #6B7280 !important;
        font-weight: 700 !important;
    }

    .footer {
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        font-size: 0.75rem;
        color: #9CA3AF;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Masthead ----------
st.markdown("""
<div class="masthead">
    <h1>VERBA</h1>
    <div class="tagline">A Translator's Companion</div>
</div>
""", unsafe_allow_html=True)

# ---------- Language Selector ----------
selected_label = st.selectbox(
    "Choose a language",
    list(LANGUAGES.keys()),
    index=0,
    label_visibility="collapsed",
)
target_language = LANGUAGES[selected_label]

# Ribbon
ribbon_html = '<div class="ribbon">'
for label in LANGUAGES.keys():
    active = " active" if label == selected_label else ""
    ribbon_html += f'<span class="{active.strip()}">{label}</span>'
ribbon_html += "</div>"
st.markdown(ribbon_html, unsafe_allow_html=True)

# ---------- Session State ----------
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

# ---------- Two Equal Panels ----------
left, right = st.columns(2, gap="large")

with left:
    st.markdown('<div class="panel-label">Original</div>', unsafe_allow_html=True)
    source_text = st.text_area(
        "Source",
        placeholder="Type or paste your text here...",
        label_visibility="collapsed",
        height=320,
        key="source_input_widget",
    )

with right:
    st.markdown(
        f'<div class="panel-label">Translation — {selected_label}</div>',
        unsafe_allow_html=True,
    )
    # ✅ Output box as custom HTML div — no Streamlit widget state issues
    translated = st.session_state.translated_text
    if translated:
        st.markdown(
            f'<div class="output-box">{translated}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="output-box empty">Translation will appear here...</div>',
            unsafe_allow_html=True,
        )

# ---------- Translate Button ----------
st.write("")
_, btn_col, _ = st.columns([1, 1, 1])
with btn_col:
    translate = st.button("Translate ➜", use_container_width=True)

if translate:
    if not source_text.strip():
        st.warning("Please type something to translate.")
    else:
        with st.spinner("Translating..."):
            result = get_groq_response(source_text, target_language)

        if isinstance(result, dict) and "error" in result:
            st.error(f"⚠️ {result['error']}")
            if "hint" in result:
                st.info(result["hint"])
            if "detail" in result:
                st.code(result["detail"])
        else:
            # ✅ Update session state, then rerun
            st.session_state.translated_text = result
            st.rerun()

# ---------- Footer ----------
st.markdown(
    '<div class="footer">Groq · LangChain · FastAPI · Streamlit</div>',
    unsafe_allow_html=True,
)