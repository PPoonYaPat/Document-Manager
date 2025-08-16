# 📄 Document Manager

## 🎯 About

Document Manager is software that allows users to edit PDF documents, integrated with LLM and RAG for automatically retrieving and editing documents. This software is a component of the Sagi project, available at [Sagi](https://github.com/Kasma-Inc/Sagi).

## ✨ Features

- **PDF to HTML Conversion**: Convert PDF documents to editable HTML format
- **LLM Integration**: Leverage LLM for intelligent document processing
- **RAG Capabilities**: Retrieval-Augmented Generation for context-aware editing
- **Interactive Editor**: Web-based document editor

## 🔜 Coming Soon

- Interactive Web UI
- Local OCR model inference on your device

## 🚀 Quick Start

**System Requirements:**
- Docker and Docker Compose ([Installation Guide](dev/prerequisite.md))

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/PPoonYaPat/Document-Manager.git
cd Document-Manager
```

#### 2. Environment Setup
```bash
cp .env.example .env
```

**Configure your `.env` file:**
- `LLM_API_KEY` - Your LLM API key
- `LLM_BASE_URL` - Your LLM endpoint URL  
- `VOYAGE_API_KEY` - Your [Voyage API key](https://www.voyageai.com/)
- Additional environment variables for running [MonkeyOCR](https://github.com/Yuliang-Liu/MonkeyOCR) on cloud service

#### 3. Build Docker Container
```bash
chmod +x dev/setup.sh
./dev/setup.sh
```

#### 4. Access the Container

**Option A:** VSCode Remote Container (Recommended)
- Use [VSCode Remote Container](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

**Option B:** Terminal Access
```bash
docker exec -it "$(whoami)_doc-manager-dev" /bin/bash
```

#### 5. Install Dependencies

**Method A:** Using pip
```bash
pip install -e .
```

**Method B:** Using uv (Faster)
```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

## 📖 Usage

### Prerequisites
Ensure you're in the virtual environment:
```bash
source .venv/bin/activate
```

### Step 1: Prepare MonkeyOCR
Edit `magic_pdf/libs/draw_bbox.py` in [MonkeyOCR](https://github.com/Yuliang-Liu/MonkeyOCR) using [new_draw_bbox.py](temp/new_draw_bbox.py)

### Step 2: Convert PDF to Editable HTML
```bash
python parse.py -f <input_path> -o <output_dir>
```

**Parameters:**
- `input_path` - Path to your PDF file
- `output_dir` - Output directory for results

**Output Structure:**
```
output_dir/
├── page_info/           # JSON data for each page from OCR
├── components/          # Extracted non-text components
├── final.html          # Converted HTML document
└── final_editable.html # Editable version with editor
```

### Step 3: Start the Backend Server
```bash
python main_server.py -d <output_dir>
```

**Note:** The server uses Anthropic by default. Check `model_client` in [main_server.py](main_server.py) to configure your preferred LLM provider.

**Parameters:**
- `output_dir` - Directory containing the HTML files from Step 2

### Step 4: Start Editing
Open `final_editable.html` in your browser to begin editing your document with AI assistance.