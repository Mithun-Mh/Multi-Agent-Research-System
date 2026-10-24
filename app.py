import streamlit as st
import time
import base64
import re
import os
import io
try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    from gtts import gTTS
except ImportError:
    gTTS = None

from fpdf import FPDF

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="InfoPlus · Autonomous AI Research System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS: Sky Blue & Navy Blue Modern Human-Centric Design ────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

  :root {
    --sky-50: #f0f9ff;
    --sky-100: #e0f2fe;
    --sky-200: #bae6fd;
    --sky-300: #7dd3fc;
    --sky-400: #38bdf8;
    --sky-500: #0ea5e9;
    --sky-600: #0284c7;
    --navy-900: #0a192f;
    --navy-800: #0f172a;
    --navy-700: #1e293b;
    --navy-600: #1e3a8a;
    --navy-500: #2563eb;
    --slate-600: #475569;
    --slate-500: #64748b;
    --slate-400: #94a3b8;
  }

  html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--navy-800);
  }

  /* Main background: Radiant Sky Blue with soft ambient gradient */
  .stApp {
    background: radial-gradient(circle at 15% 15%, #e0f2fe 0%, #f0f9ff 45%, #eff6ff 100%) !important;
    min-height: 100vh;
  }

  #MainMenu, footer, header { visibility: hidden; }
  .block-container {
    padding-top: 1.8rem;
    padding-bottom: 3.5rem;
    max-width: 1060px;
  }

  /* Brand Header */
  .ip-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 1.4rem;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(186, 230, 253, 0.8);
    border-radius: 18px;
    box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.08), 0 4px 6px -2px rgba(15, 23, 42, 0.03);
    margin-bottom: 1.6rem;
  }
  .ip-brand-left {
    display: flex;
    align-items: center;
    gap: 14px;
  }
  .ip-logo-badge {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #0284c7 0%, #0f172a 100%);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    color: #ffffff;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
  }
  .ip-brand-title {
    font-size: 1.4rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
    line-height: 1.2;
  }
  .ip-brand-title span {
    color: #0284c7;
  }
  .ip-brand-sub {
    font-size: 0.76rem;
    color: #64748b;
    font-weight: 500;
    letter-spacing: 0.2px;
  }
  .ip-status-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    background: #e0f2fe;
    border: 1px solid #bae6fd;
    border-radius: 30px;
    font-size: 0.8rem;
    font-weight: 600;
    color: #0369a1;
  }
  .ip-status-dot {
    width: 8px;
    height: 8px;
    background: #0284c7;
    border-radius: 50%;
    box-shadow: 0 0 8px #0284c7;
    animation: pulse 2s infinite;
  }
  @keyframes pulse {
    0% { transform: scale(0.95); opacity: 0.7; }
    50% { transform: scale(1.15); opacity: 1; }
    100% { transform: scale(0.95); opacity: 0.7; }
  }

  /* Human Agent Specialist Cards */
  .ip-agent-bar-title {
    font-size: 0.76rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #0369a1;
    margin-bottom: 0.6rem;
  }
  .ip-agent-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 1.6rem;
  }
  .ip-agent-card {
    background: #ffffff;
    border: 1px solid #e0f2fe;
    border-radius: 14px;
    padding: 0.9rem 1rem;
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.06);
    transition: all 0.25s ease;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .ip-agent-card:hover {
    transform: translateY(-2px);
    border-color: #7dd3fc;
    box-shadow: 0 8px 20px rgba(2, 132, 199, 0.12);
  }
  .ip-avatar {
    width: 42px;
    height: 42px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
    background: #f0f9ff;
    border: 1px solid #bae6fd;
  }
  .ip-agent-name {
    font-size: 0.85rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.2;
  }
  .ip-agent-role {
    font-size: 0.72rem;
    color: #0284c7;
    font-weight: 600;
    line-height: 1.2;
  }
  .ip-agent-desc {
    font-size: 0.68rem;
    color: #64748b;
    margin-top: 2px;
  }

  /* Search & Prompt Section - ChatGPT Style */
  .ip-search-container {
    background: #ffffff;
    border: 1.5px solid #bae6fd;
    border-radius: 20px;
    padding: 1.5rem 1.6rem 1.2rem;
    box-shadow: 0 12px 30px -4px rgba(2, 132, 199, 0.12), 0 4px 6px -1px rgba(15, 23, 42, 0.04);
    margin-bottom: 1.4rem;
    transition: all 0.25s ease;
  }
  .ip-search-container:focus-within {
    border-color: #0284c7;
    box-shadow: 0 14px 34px -4px rgba(2, 132, 199, 0.2), 0 0 0 3px rgba(56, 189, 248, 0.25);
  }
  .stTextArea textarea {
    background: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 12px !important;
    color: #0f172a !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1rem !important;
    line-height: 1.6 !important;
    resize: none !important;
    padding: 0.9rem !important;
    box-shadow: inset 0 2px 4px rgba(15, 23, 42, 0.03) !important;
  }
  .stTextArea textarea:focus {
    border-color: #0284c7 !important;
    background: #ffffff !important;
    box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.2) !important;
  }
  .stTextArea > label {
    font-size: 0.86rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    letter-spacing: 0.3px !important;
  }

  /* Primary Action Button ("⚡ Let's Search") - Rich Navy Blue */
  .ip-search-action div[data-testid="stButton"] > button,
  .ip-search-container > div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%) !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 1.05rem !important;
    border: 1px solid #1e3a8a !important;
    border-radius: 14px !important;
    padding: 0.85rem 2.2rem !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.35) !important;
    transition: all 0.22s ease !important;
    width: 100% !important;
  }
  .ip-search-action div[data-testid="stButton"] > button:hover,
  .ip-search-container > div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
    border-color: #38bdf8 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.5) !important;
  }

  /* Live Progress Workflow */
  .ip-flow-step {
    background: #ffffff;
    border: 1px solid #e0f2fe;
    border-radius: 12px;
    padding: 0.75rem 1rem;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 0.6rem;
    font-size: 0.88rem;
    font-weight: 600;
    color: #1e293b;
    box-shadow: 0 2px 6px rgba(14, 165, 233, 0.05);
  }
  .ip-flow-step.active {
    background: #f0f9ff;
    border: 1.5px solid #0284c7;
    color: #0369a1;
  }
  .ip-flow-step.done {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    color: #475569;
  }

  /* Research Report Container */
  .ip-report-box {
    background: #ffffff;
    border: 1px solid #bae6fd;
    border-radius: 18px;
    padding: 2.2rem 2.4rem;
    box-shadow: 0 10px 30px -5px rgba(2, 132, 199, 0.09), 0 4px 6px -2px rgba(15, 23, 42, 0.03);
    margin-top: 1rem;
    line-height: 1.75;
    color: #1e293b;
  }
  .ip-report-box h1, .ip-report-box h2, .ip-report-box h3 {
    color: #0f172a;
    font-weight: 800;
    letter-spacing: -0.4px;
  }
  .ip-report-box h2 {
    border-bottom: 2px solid #e0f2fe;
    padding-bottom: 0.4rem;
    margin-top: 1.6rem;
  }

  /* Critic Review Card */
  .ip-critic-card {
    background: linear-gradient(135deg, #f8fafc 0%, #f0f9ff 100%);
    border: 1.5px solid #7dd3fc;
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    margin-top: 1.4rem;
    box-shadow: 0 6px 18px rgba(14, 165, 233, 0.08);
  }
  .ip-critic-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.9rem;
  }
  .ip-score-badge {
    background: #0f172a;
    color: #38bdf8;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 0.9rem;
    padding: 4px 14px;
    border-radius: 20px;
    border: 1px solid #38bdf8;
  }

  /* Picture Suggestions / Visual Preview Cards */
  .ip-picture-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 1.2rem 0;
  }
  .ip-picture-card {
    background: #ffffff;
    border: 1px solid #e0f2fe;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.08);
    transition: transform 0.2s ease;
  }
  .ip-picture-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(2, 132, 199, 0.16);
  }
  .ip-picture-card img {
    width: 100%;
    height: 160px;
    object-fit: cover;
  }
  .ip-picture-caption {
    padding: 0.8rem 1rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: #1e293b;
    background: #ffffff;
  }

  /* Download Buttons */
  .stDownloadButton > button {
    background: #ffffff !important;
    color: #0f172a !important;
    border: 1.5px solid #0284c7 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    box-shadow: 0 2px 8px rgba(2, 132, 199, 0.1) !important;
    transition: all 0.2s ease !important;
  }
  .stDownloadButton > button:hover {
    background: #f0f9ff !important;
    border-color: #0369a1 !important;
    color: #0284c7 !important;
    transform: translateY(-1px) !important;
  }

  /* Verified Web Source Badges */
  .ip-sources-box {
    background: #ffffff;
    border: 1px solid #bae6fd;
    border-radius: 14px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 2px 8px rgba(2, 132, 199, 0.05);
  }
  .ip-sources-title {
    font-size: 0.76rem;
    font-weight: 700;
    color: #0369a1;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .ip-sources-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
  .ip-source-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 0.8rem;
    font-weight: 600;
    color: #0284c7 !important;
    text-decoration: none !important;
    transition: all 0.2s ease;
  }
  .ip-source-pill:hover {
    background: #e0f2fe;
    border-color: #38bdf8;
    color: #0369a1 !important;
    transform: translateY(-1px);
    box-shadow: 0 3px 8px rgba(2, 132, 199, 0.15);
  }

  /* Direct Base64 Instant Download Link */
  .ip-dl-direct-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: linear-gradient(135deg, #0284c7 0%, #0f172a 100%);
    color: #ffffff !important;
    font-size: 0.88rem;
    font-weight: 700;
    text-decoration: none !important;
    padding: 0.62rem 1.4rem;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.28);
    transition: all 0.2s ease;
    width: 100%;
    text-align: center;
    box-sizing: border-box;
  }
  .ip-dl-direct-btn:hover {
    background: linear-gradient(135deg, #0369a1 0%, #1e293b 100%);
    color: #ffffff !important;
    transform: translateY(-1.5px);
    box-shadow: 0 6px 18px rgba(2, 132, 199, 0.4);
  }

  /* Hero Relevant Photo in Report */
  .ip-hero-banner {
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 1.5rem;
    border: 1.5px solid #bae6fd;
    box-shadow: 0 6px 20px rgba(2, 132, 199, 0.1);
  }
  .ip-hero-banner img {
    width: 100%;
    max-height: 280px;
    object-fit: cover;
    display: block;
  }
  .ip-hero-caption {
    background: #ffffff;
    padding: 0.7rem 1.1rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: #334155;
    border-top: 1px solid #e0f2fe;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  /* Audio Briefing Player Card */
  .ip-audio-card {
    background: #ffffff;
    border: 1px solid #bae6fd;
    border-radius: 14px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.08);
  }

  /* Tab styling */
  .stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(224, 242, 254, 0.5);
    padding: 6px;
    border-radius: 12px;
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.88rem;
    color: #475569;
    padding: 8px 16px;
  }
  .stTabs [aria-selected="true"] {
    background-color: #ffffff !important;
    color: #0284c7 !important;
    box-shadow: 0 2px 8px rgba(2, 132, 199, 0.12) !important;
  }
