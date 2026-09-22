# Verba Translator 🌍

Verba Translator is an AI-powered multilingual translation application built with **Streamlit, FastAPI, LangChain, and Groq**. It provides a simple web interface for translating text into 25 supported languages using the `openai/gpt-oss-20b` model through Groq.

## ✨ Features

- 🌍 Translation across **25 languages**
- 🤖 Groq-powered LLM translation with `openai/gpt-oss-20b`
- 🔗 LangChain prompt → model → output pipeline
- ⚡ FastAPI backend for translation requests
- 🎨 Streamlit frontend with a clean two-panel UI
- 🧠 Session-state support for the translation interface
- 🛡️ Basic input validation and error handling
- 🔐 API key loaded securely through environment variables

## 🌐 Supported Languages

| # | Language | # | Language |
|---|---|---|---|
| 1 | French | 14 | Urdu |
| 2 | Spanish | 15 | Turkish |
| 3 | German | 16 | Dutch |
| 4 | Italian | 17 | Swedish |
| 5 | Portuguese | 18 | Polish |
| 6 | Russian | 19 | Greek |
| 7 | Japanese | 20 | Thai |
| 8 | Korean | 21 | Vietnamese |
| 9 | Chinese | 22 | Indonesian |
| 10 | Arabic | 23 | Hebrew |
| 11 | Hindi | 24 | Ukrainian |
| 12 | Bengali | 25 | Romanian |
| 13 | Czech | | |

## 🏗️ Architecture

```
┌─────────────────────┐
│   Streamlit Client  │
│      (client.py)    │
└──────────┬──────────┘
           │ POST /chain/invoke
           ▼
┌─────────────────────┐
│    FastAPI Server   │
│      (serve.py)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ LangChain Prompt    │
│   Template / Chain  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      ChatGroq       │
│ openai/gpt-oss-20b  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Translated Output   │
└─────────────────────┘
```

## 🔄 How It Works

1. Enter the text you want to translate.
2. Select the target language.
3. Streamlit sends the request to the FastAPI backend.
4. FastAPI passes the input through the LangChain translation chain.
5. Groq processes the request using `openai/gpt-oss-20b`.
6. The translated text is returned to the Streamlit interface.

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **LLM Framework:** LangChain
- **LLM Provider:** Groq
- **Model:** `openai/gpt-oss-20b`
- **Language:** Python
- **Server:** Uvicorn
- **Configuration:** python-dotenv

## 📁 Project Structure

```
verba-translator/
├── client.py
├── serve.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Tauhid-Topu-007/verba-translator.git
cd verba-translator
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit your API key to GitHub. Make sure `.env` is included in `.gitignore`.

## ▶️ Run Locally

Start the FastAPI backend:

```bash
python serve.py
```

The backend runs on:

```
http://127.0.0.1:8000
```

Then start the Streamlit frontend in another terminal:

```bash
streamlit run client.py
```

### Backend URL Configuration

The frontend sends translation requests to the backend endpoint:

```
http://127.0.0.1:8000/chain/invoke
```

For a deployed backend, configure `BACKEND_URL` in `client.py` to point to the deployed `/chain/invoke` endpoint.

## 🔌 API

### Health Check

**GET /**

```json
{
  "status": "ok",
  "message": "Backend is running"
}
```

### Translation

**POST /chain/invoke**

Request:

```json
{
  "input": {
    "language": "Bengali",
    "text": "Hello, how are you?"
  },
  "config": {},
  "kwargs": {}
}
```

Response:

```json
{
  "output": "হ্যালো, আপনি কেমন আছেন?"
}
```

## ☁️ Deployment Architecture

The application can be deployed as two services:

```
User
  │
  ▼
Streamlit Frontend
  │
  ▼
FastAPI Backend
  │
  ▼
Groq API
  │
  ▼
LLM Translation
```

Store `GROQ_API_KEY` as a deployment secret/environment variable rather than hard-coding it.

## 🔮 Future Improvements

- Automatic source-language detection
- Translation history
- Copy/download translated text
- More language support
- Streaming responses
- Authentication and usage limits
- Configurable model and temperature
- Improved deployment configuration using environment variables

## 👨‍💻 Author

**Tauhidul Islam Topu**

- GitHub: [Tauhid-Topu-007](https://github.com/Tauhid-Topu-007)

## 📄 License

No explicit license is currently defined in the repository. Add a license file if you plan to distribute the project under specific open-source terms.
