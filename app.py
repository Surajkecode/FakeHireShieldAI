import streamlit as st
import pandas as pd
import os
import random
import datetime
import re
import spacy
from dotenv import load_dotenv
import google.generativeai as genai
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY not found in .env!")
    st.stop()

MODEL_ID = "models/gemini-1.5-flash"
genai.configure(api_key=GEMINI_API_KEY)

@st.cache_resource
def load_spacy():
    return spacy.load("en_core_web_sm")

nlp = load_spacy()

SCAM_KEYWORDS = [
    "urgent hire", "quick money", "immediate start", "work from home",
    "no experience required", "limited positions", "training provided",
    "data entry", "admin fee", "credit report", "wire transfer",
    "application fee", "send money", "direct deposit", "equipment fee",
    "cash job", "easy money", "flexible hours", "processing fee",
    "crypto", "pay to apply", "gift card", "advance payment", "loan",
    "bank details", "interview fee", "free laptop", "too good to be true",
    "investment", "salary advance"
]

DATA_FOLDER = "data"
BLACKLIST_FILE = os.path.join(DATA_FOLDER, "blacklist.csv")
FEEDBACK_FILE = os.path.join(DATA_FOLDER, "feedback.csv")
QUIZ_SCORE_FILE = os.path.join(DATA_FOLDER, "quiz_scores.csv")

@st.cache_data
def load_blacklist():
    if not os.path.exists(BLACKLIST_FILE):
        return []
    try:
        df = pd.read_csv(BLACKLIST_FILE)
        return df["company"].dropna().tolist() if "company" in df.columns else []
    except Exception:
        return []

def save_blacklist(blacklist):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    pd.DataFrame({"company": sorted(set(blacklist))}).to_csv(BLACKLIST_FILE, index=False)

def detect_scam_keywords(text):
    return [kw for kw in SCAM_KEYWORDS if kw in text.lower()]

def predict_scam_risk(text):
    keywords = detect_scam_keywords(text)
    score = len(keywords) / len(SCAM_KEYWORDS)
    if score > 0.35:
        return "\U0001F6AB Strongly Fake", "High", keywords
    elif score > 0.15:
        return "\u26A0\uFE0F Possibly Fake", "Moderate", keywords
    else:
        return "\u2705 Probably Real", "Low", keywords

def highlight_keywords(text, keywords):
    for kw in sorted(keywords, key=len, reverse=True):
        text = re.sub(re.escape(kw), f"<span style='color:red; font-weight:bold'>{kw}</span>", text, flags=re.IGNORECASE)
    return text

def save_feedback(text, label):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().isoformat()
        f.write(f'"{text.replace(chr(34), chr(39))}","{label}","{timestamp}"\n')

def explain_with_gemini(text):
    try:
        model = genai.GenerativeModel(MODEL_ID)
        prompt = f"Explain why this job post may be a scam: {text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini explanation error: {e}"

def scrape_url_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all('p')
        return "\n".join(p.text for p in paragraphs)
    except Exception as e:
        return f"Error scraping content: {e}"

def get_scam_feed():
    return [
        "\U0001F4AC User: Got offered remote job with upfront fee — scam?",
        "\u26A0\uFE0F Warning: Internship asking for 'processing fee'.",
        "\U0001F6A8 BBB alert: Crypto hiring scam reported in July 2025.",
    ]

def log_quiz_score(score, total):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    timestamp = datetime.datetime.now().isoformat()
    with open(QUIZ_SCORE_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp},{score},{total}\n")

def show_header():
    st.markdown("""
        <h1 style="text-align:center; color:#d90429;">\U0001F6A8 Fake Job & Internship Detector \U0001F6A8</h1>
        <h4 style="text-align:center; color:#aaa;">Protect yourself from scams - powered by AI</h4>
    """, unsafe_allow_html=True)

def show_sidebar():
    st.sidebar.title("\U0001F4CC Navigation")
    st.sidebar.image("https://images.unsplash.com/photo-1504384308090-2f0ef1f1063c?auto=format&fit=crop&w=300&q=80", width=150)
    return st.sidebar.selectbox("Choose a page", ["Analyze", "Blacklist", "Chatbot", "Quiz", "Scam Feed"])

def analyze_page(blacklist):
    st.subheader("\U0001F92E‍💨 Analyze a Job or Internship Description")
    content_input = st.text_area("Paste job description or message", height=220)
    url_input = st.text_input("Or paste a job post URL to scrape")

    if st.button("Analyze"):
        if url_input.strip():
            content = scrape_url_content(url_input.strip())
            st.text_area("\U0001F310 Scraped Content", content, height=200)
        else:
            content = content_input

        if not content.strip():
            st.warning("Please enter some text or URL.")
            return

        prediction, confidence, keywords = predict_scam_risk(content)
        doc = nlp(content)
        companies = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        flagged = any(c.lower() in (x.lower() for x in blacklist) for c in companies)

        st.info(f"Confidence: {confidence}")
        if prediction.startswith("\U0001F6AB"):
            st.error(f"Prediction: **{prediction}**")
        elif prediction.startswith("\u26A0"):
            st.warning(f"Prediction: **{prediction}**")
        else:
            st.success(f"Prediction: **{prediction}**")

        st.markdown("### Keywords Found")
        st.write(", ".join(keywords) if keywords else "No scam keywords detected.")
        st.markdown("### Highlighted Text")
        st.markdown(highlight_keywords(content, keywords), unsafe_allow_html=True)
        if companies:
            st.info("Companies Detected: " + ", ".join(companies))
        if flagged:
            st.error("\u26A0\uFE0F Warning: Company matched the blacklist!")

        st.markdown("---")
        st.markdown("### 🤖 Gemini Explanation")
        explanation = explain_with_gemini(content)
        st.markdown(explanation)

        st.markdown("### Your Feedback")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("\U0001F44D Yes"):
                save_feedback(content, "correct")
                st.success("Thank you for your feedback!")
        with col2:
            if st.button("\U0001F44E No"):
                save_feedback(content, "incorrect")
                st.warning("We appreciate your input!")

