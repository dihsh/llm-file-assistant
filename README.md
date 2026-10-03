# LLM File Assistant & Tool Calling Engine

**Author:** Divyansh Sharma ([@dihsh](https://github.com/dihsh))  
**Project Repository:** [https://github.com/dihsh/llm-file-assistant](https://github.com/dihsh/llm-file-assistant)  

---

## Overview

The **LLM File Assistant** is an agentic Python system that bridges Large Language Models with local document storage through **Structured Function Calling (Tool Use)**. Rather than relying on static prompts or ungrounded generative guesses, this project empowers an LLM to inspect directories, extract text from multi-format resume documents (`.pdf`, `.docx`, `.txt`), execute case-insensitive contextual searches, and programmatically write candidate summaries to disk.

---

## Learning Objectives

1. **LLM Function Calling / Tool Use**: Implement structured JSON schemas (`TOOLS_SCHEMA`) and handle the cyclical tool-calling execution loop (User Query → Model Tool Decision → Tool Execution → Result Return → Final Synthesis).
2. **Structured Tool Interfaces**: Design robust, type-hinted Python functions returning standardized dictionaries with error handling and metadata.
3. **File I/O Operations**: Programmatically handle file discovery, directory creation, and disk writes.
4. **Document Parsing & Validation**: Extract and validate textual content across binary PDF (`pypdf`), Microsoft Word (`python-docx`), and plain text (`txt`) files.

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
|                          LLM AGENTIC ENGINE                             |
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
|        LLM summarizes qualified candidates with factual evidence        |
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

`llm_file_assistant.py` binds `fs_tools.py` with an LLM agent:

- **Multi-Provider Support:**
  - **OpenAI:** Uses `OPENAI_API_KEY` (e.g. `gpt-4o-mini`, `gpt-4o`).
  - **Google Gemini:** Supports `GEMINI_API_KEY` through the OpenAI-compatible Gemini endpoint (`gemini-2.5-flash`).
  - **Local Models:** Connects to Ollama / vLLM / LocalAI via `OPENAI_BASE_URL`.
  - **Autonomous Engine / Offline Demo Mode:** If no API key is configured or when running `--demo`, the assistant uses a deterministic tool execution engine to demonstrate tool calling without requiring third-party API fees.
- **Agent Loop:**
  - Manages conversation state.
  - Automatically invokes tools requested by the model.
  - Feeds structured results back into the context.
  - Synthesizes user-friendly answers.

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

## Setup & Installation

### 1. Prerequisites
- Python 3.10+ (or Python managed via `uv`)
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/dihsh/llm-file-assistant.git
cd llm-file-assistant
```

### 3. Setup Virtual Environment & Install Dependencies
```bash
# Using standard Python venv
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
.venv\Scripts\activate     # On Windows

pip install -r requirements.txt
```

*(Optional) Using `uv`:*
```bash
uv venv
uv pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)
Copy `.env.example` to `.env` and insert your API key:
```bash
cp .env.example .env
```
*(If omitted, the assistant seamlessly runs in Autonomous Tool-Calling Mode).*

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

See [DEMO_SCRIPT.md](file:///D:/projects/llm-file-assistant/DEMO_SCRIPT.md) for the 2-3 minute presentation script, narration essay, and screen recording guide.

---

## Project Structure

```
llm-file-assistant/
|-- fs_tools.py             # Part A: Core file system tools & schemas
|-- llm_file_assistant.py   # Part B: LLM function calling agent
|-- generate_resumes.py     # Programmatic generator for dummy resume files
|-- test_fs_tools.py        # Automated unit test suite (14 test cases)
|-- requirements.txt        # Python package dependencies
|-- .env.example            # Environment variables template
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
