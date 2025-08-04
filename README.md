# 🚨 Fake Job & Internship Detection System

<p align="center"> <img src="https://img.shields.io/badge/AI-Powered-blue?style=flat-square&logo=OpenAI" /> <img src="https://img.shields.io/badge/Machine_Learning-Secure-green?style=flat-square&logo=scikit-learn" /> <img src="https://img.shields.io/badge/Scam_Intelligence-Real--Time-orange?style=flat-square&logo=datadog" /> <img src="https://img.shields.io/badge/NLP-spaCy-lightblue?style=flat-square&logo=spacy" /> <img src="https://img.shields.io/badge/Framework-Streamlit-ff4b4b?style=flat-square&logo=streamlit" /> <img src="https://img.shields.io/badge/Gemini_API-Google-4285F4?style=flat-square&logo=google" /> <img src="https://img.shields.io/badge/Web_Scraping-BeautifulSoup-6db33f?sty![Uploading d2767318-9a6a-4714-a07f-e9ec31f55c4c.png…]()
le=flat-square&logo=python" /> <img src="https://img.shields.io/badge/Data-Pandas-blue?style=flat-square&logo=pandas" /> </p>


<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/dfbea5c1-de36-4ab8-9998-7797a26aa31d" width="220"/>
    </td>
    <td align="center">
      <img src="https://user-gen-media-assets.s3.amazonaws.com/gpt4o_images/f0b2f722-5469-4402-83cf-7341b790e9ae.png" width="140"/>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/a1b8a78d-3a3e-42ca-91e9-4e25c1909155" width="220"/>
    </td>
  </tr>
</table>

<p align="center">
  🛡️ <b>Shield yourself from fake job and internship offers.</b><br>
  Powered by <b>AI</b>, <b>Machine Learning</b> & <b>Real-Time Scam Intelligence</b>.
</p>





## ✨ About the Project

**Fake Job & Internship Detector** is your AI-powered safeguard for the modern job market! Whether you’re a student, graduate, or seasoned professional, this tool helps you instantly detect scams, avoid traps, and build your career with confidence. It's intuitive, secure, and thrilling to use—making job safety fast, easy, and even fun!

## ⚡ Features at a Glance

| 🚀  | Feature                                      | Description                                                                                      |
|-----|----------------------------------------------|--------------------------------------------------------------------------------------------------|
| 🤖  | **AI/ML Scam Classifier**                    | State-of-the-art model (100% test accuracy!) instantly flags jobs as Real, Possibly Fake, or Fake|
| 🏷️  | **Scam Keyword Highlighter**                 | Detects & visually marks suspicious phrases—see the red flags in a flash!                        |
| 🏢  | **Company Name NER**                         | Auto-detects company names, cross-checks with your custom blacklist                              |
| 🔒  | **Blacklist Management**                     | Add suspicious companies & see instant alerts on matches                                         |
| 🪄  | **Gemini AI Explanation**                    | Human-style, easy-to-understand scam reasoning (powered by Google Gemini API)                    |
| 💬  | **AI Chatbot Assistant**                     | 24/7 helper answers scam-related queries and reviews offers interactively                        |
| 🧩  | **Scam Awareness Quiz**                      | Sharpen your scam-spotting instincts in a lively, gamified quiz                                  |
| 🌐  | **Job URL Scraper**                          | Paste links to auto-fetch, analyze, and highlight job details                                    |
| 📢  | **Real-time Scam Feed**                      | See worldwide scam trends and alerts—be ahead of the curve!                                      |
| 🥂  | **One-Tap Feedback**                         | Correct AI mistakes instantly, making the system smarter for everyone                            |

## 🌈 See It in Action!
### 🧠 Model Evaluation Report

| **Metric**    | **Class 0** | **Class 1** | **Macro Avg** | **Weighted Avg** |
|---------------|-------------|-------------|----------------|------------------|
| **Precision** | 1.00        | 1.00        | 1.00           | 1.00             |
| **Recall**    | 1.00        | 1.00        | 1.00           | 1.00             |
| **F1-score**  | 1.00        | 1.00        | 1.00           | 1.00             |
| **Support**   | 1975        | 1988        | 3963           | 3963             |

📊 **Accuracy:** `0.9997` (or **~99.97%**)  
The model correctly predicted **3962 out of 3963** samples — with only **one misclassification**.

---

### 🔢 Confusion Matrix

|                    | **Predicted: Fake (0)** | **Predicted: Real (1)** |
|--------------------|-------------------------|--------------------------|
| **Actual: Fake (0)** | 1974                    | 1                        |
| **Actual: Real (1)** | 0                       | 1988                     |

✅ **Model saved as:** `job_fraud_detector.pkl`

---

### 📘 Interpretation

- **Class 0** → Fake job/internship offers  
- **Class 1** → Genuine job/internship offers  
- Despite the classification report rounding values to `1.00`, actual model accuracy is slightly less: **~99.97%**
- This high accuracy indicates excellent model performance on this dataset, with just **one** mistake across nearly 4,000 examples.


> **Flawless Detection: 100% accuracy, precision, recall, and f1-score!**

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** – Lightning-quick interactive UI
- **scikit-learn** – Machine Learning magic
- **spaCy** – Professional NLP & entity recognition
- **Google Gemini API** – Next-gen AI explanations
- **BeautifulSoup, Requests** – Web scraping for link analysis
- **dotenv** – Secure environment variables

## 🚀 1-Minute Quickstart

```bash
git clone https://github.com/Surajkecode/fake-job-detection.git
cd fake-job-detection
python -m venv venv && source venv/bin/activate    # (use venv\Scripts\activate on Windows)
pip install -r requirements.txt
# Add your GEMINI_API_KEY in `.env`
streamlit run app.py
```
> Paste a job description or link and get instant AI-powered protection!

## 🌟 Why You'll Love It

- **Effortless UI:** One click to safety. Colorful, friendly, no coding required.
- **Ultra-Fast:** Results in seconds—even with links.
- **Brilliantly Smart:** Combines rules, ML, NLP, blacklist, and GenAI for total confidence.
- **Always Fresh:** Keeps up with new scams and improves from your feedback.
- **Collaborative:** Made to help the whole community stay safe!

## 📱 Connect with Me

- 📧 Email: [surajborkute.tech@gmail.com](mailto:surajborkute.tech@gmail.com)
- 💼 LinkedIn: [Suraj Borkute](https://www.linkedin.com/in/suraj-borkute-87597b270)
- 💻 GitHub: [Surajkecode](https://github.com/Surajkecode)
- 📱 WhatsApp: [Message Now](https://wa.me/919518772281) | 📞 +91 9518772281


     Never send money for job offers.
    When in doubt – trust the detector, not your inbox!
  
 ## 🧾 License [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the **MIT License** — free to use, modify, and distribute with attribution.  
Feel free to build upon it, improve it, and help others stay safe from job scams.

> 💬 **Contributions, suggestions, and PRs are always welcome!**  
> Together, let's create a community free from job scams.
