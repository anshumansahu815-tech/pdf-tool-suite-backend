# PDF Tool Suite Backend 📄🚀

A high-performance Flask-based REST API designed for fast, in-memory processing of PDF documents. This tool extracts structural text and images without any local storage overhead.

## ✨ Key Features
* **In-Memory Extraction:** Uses `PyMuPDF` to convert PDF pages directly to Base64 strings for instant frontend rendering.
* **Smart Parsing:** Engineered regular expression algorithms to automatically detect and extract document subsections.
* **Zero Footprint:** No temporary files are saved on the server, ensuring security and speed.
* **RESTful Architecture:** Clean API endpoints for seamless integration with any modern frontend.

## 🛠️ Tech Stack
* **Language:** Python
* **Framework:** Flask
* **Libraries:** PyMuPDF (fitz), Regex, Flask-CORS

## 🚀 Getting Started
1. Clone the repo: `git clone https://github.com/anshumansahu815-tech/pdf-tool-suite-backend.git`
2. Install dependencies: `pip install flask flask-cors PyMuPDF`
3. Run the server: `python app.py`
