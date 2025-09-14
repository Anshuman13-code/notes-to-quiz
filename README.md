# 📚 Notes → Quiz Generator 

This is a Streamlit app that generates **5 multiple-choice questions** from lecture notes using the Gemini (or OpenAI) API.

## Features

- Generate 5 unique multiple-choice questions from your notes
- Each question has 4 options (A-D) and the correct answer
- Answers are displayed in green bold text
- Removes duplicate questions automatically
- Interactive Streamlit interface

## Getting Started

1️⃣ Clone the Repository

```bash
git clone https://github.com/Anshuman13-code/notes-to-quiz.git
cd notes-to-quiz
```
2️⃣ Set Up a Python Environment

Create a virtual environment:
```
python -m venv venv
```
Activate it:

macOS/Linux:
```
source venv/bin/activate
```

Windows CMD:
```
venv\Scripts\activate
```
Windows PowerShell:
```
venv\Scripts\Activate.ps1
```
3️⃣ Install Required Packages
```
pip install -r requirements.txt
```

If requirements.txt is not available, install manually:
```
pip install streamlit python-dotenv google-generativeai
```

4️⃣ Set Up API Keys

Create a file called api.env in the project folder:
```
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # optional
```

Important: Do NOT commit or share this file. It is ignored by GitHub.

5️⃣ Run the App
```
streamlit run app1gem.py
```

- 📝 **Paste your lecture notes in the app**
- 🚀 **Click Generate Quiz**
- 🎯 **Get 5 multiple-choice questions with answers**

---

### 📝 Notes

> ⚠️ **This app uses environment variables for security.**  
> 🌐 **The GitHub repo is public, but API keys must remain local.**  
> 🔑 **If you want to use it, get your own Gemini/OpenAI API key.**

---
