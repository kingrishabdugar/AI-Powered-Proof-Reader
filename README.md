# AI-Powered Proof-Reader for Indic Religious Documents

![App Demo](https://via.placeholder.com/800x400?text=App+Demo+GIF) <!-- Replace with actual GIF or screenshot link for interactivity -->

This is an **AI-Powered Proof-Reader** built with Streamlit, designed specifically for correcting and identifying words in documents related to Indic religions (e.g., Hinduism, Buddhism, Jainism). It focuses on Hindi words that may be archaic, specialized, or unavailable in traditional vocabularies, using vector search and Gemini AI for intelligent suggestions.

The app extracts unique Hindi words from DOCX files, compares them against a custom dictionary, suggests corrections via semantic similarity, and allows interactive user approval before replacing them in the document.

## Features
- **Hindi Word Extraction**: Automatically pulls unique Devanagari-script words from DOCX files, filtering for Hindi using language detection.
- **Vector-Powered Spell Checking**: Uses Gemini API embeddings and FAISS for efficient, semantic similarity-based corrections (e.g., matching rare religious terms like "प्राणायाम" even if slightly misspelled).
- **Interactive Workflow**: Step-by-step Streamlit interface with approvals, bulk actions, real-time feedback, and progress indicators.
- **Custom Dictionary Support**: Upload your own TXT dictionary tailored to Indic religious terminology.
- **Output Handling**: Generates corrected DOCX files prefixed with "Corrected_".
- **Efficiency & Cloud-Ready**: Caching, batching, and error handling for smooth performance; deployable to Streamlit Cloud.
- **Fallback Mechanisms**: Switches to sentence-transformers if Gemini API issues arise.

This tool is ideal for scholars, researchers, or enthusiasts working with Sanskrit-influenced Hindi texts in religious contexts, where standard spell-checkers fail due to uncommon vocabulary.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/ai-proof-reader.git
   cd ai-proof-reader
   ```

2. Install dependencies from `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```

   **requirements.txt** (included in repo):
   ```
   streamlit==1.37.1
   python-docx==1.1.2
   google-generativeai==0.7.2
   sentence-transformers==3.0.1
   faiss-cpu==1.8.0
   langdetect==1.0.9
   regex==2024.7.24
   ```

3. Set up your Gemini API key:
   - Get a free key from [Google AI Studio](https://aistudio.google.com/).
   - For local run: `export GEMINI_API_KEY='your_key'`.
   - For Streamlit Cloud: Add to `secrets.toml` in your repo: `GEMINI_API_KEY = "your_key"`.

## Usage

1. Run the app locally:
   ```
   streamlit run app.py
   ```

2. In the app:
   - Upload a DOCX file (e.g., a document with Hindi religious text).
   - Upload a custom dictionary TXT (one word per line, e.g., "अहिंसा", "कर्म").
   - Follow the interactive steps: Extract words, review suggestions, approve changes, and download the corrected file.

   Example: For a document with a misspelled "ध्यान" as "धयान", the app suggests corrections based on vector similarity to dictionary terms.

3. Interactive Elements:
   - **Checkboxes for Approvals**: Approve one-by-one or all at once.
   - **Progress Spinners**: For embeddings and processing.
   - **Error Handling**: User-friendly messages for issues like invalid files or API errors.

## Deployment to Streamlit Cloud

1. Push your repo to GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io/), connect your GitHub account, and create a new app.
3. Select your repo and branch.
4. In app settings:
   - Set Python version to 3.10+.
   - Add secrets (e.g., GEMINI_API_KEY).
5. Deploy! The app will be live at a shareable URL.

For other clouds (e.g., Heroku), use the same `requirements.txt` and add a `Procfile`: `web: streamlit run --server.port $PORT app.py`.

## Contributing

We welcome contributions, especially for expanding to other Indic languages (e.g., Sanskrit, Tamil) or improving religious vocabulary datasets!

1. Fork the repo.
2. Create a feature branch: `git checkout -b feature/new-lang-support`.
3. Commit changes: `git commit -m "Add Sanskrit support"`.
4. Push: `git push origin feature/new-lang-support`.
5. Open a Pull Request.

## Contact

For questions or suggestions, open an issue or reach out to [rishabdugar.jain@gmail.com].

*Built with ❤️ for preserving Indic heritage through AI.*