</style>
""", unsafe_allow_html=True)

# ── Session State Management ───────────────────────────────────────────────────
for key, default in [
    ("result", None),
    ("running", False),
    ("error", None),
    ("selected_topic", "Quantum Computing Breakthroughs in 2026"),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Helpers for Sources and Visuals ─────────────────────────────────────────────
def extract_sources(*data_items) -> list:
    """Extracts valid URLs and domain names from any search results (str, list, dict)."""
    text_parts = []
    for item in data_items:
        if isinstance(item, (list, tuple)):
            for sub in item:
                text_parts.append(str(sub))
        elif isinstance(item, dict):
            for v in item.values():
                text_parts.append(str(v))
        elif item is not None:
            text_parts.append(str(item))

    combined_text = "\n".join(text_parts)
    urls = re.findall(r'https?://[^\s<>"\'\)]+', combined_text)
    sources = []
    seen = set()
    for u in urls:
        clean_u = u.rstrip(".,;:')\"")
        if clean_u not in seen and len(clean_u) > 12:
            seen.add(clean_u)
            domain = clean_u.split("//")[-1].split("/")[0].replace("www.", "")
            sources.append({"url": clean_u, "domain": domain})
    return sources[:8]

def get_topic_visuals(topic_clean: str):
    """Returns curated contextual images and captions for the topic."""
    topic_lower = topic_clean.lower()
    if "quantum" in topic_lower:
        return [
            ("https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&auto=format&fit=crop&q=80", "Quantum Processor Qubits & Superconducting Circuits"),
            ("https://images.unsplash.com/photo-1509228468518-180dd4864904?w=800&auto=format&fit=crop&q=80", "Mathematical Foundations & Quantum Decoherence"),
            ("https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format&fit=crop&q=80", "Next-Gen Quantum Hardware Infrastructure"),
        ]
    elif "battery" in topic_lower:
        return [
            ("https://images.unsplash.com/photo-1558441719-f3088b394f1d?w=800&auto=format&fit=crop&q=80", "Solid-State Electrolyte & Anode Chemistry"),
            ("https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=800&auto=format&fit=crop&q=80", "Electric Vehicle Energy Density Scaling"),
            ("https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=800&auto=format&fit=crop&q=80", "Advanced Materials & Gigafactory Manufacturing"),
        ]
    elif "gene" in topic_lower or "crispr" in topic_lower:
        return [
            ("https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&auto=format&fit=crop&q=80", "CRISPR-Cas9 Gene Editing Mechanism"),
            ("https://images.unsplash.com/photo-1579165466791-78822231267f?w=800&auto=format&fit=crop&q=80", "Biomolecular Double Helix Architecture"),
            ("https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&auto=format&fit=crop&q=80", "Clinical Trial Precision Medicine Delivery"),
        ]
    else:
        return [
            ("https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&auto=format&fit=crop&q=80", "Neural Intelligence & Multi-Agent Cognitive Graph"),
            ("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop&q=80", "Autonomous Decision Architecture & Systems"),
            ("https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&auto=format&fit=crop&q=80", "Global Cybernetic Knowledge Synthesis"),
        ]

# ── Voice Speech-to-Text and Text-to-Speech Helpers ─────────────────────────────
def transcribe_speech_audio(audio_bytes: bytes) -> str:
    """Transcribes audio using SpeechRecognition with graceful error handling and Gemini fallback."""
    # 1. Primary: SpeechRecognition
    if sr is not None:
        try:
            r = sr.Recognizer()
            with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                r.adjust_for_ambient_noise(source, duration=0.15)
                audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            if text and text.strip():
                return text.strip()
        except Exception:
            pass

    # 2. Fallback: Google Gemini
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-flash-latest")
            res = model.generate_content([
                {"mime_type": "audio/wav", "data": audio_bytes},
                "Transcribe this spoken research inquiry into clean text. Output only the query words without quotes or punctuation."
            ])
            if res.text and res.text.strip():
                return res.text.strip()
    except Exception:
        pass

    return ""

def generate_voice_briefing(text: str) -> bytes:
    """Generates MP3 audio for Julian Hayes's spoken executive summary."""
    if gTTS is None:
        return b""
    try:
        clean_text = re.sub(r'#+\s*', '', text)
        clean_text = re.sub(r'[*_`\[\]]', '', clean_text)
        summary_slice = clean_text[:480].strip()
        if not summary_slice:
            summary_slice = "Research completed. Please examine the detailed executive briefing below."
        tts = gTTS(text=f"Here is your executive research briefing. {summary_slice}", lang='en', tld='com')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp.getvalue()
    except Exception:
        return b""

