# 📄 Document Manager

## 🎯 About

Document Manager is a software tool that enables users to edit PDF documents, integrated with LLM and RAG capabilities for automatic document retrieval and editing. This software is a component of the Sagi project, available at [Sagi](https://github.com/Kasma-Inc/Sagi).

## ✨ Features

- **PDF to HTML Conversion**: Convert PDF documents to editable HTML format
- **LLM Integration**: Leverage LLM for intelligent document processing
- **RAG Capabilities**: Retrieval-Augmented Generation for context-aware editing
- **Interactive Editor**: Web-based document editor

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
- Additional environment variables for running [DotsOCR](https://github.com/rednote-hilab/dots.ocr) on a cloud service. You may skip these if you want to run locally.

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

**Option A:** Using pip
```bash
pip install -e .
```

**Option B:** Using uv (Faster)
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

### Step 1: Prepare DotsOCR
Choose one of the following options to set up DotsOCR for document processing:

**Option A: Cloud Service Setup**
- Deploy DotsOCR on your preferred cloud service provider
- Update the cloud service environment variables in your `.env` file

**Option B: Local Installation**
- Clone and set up the DotsOCR repository by following the [installation instructions on GitHub](https://github.com/rednote-hilab/dots.ocr)
- Install anywhere on your system - only the extraction results are needed

**Option C: Web Interface**
- Use the online DotsOCR service at [dotsocr.xiaohongshu.com](https://dotsocr.xiaohongshu.com/)
- Process your documents directly through the web interface

### Step 2: Set the Model Client

Configure your AI models in [model_client.py](model_client.py) :

- **`model_client`** : Claude Sonnet 4 (main processing)
- **`small_model_client`** : Claude Haiku 3.5 (lightweight tasks)

You can change to your preferred models by following the [Autogen model configuration guide](https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/tutorial/models).

**NOTE:** The quality of extraction and editing also depends on the model used, so you may balance between model quality and cost.

### Step 3: Convert PDF to Editable HTML
**Option A:** Running on a cloud service
```bash
python parse.py -f <input_path> -o <output_dir>
```

**Parameters:**
- `input_path` - Path to your PDF file
- `output_dir` - Output directory for results

**Output Structure:**
```
output_dir/
├── ocr_output/           # result from DotsOCR
|    ├── filename_nohf.md
|    ├── filename.json
|    └── filename.md
├── components/           # Extracted non-text components
├── final.html            # Converted HTML document
└── final_editable.html   # Editable version with editor
```

**Option B:** Running locally
```bash
python parse.py -f <input_path> -o <output_dir> -l <json_file>
```

**Parameters:**
- `input_path` - Path to your PDF file
- `output_dir` - Output directory for results
- `json_file` - JSON result from running DotsOCR locally

**Output Structure:**
```
output_dir/
├── components/           # Extracted non-text components
├── final.html            # Converted HTML document
└── final_editable.html   # Editable version with editor
```

### Step 4: Start the Backend Server
```bash
python main_server.py -d <output_dir>
```


**Parameters:**
- `output_dir` - Directory containing the HTML files from Step 2

### Step 5: Start Editing
Open `final_editable.html` in your browser to begin editing your document with AI assistance.