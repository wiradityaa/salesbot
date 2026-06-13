import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import streamlit as st

from agents.intent_classifier import classify_intent
from agents.tool_router import route
from agents.response_generator import generate_response

st.set_page_config(
    page_title="SalesBot AI",
    page_icon="🤖",
    layout="wide"
)

# =====================================
# CSS — match dashboard style exactly
# =====================================

st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main, .stApp {
    background-color: #0f172a !important;
    color: #e2e8f0 !important;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

[data-testid="stSidebar"] {
    background: #0a1120 !important;
}

[data-testid="stSidebar"] * {
    color: #94a3b8 !important;
}

[data-testid="stHeader"] {
    background: transparent;
}

/* Quick question buttons */
div[data-testid="stButton"] > button {
    background: #1e293b;
    border: 1px solid #334155;
    color: #cbd5e1;
    border-radius: 8px;
    font-size: 0.88rem;
    transition: all 0.15s ease;
}

div[data-testid="stButton"] > button:hover {
    background: #334155;
    border-color: #475569;
    color: #f1f5f9;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: #1e293b !important;
    border-color: #334155 !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: #1e293b !important;
    border: 1px solid #1e293b;
    border-radius: 12px;
}

/* Divider */
hr {
    border-color: #1e293b !important;
}

/* st.info box */
[data-testid="stAlert"] {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    color: #94a3b8 !important;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversations" not in st.session_state:
    st.session_state.conversations = []

if "active_conv_idx" not in st.session_state:
    st.session_state.active_conv_idx = None

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    # Logo + title
    st.markdown(
        "<div style='display:flex;align-items:center;gap:0.6rem;margin-bottom:0.25rem;'>"
        "<span style='font-size:1.4rem;'>🤖</span>"
        "<div>"
        "<p style='color:#f1f5f9;font-size:1.05rem;font-weight:700;margin:0;'>SalesBot</p>"
        "<p style='color:#475569;font-size:0.75rem;margin:0;'>AI Assistant</p>"
        "</div></div>",
        unsafe_allow_html=True
    )

    st.markdown("<hr style='border-color:#1e293b;margin:0.75rem 0;'>",
                unsafe_allow_html=True)

    # New Conversation
    if st.button("➕ New Conversation", use_container_width=True, type="primary"):
        if st.session_state.messages:
            first_msg = st.session_state.messages[0]["content"]
            title = first_msg[:28] + "..." if len(first_msg) > 28 else first_msg
            st.session_state.conversations.insert(0, {
                "title": title,
                "time": "now",
                "messages": st.session_state.messages.copy()
            })
        st.session_state.messages = []
        st.session_state.active_conv_idx = None
        st.rerun()

    st.markdown("<hr style='border-color:#1e293b;margin:0.75rem 0;'>",
                unsafe_allow_html=True)

    # Recent conversations
    st.markdown(
        "<p style='color:#475569;font-size:0.72rem;text-transform:uppercase;"
        "letter-spacing:0.08em;margin:0 0 0.6rem 0;'>Recent Conversations</p>",
        unsafe_allow_html=True
    )

    if st.session_state.conversations:
        for i, conv in enumerate(st.session_state.conversations):
            col_t, col_time = st.columns([3, 1])
            with col_t:
                if st.button(conv["title"], key=f"conv_{i}",
                             use_container_width=True):
                    st.session_state.messages = conv["messages"].copy()
                    st.session_state.active_conv_idx = i
                    st.rerun()
            with col_time:
                st.markdown(
                    f"<p style='color:#334155;font-size:0.68rem;"
                    f"padding-top:9px;'>{conv['time']}</p>",
                    unsafe_allow_html=True
                )
    else:
        st.markdown(
            "<p style='color:#334155;font-size:0.82rem;'>No conversations yet.</p>",
            unsafe_allow_html=True
        )

    st.markdown("<hr style='border-color:#1e293b;margin:0.75rem 0;'>",
                unsafe_allow_html=True)

    if st.button("🗑 Clear Conversations", use_container_width=True):
        st.session_state.conversations = []
        st.session_state.messages = []
        st.session_state.active_conv_idx = None
        st.rerun()

    st.markdown("<hr style='border-color:#1e293b;margin:0.75rem 0;'>",
                unsafe_allow_html=True)

    st.markdown(
        "<p style='color:#22c55e;font-size:0.82rem;margin:0;'>● Data Source</p>"
        "<p style='color:#475569;font-size:0.78rem;margin:0;'>Supabase</p>",
        unsafe_allow_html=True
    )

# =====================================
# HEADER
# =====================================

st.markdown(
    "<div style='display:flex;align-items:center;gap:0.75rem;margin-bottom:0.25rem;'>"
    "<span style='font-size:1.6rem;'>🤖</span>"
    "<div>"
    "<h2 style='color:#f1f5f9;margin:0;font-size:1.6rem;font-weight:700;"
    "display:inline;'>SalesBot</h2>"
    "&nbsp;<span style='color:#475569;font-size:0.95rem;font-weight:400;'>"
    "AI-powered retail analytics assistant</span>"
    "</div></div>",
    unsafe_allow_html=True
)

st.markdown("<hr style='border-color:#1e293b;margin:0.5rem 0 1rem 0;'>",
            unsafe_allow_html=True)

# =====================================
# MAIN — Two columns
# =====================================

left_col, right_col = st.columns([1, 3])

# ---- Left: Quick Questions + AI Insights ----
with left_col:

    st.markdown(
        "<p style='color:#f1f5f9;font-size:1rem;font-weight:600;"
        "margin:0 0 0.75rem 0;'>⚡ Quick Questions</p>",
        unsafe_allow_html=True
    )

    quick_questions = [
        "Produk apa yang paling laris?",
        "Provinsi mana revenue tertinggi?",
        "Kategori paling menguntungkan?",
        "Metode pembayaran terbaik?",
        "Tampilkan tren revenue bulanan",
        "Berikan rekomendasi bisnis",
    ]

    for q in quick_questions:
        if st.button(q, use_container_width=True, key=f"qq_{q}"):
            st.session_state.quick_question = q

    st.markdown("<hr style='border-color:#1e293b;margin:1rem 0;'>",
                unsafe_allow_html=True)

    # AI Insights card — styled like dashboard
    st.markdown(
        "<p style='color:#f1f5f9;font-size:1rem;font-weight:600;"
        "margin:0 0 0.75rem 0;'>📊 AI Insights</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='background:#1e293b;border:1px solid #334155;"
        "border-radius:12px;padding:1rem 1.2rem;'>"
        "<p style='color:#475569;font-size:0.72rem;text-transform:uppercase;"
        "letter-spacing:0.08em;margin:0 0 0.75rem 0;'>SalesBot dapat membantu</p>"
        "<div style='display:flex;flex-direction:column;gap:0.5rem;'>"
        + "".join([
            f"<div style='display:flex;align-items:center;gap:0.5rem;'>"
            f"<span style='color:#3b82f6;font-size:0.7rem;'>●</span>"
            f"<span style='color:#94a3b8;font-size:0.85rem;'>{item}</span>"
            f"</div>"
            for item in [
                "Analisis Produk",
                "Analisis Provinsi",
                "Analisis Kategori",
                "Analisis Payment",
                "Tren Penjualan",
                "Rekomendasi Bisnis",
            ]
        ])
        + "</div></div>",
        unsafe_allow_html=True
    )

# ---- Right: Chat ----
with right_col:

    # Chat header
    chat_left, chat_right = st.columns([5, 1])

    with chat_left:
        st.markdown(
            "<p style='color:#f1f5f9;font-size:1.05rem;font-weight:600;"
            "margin:0;'>🤖 SalesBot AI Assistant</p>"
            "<p style='color:#475569;font-size:0.82rem;margin:0;'>"
            "Tanyakan apa saja tentang data penjualan retail</p>",
            unsafe_allow_html=True
        )

    with chat_right:
        if st.button("🗑 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown("<hr style='border-color:#1e293b;margin:0.75rem 0;'>",
                unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    prompt = st.chat_input("Tanyakan sesuatu tentang data penjualan...")

    if "quick_question" in st.session_state:
        prompt = st.session_state.quick_question
        del st.session_state.quick_question

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Menganalisis data..."):
                try:
                    intent = classify_intent(prompt)
                    result = route(intent["data"])
                    answer = generate_response(prompt, result, intent["data"])
                except Exception as e:
                    answer = (
                        "Maaf, terjadi kesalahan saat memproses pertanyaan Anda. "
                        f"Silakan coba lagi.\n\n_Error: {e}_"
                    )
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

        if len(st.session_state.messages) == 2:
            first_msg = st.session_state.messages[0]["content"]
            title = first_msg[:28] + "..." if len(first_msg) > 28 else first_msg
            st.session_state.conversations.insert(0, {
                "title": title,
                "time": "now",
                "messages": st.session_state.messages.copy()
            })

        st.rerun()