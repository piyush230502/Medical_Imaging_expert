# Medical Imaging Expert

![Medical Imaging Expert Banner](https://images.unsplash.com/photo-1511174511562-5f97f4f4e0c8?auto=format&fit=crop&w=1200&q=80)

> **AI-powered medical image analysis. Upload, analyze, and get expert insights instantly.**

---

## 🚀 Overview
Medical Imaging Expert is a modern web application that leverages advanced AI (Google Gemini via the `agno` library) to analyze medical images and provide expert-level insights. Designed for healthcare professionals, researchers, and students, it offers a seamless, secure, and visually stunning user experience.

---

## ✨ Features
- **Gorgeous, Responsive UI/UX**: Built with Bootstrap 5 and custom CSS for a professional look and feel.
- **Secure API Key Management**: Configure and reset your Google API key directly from the web interface.
- **Fast Image Upload & Preview**: Upload medical images (X-rays, MRIs, etc.), with instant preview and size optimization.
- **AI-Powered Analysis**: Uses Google Gemini (via `agno`) to analyze images and return detailed, human-readable reports.
- **Automatic Cleanup**: Uploaded images are securely deleted after analysis.
- **Comprehensive Logging**: All actions are logged for transparency and debugging.

---

## 🖥️ Demo
![UI Screenshot](https://drive.google.com/file/d/1gzd_XBdaWUYDRkgApE4o-yVLZYON18XO/view?usp=sharing)

![UI Video](https://drive.google.com/file/d/1QphxpkoT7bJiOewtj2yJPnb2MiIERKTc/view?usp=sharing)

---

## 📦 Project Structure
```
Medical_Imaging_expert/
├── main.py                # Flask backend (API, logic, routing)
├── requirements.txt       # Python dependencies
├── backend/               # LLM and prompt logic
├── frontend/              # All UI/UX files (HTML, CSS, JS)
│   ├── index.html         # Main web page
│   └── static/
│       ├── style.css      # Custom styles
│       └── app.js         # Frontend logic
├── uploads/               # Temporary image storage (auto-cleaned)
└── README.md              # This file
```

---

## ⚡ Quickstart

### 1. Clone the repository
```sh
git clone https://github.com/piyush230502/Medical_Imaging_expert.git
cd Medical_Imaging_expert
```

### 2. Install dependencies
```sh
pip install -r requirements.txt
```

### 3. Set up your Google API Key
- Get a valid Google Gemini API key with image analysis access.
- You can set it as an environment variable:
  ```sh
  $env:GOOGLE_API_KEY="your-key-here"  # PowerShell
  # or
  export GOOGLE_API_KEY="your-key-here" # Bash
  ```
- Or, simply enter it in the web UI when prompted.

### 4. Run the app
```sh
python main.py
```
- Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🧑‍💻 Usage
1. **Configure API Key**: Enter your Google API key in the top section and save.
2. **Upload Image**: Select a medical image file (JPG, PNG, etc.) and click "Upload & Analyze".
3. **View Results**: The AI will analyze the image and display a detailed report.
4. **Analyze More**: Click "Analyze Another Image" to repeat.

---

## 🔒 Security & Privacy
- **API Key**: Never stored on disk; only in your session.
- **Images**: Deleted after analysis; never shared or stored long-term.
- **Logs**: Only for debugging; no sensitive data is logged.

---

## 🛠️ Tech Stack
- **Backend**: Python, Flask, agno (Google Gemini integration)
- **Frontend**: HTML5, Bootstrap 5, custom CSS/JS
- **Image Processing**: Pillow (PIL)

---

## 📚 Customization
- Edit `frontend/index.html`, `style.css`, or `app.js` for UI changes.
- Update `backend/llm.py` or `backend/prompt.py` to change AI logic or prompts.

---

## ❓ FAQ
**Q: What image types are supported?**
> JPG, PNG, and most common medical image formats.

**Q: Is my data safe?**
> Yes. Images are deleted after analysis and API keys are never stored on disk.

**Q: Can I use another AI model?**
> Yes, by modifying the backend logic in `backend/llm.py`.

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License
This project is licensed under the MIT License.

---

## 🙏 Acknowledgements
- [Google Gemini](https://ai.google.dev/gemini-api/docs)
- [agno Python Library](https://pypi.org/project/agno/)
- [Bootstrap](https://getbootstrap.com/)
- [Unsplash Medical Images](https://unsplash.com/s/photos/medical)

---

> Made with ❤️ for the future of healthcare.
