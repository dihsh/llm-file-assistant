# LLM File Assistant & Tool Calling Engine

**Author:** Divyansh Sharma ([@dihsh](https://github.com/dihsh))  
**Project Repository:** [https://github.com/dihsh/llm-file-assistant](https://github.com/dihsh/llm-file-assistant)  
**Primary LLM Engine:** Google Gemini (Free Tier API via Google AI Studio)  

---

## Overview

The **LLM File Assistant** is an agentic Python system that bridges Large Language Models with local document storage through **Structured Function Calling (Tool Use)**. Powered by the **free Google Gemini API** (`gemini-2.5-flash`), this project empowers an LLM to inspect directories, extract text from multi-format resume documents (`.pdf`, `.docx`, `.txt`), execute case-insensitive contextual searches, and programmatically write candidate summaries to disk.

By leveraging Google Gemini's generous free tier, this project provides a 100% free-to-run, enterprise-grade tool-calling architecture without requiring paid API subscriptions.

---

## Key Features & Learning Objectives

1. **LLM Function Calling / Tool Use**: Implement structured JSON schemas (`TOOLS_SCHEMA`) and handle the cyclical tool-calling execution loop (User Query → Gemini Tool Decision → Tool Execution → Result Return → Final Synthesis).
2. **Powered by Gemini Free API**: Seamlessly integrates with Google AI Studio's free Gemini API key (`GEMINI_API_KEY`) and supports OpenAI / local models as well.
3. **Structured Tool Interfaces**: Robust, type-hinted Python functions returning standardized dictionaries with error handling and metadata.
4. **File I/O Operations**: Programmatic directory discovery, safe parent directory creation, and UTF-8 disk writes.
5. **Multi-Format Document Parsing**: Text extraction across binary PDF (`pypdf`), Microsoft Word (`python-docx`), and plain text (`txt`) files.

---

## Architecture & Tool-Calling Loop

```
+-------------------------------------------------------------------------+
|                               USER QUERY                                |
|             "Find resumes mentioning Python experience"                 |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                      GOOGLE GEMINI 2.5 FLASH                            |
|             (Google AI Studio Free Tier via GEMINI_API_KEY)             |
|               Analyzes intent against `TOOLS_SCHEMA`                    |
+-------------------------------------------------------------------------+
                                    |
                                    v
                         Emits Tool Call Request:
            `search_in_file(filepath='resume_john_doe.pdf', keyword='Python')`
                                    |
                                    v
+-------------------------------------------------------------------------+
|                          `fs_tools.py`                                  |
|         - Reads file content (PDF/DOCX/TXT)                             |
|         - Searches case-insensitively with regex                        |
|         - Extracts line numbers and contextual snippets                 |
+-------------------------------------------------------------------------+
                                    |
                                    v
                    Returns Structured JSON Result:
       `{"status": "success", "total_matches": 5, "matches": [...]}`
                                    |
                                    v
+-------------------------------------------------------------------------+
|                          FINAL SYNTHESIS                                |
|     Gemini summarizes qualified candidates with factual evidence        |
+-------------------------------------------------------------------------+
```

---

## Part A: Core File System Tools (`fs_tools.py`)

`fs_tools.py` provides four core operations designed specifically for LLM tool use:

### 1. `read_file(filepath: str) -> dict`
- **Supported Formats:** `.pdf` (via `pypdf`), `.docx` (via `python-docx`), `.txt` (UTF-8 / Latin-1 fallback).
- **Extracted Metadata:** File name, extension, size in bytes, last modified timestamp (ISO-8601), and page count (for PDFs).
- **Error Handling:** Gracefully handles non-existent paths, directories, and unsupported formats without crashing.

### 2. `list_files(directory: str, extension: str = None) -> list`
- Scans directory contents and returns structured file metadata.
- Supports flexible extension filtering (e.g., `'.pdf'`, `'pdf'`, `'.docx'`).
- Returns sorted metadata list including name, full path, file size, and modified date.

### 3. `write_file(filepath: str, content: str) -> dict`
- Writes text content safely with UTF-8 encoding.
- Automatically creates nested parent directories if they do not already exist.
- Returns status, written path, and byte count.

### 4. `search_in_file(filepath: str, keyword: str) -> dict`
- Reads file content and performs case-insensitive regex search.
- Computes 1-based line numbers.
- Extracts surrounding textual snippets (window of 60 characters before and after match) with ellipsis indicators for context.

---

## Part B: LLM Integration (`llm_file_assistant.py`)

`llm_file_assistant.py` binds `fs_tools.py` with the LLM agent:

- **Primary Engine: Google Gemini Free API**:
  - Connects using `GEMINI_API_KEY` from Google AI Studio.
  - Employs `gemini-2.5-flash` for high-speed, cost-free function calling.
- **Secondary Engine: OpenAI & Local Models**:
  - Supports `OPENAI_API_KEY` or custom local endpoints like Ollama (`OPENAI_BASE_URL`).
- **Autonomous Engine / Offline Demo Mode**:
  - Includes a deterministic function-calling engine for automated testing, grading, and recording the demo video (`--demo`) with or without an active internet connection.

---

## Sample Dataset (`resumes/`)

The repository includes 8 diverse, realistic synthetic resumes across multiple engineering disciplines:

| File Name | Format | Candidate Name | Primary Specialization |
| :--- | :---: | :--- | :--- |
| `resume_john_doe.pdf` | PDF | John Doe | Senior Python & Backend Engineer (FastAPI, Redis) |
| `resume_jane_smith.docx` | DOCX | Jane Smith | Full Stack Developer (React, Node.js, Python) |
| `resume_alex_kumar.txt` | TXT | Alex Kumar | Machine Learning Engineer (PyTorch, LangChain, Python) |
| `resume_emily_chen.pdf` | PDF | Emily Chen | Senior Data Scientist (Python, Pandas, SQL) |
| `resume_michael_brown.docx` | DOCX | Michael Brown | DevOps & Cloud Architect (Kubernetes, AWS, Go) |
| `resume_sarah_patel.txt` | TXT | Sarah Patel | Frontend UI/UX Engineer (React, TypeScript, CSS) |
| `resume_david_wilson.pdf` | PDF | David Wilson | Cybersecurity Specialist & SRE (Python, Linux) |
| `resume_priya_sharma.docx` | DOCX | Priya Sharma | AI Research Scientist (LLMs, Transformers, Python) |

---

## Setup & Free Gemini API Configuration

### 1. Clone the Repository
```bash
git clone https://github.com/dihsh/llm-file-assistant.git
cd llm-file-assistant
```

### 2. Setup Virtual Environment & Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
.venv\Scripts\activate     # On Windows

pip install -r requirements.txt
```

### 3. Configure Free Gemini API Key
1. Get your free API key at **[https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)** (no credit card required).
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Set your free Gemini API key in `.env`:
   ```ini
   GEMINI_API_KEY=your_gemini_free_api_key_here
   OPENAI_MODEL=gemini-2.5-flash
   ```

*(Note: If you run without an API key, the assistant automatically runs in Autonomous Function-Calling Simulator Mode).*

---

## Verification & Usage

### 1. Run Unit Tests (14 Tests)
```bash
python -m unittest test_fs_tools.py -v
```

### 2. Run Automated 3-Query Demo
Executes the three canonical assignment queries in sequence:
```bash
python llm_file_assistant.py --demo
```
**Queries Demonstrated:**
1. `Read all resumes in the resumes folder`
2. `Find resumes mentioning Python experience`
3. `Create a summary file for resume_john_doe.pdf`

### 3. Run Direct Queries via CLI
```bash
python llm_file_assistant.py "Find resumes mentioning Python experience"
```

### 4. Interactive Chat Session
```bash
python llm_file_assistant.py
```

---

## Demo Video Script

See [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for the 2-3 minute presentation script, narration essay, and screen recording guide tailored for Divyansh Sharma.

---

## Project Structure

```
llm-file-assistant/
|-- fs_tools.py             # Part A: Core file system tools & schemas
|-- llm_file_assistant.py   # Part B: LLM function calling agent (Gemini / OpenAI)
|-- generate_resumes.py     # Programmatic generator for dummy resume files
|-- test_fs_tools.py        # Automated unit test suite (14 test cases)
|-- requirements.txt        # Python package dependencies
|-- .env.example            # Environment variables template (Gemini / OpenAI)
|-- .gitignore              # Git ignore rules
|-- DEMO_SCRIPT.md          # 2-3 minute video presentation script & narration
|-- README.md               # Complete project documentation
|-- resumes/                # Sample resumes dataset (PDF, DOCX, TXT)
|   |-- resume_john_doe.pdf
|   |-- resume_jane_smith.docx
|   |-- resume_alex_kumar.txt
|   |-- resume_emily_chen.pdf
|   |-- resume_michael_brown.docx
|   |-- resume_sarah_patel.txt
|   |-- resume_david_wilson.pdf
|   `-- resume_priya_sharma.docx
`-- summaries/              # Generated candidate summaries output folder
    `-- summary_john_doe.txt
```
