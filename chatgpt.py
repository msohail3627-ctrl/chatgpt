
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Load environment variables
load_dotenv(override=True)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MS AI | Custom ChatGPT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "system_role" not in st.session_state:
    st.session_state.system_role = (
        "You are Nova AI, a helpful, friendly, and accurate AI assistant. "
        "Answer clearly and provide examples when useful."
    )

if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""

if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True

if "model_name" not in st.session_state:
    st.session_state.model_name = "gpt-4o-mini"


def get_api_key():
    """Enable chat only after a key is entered on the welcome page."""
    return st.session_state.get("user_api_key", "").strip()


# ---------------- CUSTOM CSS: LIGHT 3D DESIGN ----------------
st.markdown("""
<style>
/* LIGHT 3D BACKGROUND */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section[data-testid="stMain"] {
    color: #17243a !important;
    background-color: #f4f8ff !important;
}

.stApp {
    background-image:
        linear-gradient(
            rgba(104, 133, 186, 0.055) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(104, 133, 186, 0.055) 1px,
            transparent 1px
        ),
        radial-gradient(
            ellipse at 10% 8%,
            rgba(111, 202, 255, 0.40) 0%,
            transparent 34%
        ),
        radial-gradient(
            ellipse at 89% 12%,
            rgba(190, 160, 255, 0.35) 0%,
            transparent 33%
        ),
        radial-gradient(
            ellipse at 75% 88%,
            rgba(133, 235, 218, 0.30) 0%,
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #f8fbff 0%,
            #edf3ff 48%,
            #fbfdff 100%
        ) !important;

    background-size:
        42px 42px,
        42px 42px,
        auto,
        auto,
        auto,
        auto !important;

    background-attachment: fixed !important;
}

/* Transparent main content */
[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
}

header[data-testid="stHeader"] {
    background: rgba(248, 251, 255, 0.72) !important;
}

/* LIGHT SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        155deg,
        #ffffff 0%,
        #f0f5ff 58%,
        #e7efff 100%
    ) !important;
    border-right: 1px solid #d6e2f5 !important;
    box-shadow: 8px 0 30px rgba(36, 65, 116, 0.08);
}

section[data-testid="stSidebar"] * {
    color: #202e46;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #202e46 !important;
}

/* GRADIENT MAIN HEADING */
.main-title {
    text-align: center;
    font-size: clamp(28px, 4vw, 46px);
    font-weight: 850;
    letter-spacing: -0.8px;
    margin-top: 25px;
    background: linear-gradient(
        100deg,
        #1f4e9b 0%,
        #5364de 48%,
        #039bb5 100%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(
        0 4px 8px rgba(44, 87, 165, 0.12)
    );
}

.subtitle {
    text-align: center;
    color: #4d5f7a !important;
    margin: 10px 0 25px 0;
}

/* RAISED 3D WELCOME PANEL */
.welcome {
    position: relative;
    text-align: center;
    padding: 30px 18px;
    margin: 18px 0 24px 0;
    border: 1px solid rgba(189, 207, 239, 0.95);
    border-radius: 26px;

    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(255,255,255,0.98),
            transparent 45%
        ),
        linear-gradient(
            145deg,
            #ffffff 0%,
            #f0f5ff 58%,
            #e8f5ff 100%
        ) !important;

    box-shadow:
        0 22px 42px rgba(42, 69, 119, 0.13),
        0 5px 12px rgba(42, 69, 119, 0.06),
        inset 0 1px 0 rgba(255,255,255,0.98);

    color: #17243a !important;
    transform: perspective(1000px) rotateX(0.5deg);
}

.welcome h2,
.welcome p {
    color: #17243a !important;
}

.robot {
    font-size: 62px;
    margin-bottom: 10px;
    filter: drop-shadow(
        0 10px 8px rgba(52, 91, 179, 0.20)
    );
}

/* FLOATING 3D FEATURE CARDS */
.feature-card {
    position: relative;
    background: linear-gradient(
        145deg,
        #ffffff 0%,
        #f2f6ff 60%,
        #eaf5ff 100%
    ) !important;

    border: 1px solid #d4e1f5;
    border-radius: 20px;
    padding: 20px 14px;
    text-align: center;
    min-height: 118px;

    box-shadow:
        0 14px 28px rgba(39, 68, 122, 0.11),
        0 4px 8px rgba(39, 68, 122, 0.05),
        inset 0 1px 0 #ffffff;

    transition:
        transform 180ms ease,
        box-shadow 180ms ease;
}

.feature-card:hover {
    transform: translateY(-5px) perspective(900px) rotateX(2deg);
    box-shadow:
        0 22px 36px rgba(39, 68, 122, 0.16),
        0 6px 12px rgba(39, 68, 122, 0.07),
        inset 0 1px 0 #ffffff;
}

.feature-card h4 {
    color: #17243a !important;
    margin-bottom: 7px;
}

.feature-card p {
    color: #52637d !important;
    font-size: 13px;
}

/* API KEY AND SIDEBAR INPUT FIELDS */
.stTextInput input,
.stTextArea textarea,
section[data-testid="stSidebar"] textarea {
    background: #ffffff !important;
    color: #17243a !important;
    -webkit-text-fill-color: #17243a !important;
    border: 1px solid #c7d5ea !important;
    border-radius: 12px !important;
    caret-color: #17243a !important;
    box-shadow: inset 0 1px 3px rgba(29, 57, 105, 0.04);
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #687994 !important;
    -webkit-text-fill-color: #687994 !important;
}

/* REMOVE WHITE STRIP UNDER CHAT INPUT */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"],
[data-testid="stBottomBlockContainer"] > div,
[data-testid="stBottomBlockContainer"]::before,
[data-testid="stBottom"]::before {
    background: #f4f8ff !important;
    background-color: #f4f8ff !important;
}

[data-testid="stBottom"] {
    border-top: 0 !important;
}

[data-testid="stBottomBlockContainer"] {
    padding-top: 16px !important;
    padding-bottom: 16px !important;
}

/* BLACK 3D FLOATING CHAT / SEARCH BAR */
[data-testid="stChatInput"] {
    background: #000000 !important;
    background-color: #000000 !important;
    border: 1px solid #3a4c70 !important;
    border-radius: 20px !important;

    box-shadow:
        0 16px 30px rgba(17, 36, 70, 0.26),
        0 4px 0 rgba(32, 61, 112, 0.20),
        inset 0 1px 0 rgba(255,255,255,0.10) !important;

    padding: 5px !important;
}

[data-testid="stChatInput"] > div {
    background: #000000 !important;
    background-color: #000000 !important;
    border: none !important;
    border-radius: 16px !important;
}

[data-testid="stChatInput"] textarea {
    background: #000000 !important;
    background-color: #000000 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #ffffff !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #b8c4d8 !important;
    -webkit-text-fill-color: #b8c4d8 !important;
}

[data-testid="stChatInput"] button {
    background: linear-gradient(
        145deg,
        #64bcff,
        #4758ee
    ) !important;
    color: #ffffff !important;
    border-radius: 14px !important;

    box-shadow: 0 5px 12px rgba(65, 105, 230, 0.35);
}

[data-testid="stChatInput"] button:hover {
    background: linear-gradient(
        145deg,
        #82cbff,
        #5b68ff
    ) !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #718cff !important;
    box-shadow:
        0 0 0 3px rgba(91, 116, 255, 0.13),
        0 16px 30px rgba(17, 36, 70, 0.24) !important;
}

/* RAISED WHITE CHAT MESSAGE PANELS */
[data-testid="stChatMessage"] {
    background: linear-gradient(
        145deg,
        #ffffff,
        #f2f6ff
    ) !important;

    color: #17243a !important;
    border: 1px solid #d9e4f3 !important;
    border-radius: 18px;
    padding: 12px;
    margin-bottom: 12px;

    box-shadow:
        0 7px 18px rgba(38, 63, 106, 0.07),
        inset 0 1px 0 #ffffff;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] code {
    color: #17243a !important;
}

/* 3D BLUE-VIOLET BUTTONS */
.stButton > button,
.stFormSubmitButton > button {
    border-radius: 13px;
    border: 1px solid #b6c8eb;
    background: linear-gradient(
        145deg,
        #eaf2ff,
        #dce8ff
    ) !important;

    color: #203c6c !important;
    padding: 10px;

    box-shadow:
        0 5px 12px rgba(39, 68, 122, 0.09),
        inset 0 1px 0 rgba(255,255,255,0.98);

    transition:
        transform 180ms ease,
        box-shadow 180ms ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-2px);
    border-color: #849fe0;

    background: linear-gradient(
        145deg,
        #dae8ff,
        #cddcff
    ) !important;

    box-shadow: 0 10px 18px rgba(39, 68, 122, 0.14);
}

/* SELECTBOX TEXT */
[data-testid="stSelectbox"] div,
[data-testid="stSelectbox"] input {
    color: #17243a !important;
}

/* FOOTER */
.footer {
    text-align: center;
    color: #61728b !important;
    font-size: 12px;
    padding: 25px 0;
}

/* REDUCE ANIMATIONS WHEN PREFERRED */
@media (prefers-reduced-motion: reduce) {
    .feature-card,
    .stButton > button,
    .stFormSubmitButton > button {
        transition: none !important;
    }

    .feature-card:hover,
    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        transform: none !important;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("# 🤖 Nova AI")
    st.caption("Your Personal AI Assistant")
    st.divider()

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.show_welcome = not bool(get_api_key())
        st.rerun()

    st.markdown("### ⚙️ Personalize AI")

    role_text = st.text_area(
        "AI instructions",
        value=st.session_state.system_role,
        height=130,
        help="Customize how the AI responds.",
    )

    if st.button("🚀 Update Role", use_container_width=True):
        st.session_state.system_role = role_text
        st.success("Instructions updated!")

    st.divider()
    st.markdown("### 🧠 AI Model")

    st.selectbox(
        "Select model",
        ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"],
        key="model_name",
        help="Only models enabled for your API account will work.",
    )

    st.divider()
    st.markdown("### 🔐 API Status")

    if get_api_key():
        st.success("API key available")
    else:
        st.warning("Enter an API key on the welcome page.")

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.show_welcome = True
        st.rerun()


# ---------------- MAIN HEADER ----------------
st.markdown(
    '<div class="main-title">✦ Welcome to Your Custom ChatGPT</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Your personal AI assistant for questions, coding, writing, and learning.'
    '</div>',
    unsafe_allow_html=True,
)


# ---------------- WELCOME PAGE + API KEY ----------------
if st.session_state.show_welcome and not st.session_state.messages:

    st.markdown("""
    <div class="welcome">
        <div class="robot">🤖</div>
        <h2>Welcome to Your Custom ChatGPT</h2>
        <p>
            Add your OpenAI API key and start exploring with Nova AI.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("api_key_form"):
        st.markdown("### 🔐 Connect your OpenAI API key")

        entered_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.user_api_key,
            type="password",
            placeholder="Paste your API key here (sk-...)",
            help="Your key is used for your OpenAI API requests. Keep it private.",
        )

        connect = st.form_submit_button(
            "🔓 Connect to Nova AI",
            use_container_width=True,
        )

        if connect:
            if not entered_key.strip():
                st.error("Please enter your API key.")
            else:
                st.session_state.user_api_key = entered_key.strip()
                st.success(
                    "API key added to this session. Send a message to test it."
                )
                st.rerun()

    st.markdown("#### ✨ What can you do?")

    c1, c2, c3, c4 = st.columns(4)

    features = [
        ("💡 Get Answers", "Ask questions"),
        ("✍️ Create Content", "Write and rewrite"),
        ("💻 Write Code", "Debug programs"),
        ("📚 Learn", "Understand topics"),
    ]

    for col, (heading, description) in zip(
        [c1, c2, c3, c4], features
    ):
        with col:
            st.markdown(
                f'<div class="feature-card">'
                f'<h4>{heading}</h4>'
                f'<p>{description}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ---------------- CHAT HISTORY ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------- BLACK CHAT / SEARCH BAR ----------------
# Chat remains disabled until an API key is entered on the welcome page.
api_key_available = bool(get_api_key())

prompt = st.chat_input(
    "✦ Ask anything..."
    if api_key_available
    else "🔒 Enter your API key above to enable chat...",
    key="nova_black_search",
    disabled=not api_key_available,
)

if prompt:
    api_key = get_api_key()

    # Check again before sending the request.
    if not api_key:
        st.warning("Please enter your OpenAI API key on the welcome page.")
    else:
        st.session_state.show_welcome = False

        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            with st.chat_message("assistant"):
                with st.spinner("Nova AI is thinking..."):

                    llm = ChatOpenAI(
                        model=st.session_state.get(
                            "model_name",
                            "gpt-4o-mini",
                        ),
                        temperature=0.5,
                        api_key=api_key,
                    )

                    chat_messages = [
                        SystemMessage(
                            content=st.session_state.system_role
                        )
                    ]

                    for item in st.session_state.messages:
                        if item["role"] == "user":
                            chat_messages.append(
                                HumanMessage(
                                    content=item["content"]
                                )
                            )
                        elif item["role"] == "assistant":
                            chat_messages.append(
                                AIMessage(
                                    content=item["content"]
                                )
                            )

                    response = llm.invoke(chat_messages)
                    answer = response.content

                    if isinstance(answer, list):
                        answer = "\n".join(
                            str(part.get("text", part))
                            if isinstance(part, dict)
                            else str(part)
                            for part in answer
                        )

                    st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
            })

        except Exception as error:
            # Remove the unanswered question so it can be retried.
            if (
                st.session_state.messages
                and st.session_state.messages[-1]["role"] == "user"
            ):
                st.session_state.messages.pop()

            st.error(f"API request failed: {error}")
            st.info(
                "Check your API key, API billing, model access, "
                "and internet connection."
            )


# ---------------- FOOTER ----------------
st.markdown(
    '<div class="footer">'
    'NOVA AI • BUILT WITH STREAMLIT + LANGCHAIN + OPENAI'
    '</div>',
    unsafe_allow_html=True,
)