def chatbot_page():
    st.subheader("\U0001F4AC AI Chatbot – Scam Helper")
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("You:", key="chat_input")

    if user_input:
        system_instruction = (
            "You are a helpful assistant who specializes in detecting fake job and internship offers. "
            "If a user pastes a job description or message, analyze it and give a scam risk verdict, "
            "explain your reasoning, and offer safety advice. If unrelated, still respond helpfully."
        )

        try:
            model = genai.GenerativeModel(MODEL_ID)
            chat = model.start_chat(history=[
                {"role": "user", "parts": [{"text": system_instruction}]}
            ])
            response = chat.send_message(user_input)
            bot_reply = response.text.strip()
        except Exception as e:
            bot_reply = f"\u26A0\uFE0F Gemini error: {e}"

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", bot_reply))

    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(f"<div style='background:#111;padding:10px;border-radius:10px;'>{message}</div>", unsafe_allow_html=True)

def blacklist_page():
    st.subheader("\U0001F6AB Manage Blacklisted Companies")
    blacklist = load_blacklist()
    new_entry = st.text_input("Add Company to Blacklist:")
    if st.button("Add"):
        if new_entry.strip():
            blacklist.append(new_entry.strip())
            save_blacklist(blacklist)
            st.success(f"Added: {new_entry}")
    if blacklist:
        st.write("### Current Blacklist:")
        st.write(sorted(set(blacklist)))

def scam_feed_page():
    st.subheader("\U0001F4E1 Real-time Scam Feed")
    feed = get_scam_feed()
    for item in feed:
        st.markdown(f"- {item}")

def quiz_page():
    st.subheader("\U0001F9E0 Scam Awareness Quiz")
    questions = [
        {"question": "Are you asked to pay any fee to apply?", "ans": "No"},
        {"question": "Is the job offer vague or too good to be true?", "ans": "No"},
        {"question": "Do they avoid video interviews or official calls?", "ans": "No"},
        {"question": "Are personal/bank details requested early?", "ans": "No"},
        {"question": "Are you offered a very high salary for little work?", "ans": "No"},
        {"question": "Do they communicate only through WhatsApp or Telegram?", "ans": "No"},
        {"question": "Does the email come from a free domain?", "ans": "No"},
        {"question": "Are grammar/spelling in the offer poor?", "ans": "No"},
        {"question": "Do they ask for Aadhaar/SSN early?", "ans": "No"},
        {"question": "Do they rush you to accept the offer?", "ans": "No"},
        {"question": "Is the company's website missing or suspicious?", "ans": "No"},
        {"question": "Are you told you were hired without interview?", "ans": "No"}
    ]

    if "quiz_restart" in st.session_state or "quiz_idx" not in st.session_state:
        st.session_state.shuffled_questions = random.sample(questions, len(questions))
        st.session_state.quiz_idx = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_restart = False

    total_questions = len(st.session_state.shuffled_questions)

    if st.session_state.quiz_idx < total_questions:
        q = st.session_state.shuffled_questions[st.session_state.quiz_idx]
        st.write(f"Q{st.session_state.quiz_idx + 1}: {q['question']}")
        choice = st.radio("Choose:", ["Yes", "No"], key=f"q{st.session_state.quiz_idx}")
        if st.button("Submit", key=f"submit_{st.session_state.quiz_idx}"):
            if choice == q["ans"]:
                st.session_state.quiz_score += 1
            st.session_state.quiz_idx += 1
    else:
        score = st.session_state.quiz_score
        log_quiz_score(score, total_questions)

        st.success(f"You scored {score}/{total_questions}")
        if score == total_questions:
            st.balloons()
            st.info("\U0001F31F Excellent! You’re well aware of scam indicators.")
        elif score >= total_questions * 0.6:
            st.info("\u2705 Good job. Stay cautious and keep learning.")
        else:
            st.warning("\u26A0\uFE0F You might be vulnerable. Please review how to spot job scams.")

        if st.button("Restart Quiz"):
            st.session_state.quiz_restart = True
            st.experimental_rerun()

def main():
    st.set_page_config(page_title="Fake Job Detector", page_icon="\U0001F6A8", layout="wide")
    show_header()
    page = show_sidebar()
    blacklist = load_blacklist()

    if page == "Analyze":
        analyze_page(blacklist)
    elif page == "Blacklist":
        blacklist_page()
    elif page == "Chatbot":
        chatbot_page()
    elif page == "Quiz":
        quiz_page()
    elif page == "Scam Feed":
        scam_feed_page()

    st.markdown("<hr><center>\U0001F6A8 Stay safe. Never send money to unknown recruiters.</center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()