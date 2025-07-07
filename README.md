# 📰 Web to EPUB Converter

Convert multiple webpages into a clean, offline-friendly EPUB eBook — with optional cover image, author info, and auto-generated Table of Contents.

## ✨ Features

- ✅ Convert multiple article/blog URLs into an EPUB
- 🖼️ Upload your own cover image (JPEG)
- 📝 Set custom title & author
- 🔗 Built-in URL list generator (e.g., `chapter001` to `chapter100`)
- 📑 Automatically extracts readable content and titles using [newspaper3k](https://github.com/codelucas/newspaper)

---

## 🚀 Demo

Live deployable via [Render.com](https://render.com), or run locally with Docker.

---

## 🧪 How to Use (Locally)

### 1. Clone and install dependencies

```bash
git clone https://github.com/yourusername/web-to-epub.git
cd web-to-epub
pip install -r requirements.txt
2. Run it
bash
Copy
Edit
python app.py
Open your browser at http://127.0.0.1:5000

🌐 Deploy on Render (Free)
1. Push to GitHub
bash
Copy
Edit
git init
git add .
git commit -m "Initial commit"
gh repo create web-to-epub --public --source=. --remote=origin --push
2. Go to https://render.com
Create a New Web Service:

Build Command: (leave blank)

Start Command: gunicorn app:app

Environment: Python 3

Add environment variable:

PORT = 10000 (used by render.yaml)

🐳 Run with Docker
bash
Copy
Edit
docker build -t web-to-epub .
docker run -p 5000:5000 web-to-epub
📦 File Structure
graphql
Copy
Edit
web_to_epub/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── Dockerfile             # For container deployment
├── render.yaml            # One-click deploy on Render
└── templates/
    └── index.html         # Frontend with URL generator
📚 Credits
EbookLib — EPUB generation

newspaper3k — Article parsing

Flask — Lightweight web framework