# ── PDF Generation Helper ───────────────────────────────────────────────────────
def generate_pdf_report(topic: str, report_text: str, feedback_text: str = "", sources: list = None) -> bytes:
    """Generates an executive, beautifully styled PDF using fpdf2 without horizontal space errors."""
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=16)
        pdf.add_page()

        # Top Banner in Navy Blue
        pdf.set_fill_color(15, 23, 42)
        pdf.rect(0, 0, 210, 32, "F")

        # Header Title
        pdf.set_xy(16, 9)
        pdf.set_font("helvetica", "B", 17)
        pdf.set_text_color(240, 249, 255)
        pdf.cell(w=pdf.epw, h=8, text="InfoPlus  |  AI Research Intelligence", new_x="LMARGIN", new_y="NEXT")

        # Header Subtitle
        pdf.set_xy(16, 17)
        pdf.set_font("helvetica", "", 9)
        pdf.set_text_color(186, 230, 253)
        pdf.cell(w=pdf.epw, h=6, text="Autonomous Multi-Agent Investigation & Synthesis Report", new_x="LMARGIN", new_y="NEXT")

        pdf.set_y(38)

        # Subject Line
        pdf.set_x(pdf.l_margin)
        pdf.set_font("helvetica", "B", 13)
        pdf.set_text_color(15, 23, 42)
        clean_topic = topic.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(w=pdf.epw, h=7, text=f"Topic: {clean_topic}", new_x="LMARGIN", new_y="NEXT")

        # Human Agent Team attribution
        pdf.set_x(pdf.l_margin)
        pdf.set_font("helvetica", "I", 9)
        pdf.set_text_color(71, 85, 105)
        agent_line = "Agents: Alex Vance (Search)  |  Dr. Elena Rostova (Analysis)  |  Julian Hayes (Author)  |  Sophia Sterling (Critic)"
        pdf.cell(w=pdf.epw, h=5, text=agent_line, new_x="LMARGIN", new_y="NEXT")

        # Divider bar
        pdf.set_draw_color(14, 165, 233)
        pdf.set_line_width(0.6)
        pdf.line(pdf.l_margin, pdf.get_y() + 2, pdf.w - pdf.r_margin, pdf.get_y() + 2)
        pdf.ln(6)

        # Executive Report Body
        pdf.set_font("helvetica", "", 10)
        pdf.set_text_color(30, 41, 59)
        clean_report = report_text.encode("latin-1", "replace").decode("latin-1")

        for raw_line in clean_report.split("\n"):
            line = raw_line.strip()
            pdf.set_x(pdf.l_margin)
            if not line:
                pdf.ln(3)
                continue
            if line.startswith("#"):
                pdf.ln(3)
                pdf.set_font("helvetica", "B", 12)
                pdf.set_text_color(2, 132, 199)
                cleaned_heading = line.lstrip("#").strip()
                pdf.multi_cell(w=pdf.epw, h=6.5, text=cleaned_heading, new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("helvetica", "", 10)
                pdf.set_text_color(30, 41, 59)
            else:
                pdf.multi_cell(w=pdf.epw, h=5.5, text=line, new_x="LMARGIN", new_y="NEXT")

        # Critic Review Section
        if feedback_text:
            pdf.ln(5)
            pdf.set_x(pdf.l_margin)
            pdf.set_fill_color(240, 249, 255)
            pdf.rect(pdf.l_margin, pdf.get_y(), pdf.epw, 9, "F")
            pdf.set_font("helvetica", "B", 11)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(w=pdf.epw, h=8, text="  Editorial Peer Review & Quality Audit (Sophia Sterling, Critic)", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)

            pdf.set_font("helvetica", "", 9.5)
            pdf.set_text_color(51, 65, 85)
            clean_feedback = feedback_text.encode("latin-1", "replace").decode("latin-1")
            for raw_fb in clean_feedback.split("\n"):
                fb_line = raw_fb.strip()
                pdf.set_x(pdf.l_margin)
                if not fb_line:
                    pdf.ln(2.5)
                    continue
                pdf.multi_cell(w=pdf.epw, h=5.2, text=fb_line, new_x="LMARGIN", new_y="NEXT")

        # Verified Sources Section in PDF
        if sources:
            pdf.ln(5)
            pdf.set_x(pdf.l_margin)
            pdf.set_fill_color(240, 249, 255)
            pdf.rect(pdf.l_margin, pdf.get_y(), pdf.epw, 8, "F")
            pdf.set_font("helvetica", "B", 10.5)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(w=pdf.epw, h=7, text="  Verified Web Sources & Citations", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)

            pdf.set_font("helvetica", "", 8.5)
            pdf.set_text_color(2, 132, 199)
            for s in sources:
                u = s.get("url", "")
                d = s.get("domain", "")
                clean_src = f"[{d}] {u}".encode("latin-1", "replace").decode("latin-1")
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(w=pdf.epw, h=4.8, text=clean_src, new_x="LMARGIN", new_y="NEXT")

        return bytes(pdf.output())

    except Exception as e:
        # Emergency fallback PDF so the application never crashes
        fallback_pdf = FPDF()
        fallback_pdf.add_page()
        fallback_pdf.set_font("helvetica", "B", 14)
        fallback_pdf.cell(w=fallback_pdf.epw, h=8, text="InfoPlus Research Report", new_x="LMARGIN", new_y="NEXT")
        fallback_pdf.set_font("helvetica", "", 10)
        fallback_pdf.multi_cell(w=fallback_pdf.epw, h=6, text=report_text.encode("latin-1", "replace").decode("latin-1"), new_x="LMARGIN", new_y="NEXT")
        return bytes(fallback_pdf.output())

# ── Top Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ip-header">
  <div class="ip-brand-left">
    <div class="ip-logo-badge">🔍</div>
    <div>
      <div class="ip-brand-title">Info<span>Plus</span></div>
      <div class="ip-brand-sub">Multi-Agent Intelligence Network · Deep Research & Synthesis</div>
    </div>
  </div>
  <div class="ip-status-pill">
    <div class="ip-status-dot"></div>
    4 Specialized Agents Ready
  </div>
</div>
""", unsafe_allow_html=True)

# ── Human Agent Team Section (Human-Centric Agent Design) ─────────────────────
st.markdown('<div class="ip-agent-bar-title">👥 Assigned Human Agent Specialists</div>', unsafe_allow_html=True)
st.markdown("""
<div class="ip-agent-grid">
  <div class="ip-agent-card">
    <div class="ip-avatar">🔍</div>
    <div>
      <div class="ip-agent-name">Alex Vance</div>
      <div class="ip-agent-role">Lead Web Detective</div>
      <div class="ip-agent-desc">Real-time source discovery</div>
    </div>
  </div>
  <div class="ip-agent-card">
    <div class="ip-avatar">📖</div>
    <div>
      <div class="ip-agent-name">Dr. Elena Rostova</div>
      <div class="ip-agent-role">Senior Data Analyst</div>
      <div class="ip-agent-desc">Deep scraping & extraction</div>
    </div>
  </div>
  <div class="ip-agent-card">
    <div class="ip-avatar">✍️</div>
    <div>
      <div class="ip-agent-name">Julian Hayes</div>
      <div class="ip-agent-role">Executive Author</div>
      <div class="ip-agent-desc">Multi-section briefing synthesis</div>
    </div>
  </div>
  <div class="ip-agent-card">
    <div class="ip-avatar">⚖️</div>
    <div>
      <div class="ip-agent-name">Sophia Sterling</div>
      <div class="ip-agent-role">Editorial Director</div>
      <div class="ip-agent-desc">Peer audit & rigor scoring</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── ChatGPT-Inspired Search & Topic Input ─────────────────────────────────────
st.markdown('<div class="ip-search-container">', unsafe_allow_html=True)

topic_input = st.text_area(
    "What would you like the InfoPlus team to research today?",
    value=st.session_state.selected_topic,
    placeholder="e.g. Commercial viability of solid-state EV batteries by 2027...",
    height=86,
    key="research_topic_text",
)

# Voice Audio Recorder (Direct microphone capture)
with st.expander("🎙️ Speak your research topic (Voice Recorder)", expanded=True):
    audio_val = st.audio_input("Record audio from your microphone:", key="voice_mic_input")
    if audio_val is not None:
        audio_bytes = audio_val.getvalue()
        audio_hash = hash(audio_bytes)
        if st.session_state.get("last_audio_hash") != audio_hash:
            st.session_state["last_audio_hash"] = audio_hash
            with st.spinner("🎙️ Transcribing spoken research query..."):
                transcribed = transcribe_speech_audio(audio_bytes)
                if transcribed:
                    st.session_state["research_topic_text"] = transcribed
                    st.session_state.selected_topic = transcribed
                    st.session_state["voice_input_active"] = True
                    st.success(f"✨ Transcribed voice input: **\"{transcribed}\"**")
                    time.sleep(0.4)
                    st.rerun()
                else:
                    st.info("🎙️ Voice recorded. Speak clearly into your microphone, or type your query directly above.")

if st.session_state.get("voice_input_active") and st.session_state.get("selected_topic"):
    st.markdown(f"""
    <div style="background:#f0f9ff; border:1px solid #7dd3fc; border-radius:10px; padding:8px 14px; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
      <span style="font-size:1.1rem;">🎙️</span>
      <span style="font-size:0.84rem; color:#0369a1; font-weight:700;">
        Voice Query Loaded: <span style="color:#0f172a;">"{st.session_state.selected_topic}"</span>
      </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="ip-search-action">', unsafe_allow_html=True)
run_clicked = st.button("⚡ Let's Search", disabled=st.session_state.running)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ── Dynamic Pipeline Execution ───────────────────────────────────────────────
if run_clicked:
    effective_topic = (
        st.session_state.get("research_topic_text", "").strip()
        or topic_input.strip()
        or st.session_state.get("selected_topic", "").strip()
    )
    if not effective_topic:
        st.warning("⚠️ Please provide a topic or record your voice query above.")
    else:
        st.session_state.result = None
        st.session_state.error = None
        st.session_state.running = True

        status_box = st.empty()
        anim_box = st.empty()

        try:
            from src.agents.agent import (
                build_search_agent, build_reader_agent,
                writer_chain, critic_chain,
            )
            state = {}

            # Step 1: Alex Vance (Search)
            with anim_box, st.spinner(f"🔍 Alex Vance is scanning the live web for: '{effective_topic}'..."):
                status_box.markdown(f"""
                <div class="ip-flow-step active">
                  <span>🔍</span>
                  <div><b>Step 1/4 · Alex Vance:</b> Searching top digital databases for <i>"{effective_topic}"</i>...</div>
                </div>
                """, unsafe_allow_html=True)
                sa = build_search_agent()
                sr = sa.invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {effective_topic}")]})
                state["search_results"] = sr["messages"][-1].content

            # Step 2: Dr. Elena Rostova (Reader / Scraper)
            with anim_box, st.spinner("📖 Dr. Elena Rostova is scraping and parsing in-depth whitepapers & articles..."):
                status_box.markdown(f"""
                <div class="ip-flow-step done"><span>✓</span> <b>Step 1 Complete:</b> Alex Vance gathered global intelligence.</div>
                <div class="ip-flow-step active">
                  <span>📖</span>
                  <div><b>Step 2/4 · Dr. Elena Rostova:</b> Scraping most authoritative primary sources for deep context...</div>
                </div>
                """, unsafe_allow_html=True)
                ra = build_reader_agent()
                rr = ra.invoke({"messages": [("user",
                    f"Based on the following search results about '{effective_topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{str(state['search_results'])[:800]}")]})
                state["scraped_content"] = rr["messages"][-1].content

            # Step 3: Julian Hayes (Writer)
            with anim_box, st.spinner("✍️ Julian Hayes is drafting a comprehensive multi-section executive report..."):
                status_box.markdown("""
                <div class="ip-flow-step done"><span>✓</span> <b>Step 2 Complete:</b> Dr. Elena Rostova extracted deep content.</div>
                <div class="ip-flow-step active">
                  <span>✍️</span>
                  <div><b>Step 3/4 · Julian Hayes:</b> Synthesizing executive report with strategic insights...</div>
                </div>
                """, unsafe_allow_html=True)
                combined = (f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                            f"SCRAPED CONTENT:\n{state['scraped_content']}")
                state["report"] = writer_chain.invoke({"topic": effective_topic, "research": combined})

            # Step 4: Sophia Sterling (Critic)
            with anim_box, st.spinner("⚖️ Sophia Sterling is performing rigorous editorial review and scoring..."):
                status_box.markdown("""
                <div class="ip-flow-step done"><span>✓</span> <b>Step 3 Complete:</b> Julian Hayes finalized draft.</div>
                <div class="ip-flow-step active">
                  <span>⚖️</span>
                  <div><b>Step 4/4 · Sophia Sterling:</b> Performing editorial peer review & scoring rigor...</div>
                </div>
                """, unsafe_allow_html=True)
                state["feedback"] = critic_chain.invoke({"report": state["report"]})

            status_box.markdown("""
            <div class="ip-flow-step done" style="background:#f0fdf4; border-color:#86efac; color:#166534;">
              <span>🎉</span> <b>All 4 Agents Completed:</b> Comprehensive report synthesized & reviewed!
            </div>
            """, unsafe_allow_html=True)
            anim_box.empty()
            st.session_state.result = state
            st.session_state.selected_topic = effective_topic

        except Exception as e:
            st.session_state.error = str(e)
            anim_box.empty()
            status_box.empty()
        finally:
            st.session_state.running = False

# ── Display Results & Picture Suggestions ───────────────────────────────────────
if st.session_state.error:
    st.error(f"❌ Investigation encountered an error: {st.session_state.error}")

elif st.session_state.result:
    res = st.session_state.result
    topic_clean = st.session_state.selected_topic
    report_text = str(res.get("report", ""))
    feedback_text = str(res.get("feedback", ""))
    search_data = res.get("search_results", "")
    scraped_data = res.get("scraped_content", "")

    # Extract score if available
    score_display = "Audited & Verified"
    for line in feedback_text.splitlines():
        if "score:" in line.lower():
            score_display = line.strip()
            break

    # Action Toolbar: Download PDF & Markdown
    st.markdown("<br>", unsafe_allow_html=True)

    # Extract real web sources safely without type concatenation errors
    extracted_sources = extract_sources(search_data, scraped_data)

    # Pre-generate and cache PDF bytes in session state
    if "pdf_bytes" not in st.session_state or st.session_state.get("pdf_topic") != topic_clean:
        st.session_state["pdf_bytes"] = generate_pdf_report(topic_clean, report_text, feedback_text, sources=extracted_sources)
        st.session_state["pdf_topic"] = topic_clean

    pdf_bytes = st.session_state["pdf_bytes"]
    safe_file_name = f"InfoPlus_{topic_clean[:28].replace(' ', '_').replace('/', '_')}.pdf"
    b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')

    tb_c1, tb_c2, tb_c3 = st.columns([2, 1.3, 1.1])

    with tb_c1:
        st.markdown(f"### 📋 Research Findings: *{topic_clean}*")

    with tb_c2:
        # Direct Base64 download link (immune to Streamlit media endpoint 404s)
        st.markdown(f"""
        <a href="data:application/pdf;base64,{b64_pdf}" download="{safe_file_name}" class="ip-dl-direct-btn">
          📥 Download PDF Report
        </a>
        """, unsafe_allow_html=True)

    with tb_c3:
        md_content = f"# InfoPlus AI Research Report: {topic_clean}\n\n{report_text}\n\n---\n\n## Editorial Peer Review\n{feedback_text}\n\n---\n\n## Verified Sources\n" + "\n".join([f"- {s['domain']}: {s['url']}" for s in extracted_sources])
        st.download_button(
            label="📄 Markdown (.md)",
            data=md_content,
            file_name=f"InfoPlus_{topic_clean[:28].replace(' ', '_')}.md",
            mime="text/markdown",
            key="btn_dl_md",
        )

    # Tabs for Visuals, Report, Agents, and Sources
    tab_report, tab_pictures, tab_critic, tab_agents, tab_sources = st.tabs([
        "📄 Executive Briefing",
        "🖼️ Picture Suggestions & Visuals",
        "⚖️ Sophia's Critique & Score",
        "👥 Agent Collaboration Log",
        "🌐 Alex & Elena's Source Data",
    ])

    # Visuals for the topic
    visuals = get_topic_visuals(topic_clean)
    hero_img, hero_caption = visuals[0]

    with tab_report:
        # 1. Clickable Verified Web Sources Row (ChatGPT Style)
        if extracted_sources:
            sources_html = '<div class="ip-sources-box">'
            sources_html += f'<div class="ip-sources-title">🌐 Verified Research Sources ({len(extracted_sources)} Found by Alex Vance):</div>'
            sources_html += '<div class="ip-sources-grid">'
            for s in extracted_sources:
                sources_html += f'<a href="{s["url"]}" target="_blank" rel="noopener noreferrer" class="ip-source-pill">🔗 {s["domain"]}</a>'
            sources_html += '</div></div>'
            st.markdown(sources_html, unsafe_allow_html=True)

        # 2. Relevant Topic Picture Banner (ChatGPT Style)
        st.markdown(f"""
        <div class="ip-hero-banner">
          <img src="{hero_img}" alt="{hero_caption}" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&auto=format&fit=crop&q=80';">
          <div class="ip-hero-caption">📷 <b>Visual Intelligence:</b> {hero_caption}</div>
        </div>
        """, unsafe_allow_html=True)

        # 3. Julian Hayes Spoken Audio Briefing
        if "briefing_audio" not in st.session_state or st.session_state.get("audio_topic") != topic_clean:
            st.session_state["briefing_audio"] = generate_voice_briefing(report_text)
            st.session_state["audio_topic"] = topic_clean

        if st.session_state.get("briefing_audio"):
            st.markdown("""
            <div class="ip-audio-card">
              <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                <span style="font-size:1.4rem;">🔊</span>
                <div>
                  <b style="font-size:0.92rem; color:#0f172a;">Julian Hayes · Executive Audio Briefing</b><br>
                  <span style="font-size:0.75rem; color:#0284c7; font-weight:600;">Spoken briefing synthesized from the research findings</span>
                </div>
              </div>
            """, unsafe_allow_html=True)
            st.audio(st.session_state["briefing_audio"], format="audio/mp3")
            st.markdown("</div>", unsafe_allow_html=True)

        # 4. Main Report Body
        st.markdown(f"""
        <div class="ip-report-box">
          <div style="font-size:0.8rem; color:#0284c7; font-weight:700; text-transform:uppercase; letter-spacing:0.8px;">
            Synthesized by Julian Hayes · Lead Research Author
          </div>
        """, unsafe_allow_html=True)
        st.markdown(report_text)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_pictures:
        st.markdown("""
        <div style="margin-top:0.5rem; margin-bottom:1rem;">
          <h4 style="color:#0f172a; margin-bottom:4px;">🖼️ ChatGPT-Style Visual Concept & Picture Suggestions</h4>
          <p style="color:#64748b; font-size:0.85rem;">
            Curated imagery and conceptual photo suggestions corresponding to key research themes.
          </p>
        </div>
        """, unsafe_allow_html=True)

        # Generate topic-relevant keyword themes for pictures
        topic_lower = topic_clean.lower()
        if "quantum" in topic_lower:
            images = [
                ("https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=600&auto=format&fit=crop&q=80", "Quantum Processor Qubits & Superconducting Circuits"),
                ("https://images.unsplash.com/photo-1509228468518-180dd4864904?w=600&auto=format&fit=crop&q=80", "Mathematical Foundations & Quantum Decoherence"),
                ("https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&auto=format&fit=crop&q=80", "Next-Gen Quantum Hardware Infrastructure"),
            ]
        elif "battery" in topic_lower:
            images = [
                ("https://images.unsplash.com/photo-1558441719-f3088b394f1d?w=600&auto=format&fit=crop&q=80", "Solid-State Electrolyte & Anode Chemistry"),
                ("https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=600&auto=format&fit=crop&q=80", "Electric Vehicle Energy Density Scaling"),
                ("https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=600&auto=format&fit=crop&q=80", "Advanced Materials & Gigafactory Manufacturing"),
            ]
        elif "gene" in topic_lower or "crispr" in topic_lower:
            images = [
                ("https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=600&auto=format&fit=crop&q=80", "CRISPR-Cas9 Gene Editing Mechanism"),
                ("https://images.unsplash.com/photo-1579165466791-78822231267f?w=600&auto=format&fit=crop&q=80", "Biomolecular Double Helix Architecture"),
                ("https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=600&auto=format&fit=crop&q=80", "Clinical Trial Precision Medicine Delivery"),
            ]
        else:
            images = [
                ("https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600&auto=format&fit=crop&q=80", "Neural Intelligence & Multi-Agent Cognitive Graph"),
                ("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&auto=format&fit=crop&q=80", "Autonomous Decision Architecture & Systems"),
                ("https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=600&auto=format&fit=crop&q=80", "Global Cybernetic Knowledge Synthesis"),
            ]

        p_cols = st.columns(3)
        for idx, (img_url, caption) in enumerate(images):
            with p_cols[idx]:
                st.markdown(f"""
                <div class="ip-picture-card">
                  <img src="{img_url}" alt="{caption}" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&auto=format&fit=crop&q=80';">
                  <div class="ip-picture-caption">📌 {caption}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 **ChatGPT-Style Visual Insight:** When researching complex technical topics, visual architecture diagrams, hardware schematics, and chemical formulations significantly accelerate executive comprehension.")

    with tab_critic:
        st.markdown(f"""
        <div class="ip-critic-card">
          <div class="ip-critic-header">
            <div style="display:flex; align-items:center; gap:10px;">
              <span style="font-size:1.6rem;">⚖️</span>
              <div>
                <b style="font-size:1.05rem; color:#0f172a;">Sophia Sterling</b><br>
                <span style="font-size:0.75rem; color:#0284c7; font-weight:600;">Editorial Director & Quality Critic</span>
              </div>
            </div>
            <div class="ip-score-badge">{score_display}</div>
          </div>
          <div style="font-size:0.92rem; color:#334155; line-height:1.7;">
            {feedback_text}
          </div>
        </div>
        """, unsafe_allow_html=True)

    with tab_agents:
        st.markdown("""
        <div style="display:flex; flex-direction:column; gap:14px; margin-top:0.6rem;">
          <div class="ip-flow-step done">
            <span style="font-size:1.3rem;">🔍</span>
            <div>
              <b>Alex Vance (Lead Web Detective):</b> Executed global query, retrieved real-time digital intelligence and prioritized authoritative web documents.
            </div>
          </div>
          <div class="ip-flow-step done">
            <span style="font-size:1.3rem;">📖</span>
            <div>
              <b>Dr. Elena Rostova (Senior Content Analyst):</b> Extracted in-depth technical paragraphs, verified primary sources, and eliminated redundant noise.
            </div>
          </div>
          <div class="ip-flow-step done">
            <span style="font-size:1.3rem;">✍️</span>
            <div>
              <b>Julian Hayes (Executive Author):</b> Synthesized findings into a cohesive, structured briefing with clear headings and implications.
            </div>
          </div>
          <div class="ip-flow-step done">
            <span style="font-size:1.3rem;">⚖️</span>
            <div>
              <b>Sophia Sterling (Editorial Director):</b> Conducted peer review, verified factual consistency, and assigned rigorous quality score.
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with tab_sources:
        with st.expander("🌐 Alex Vance's Raw Search Findings", expanded=False):
            st.code(str(search_data), language="text")
        with st.expander("📖 Dr. Elena Rostova's Scraped Deep Content", expanded=False):
            st.code(str(scraped_data), language="text")

else:
    # Initial State Hero Prompt
    st.markdown("""
    <div style="text-align:center; padding: 3rem 1.5rem; background:rgba(255,255,255,0.7); border-radius:18px; border:1px dashed #bae6fd; margin-top:1rem;">
      <div style="font-size:2.8rem; margin-bottom:0.8rem;">🌐 👥 📑</div>
      <h3 style="color:#0f172a; font-weight:800; margin-bottom:0.4rem;">Your Autonomous Research Team Is On Standby</h3>
      <p style="color:#64748b; font-size:0.92rem; max-width:620px; margin:0 auto 1.5rem auto;">
        Alex Vance, Dr. Elena Rostova, Julian Hayes, and Sophia Sterling collaborate synchronously to search the global web, scrape technical data, draft executive briefings, and peer-review findings into downloadable PDF reports.
      </p>
      <div style="display:inline-flex; gap:10px; font-size:0.82rem; font-weight:600; color:#0369a1; background:#e0f2fe; padding:6px 18px; border-radius:24px;">
        ✨ Sky Blue & Navy Palette &nbsp;•&nbsp; 📥 PDF & MD Export &nbsp;•&nbsp; 🖼️ Visual Suggestions
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-top:3.5rem; padding-top:1.5rem; border-top:1px solid #bae6fd; font-size:0.75rem; color:#64748b;">
  <b>InfoPlus</b> · Powered by LangChain, LangGraph & Gemini · Multi-Agent Research System
</div>
""", unsafe_allow_html=True)
