# Video Presentation Script & Speech Essay: LLM Tool Calling in Action

**Presenter:** Divyansh Sharma  
**Project:** LLM File Assistant & Core File System Tools  
**Duration:** 2 to 3 Minutes  
**Demonstration:** Terminal & Code Walkthrough  

---

## 1. Complete Speech Essay / Paragraph (What to Say in the Video)

> "Hello everyone, my name is Divyansh Sharma, and today I am excited to demonstrate my **LLM File Assistant** project, highlighting the power of **LLM Function Calling and Structured Tool Use**. 
>
> Large Language Models are exceptionally skilled at natural language reasoning, but by themselves, they cannot interact with local file systems or parse proprietary binary documents like PDFs and Word files. That is where tool calling comes in. In this project, I implemented two core components: first, a robust Python module called `fs_tools.py`, which equips the system with deterministic file operations—reading PDF, DOCX, and TXT files, listing directory files with metadata, safely writing files with automatic directory creation, and performing contextual keyword searches. 
>
> Second, in `llm_file_assistant.py`, I integrated these tools with an LLM agentic loop. When a user asks a high-level question—such as *'Find all resumes mentioning Python experience'* or *'Create a summary file for John Doe's resume'*—the language model does not guess. Instead, it inspects the JSON schemas of our tools, determines the optimal sequence of actions, and emits structured tool calls. Our Python application intercepts these function calls, executes the actual code against our sample resume database, and feeds the structured results back into the model's context. The LLM then synthesizes a verified, factual response and can even persist output files directly onto disk. 
>
> In this demo, you will see the assistant list and parse diverse resume formats, perform case-insensitive keyword searches with surrounding contextual snippets, and generate candidate summary files on the fly. This architecture demonstrates how combining the reasoning capability of LLMs with deterministic, structured tools unlocks reliable, enterprise-grade AI automation."

---

## 2. Minute-by-Minute Video Recording Timeline (2 - 3 Minutes)

### [0:00 – 0:35] Introduction & Learning Objectives
* **Screen Display:** Project folder open in VS Code / Terminal showing `fs_tools.py` and `resumes/`.
* **Spoken Script:**
  > *"Hi everyone, I am Divyansh Sharma. Today, I'll be demonstrating the LLM File Assistant project. The objective is to understand how LLMs can transition from pure text generators into autonomous agents using structured tool calling, file I/O operations, and multi-format document parsing."*
* **Action on Screen:** Briefly show the `resumes/` folder containing PDF, DOCX, and TXT files.

---

### [0:35 – 1:15] Part A: Core File System Tools (`fs_tools.py`) & Unit Tests
* **Screen Display:** Open `fs_tools.py`, scroll past `read_file`, `list_files`, `write_file`, and `search_in_file`.
* **Spoken Script:**
  > *"In Part A, I built `fs_tools.py`. Here we have four core tools: `read_file` extracts text and metadata across PDF, DOCX, and TXT files; `list_files` scans directories and filters by extension; `write_file` safely creates directories and writes files; and `search_in_file` performs case-insensitive regex searches, capturing line numbers and surrounding snippets. Let's run our automated test suite to verify all tools."*
* **Action on Screen:** In terminal, run:
  ```bash
  python -m unittest test_fs_tools.py -v
  ```
  Highlight the output: `Ran 14 tests ... OK`.

---

### [1:15 – 2:15] Part B: LLM Tool Calling in Action
* **Screen Display:** Terminal executing `llm_file_assistant.py --demo`.
* **Action on Screen:** In terminal, run:
  ```bash
  python llm_file_assistant.py --demo
  ```
* **Spoken Script (Query 1 - Reading Resumes):**
  > *"Now let's see tool calling in action. In our first query: 'Read all resumes in the resumes folder', notice what happens. The agent first calls `list_files` on the resumes directory. Upon receiving the file list, it sequentially calls `read_file` for each PDF, DOCX, and TXT file, extracting metadata and contents before presenting a consolidated overview."*
* **Spoken Script (Query 2 - Skill Search):**
  > *"Next, the query is: 'Find resumes mentioning Python experience'. Instead of hallucinating, the agent issues `search_in_file` calls for each candidate. It detects that John Doe, Jane Smith, Alex Kumar, Emily Chen, and Priya Sharma have verified Python experience, extracting exact contextual quotes from the files."*
* **Spoken Script (Query 3 - File Creation):**
  > *"Finally: 'Create a summary file for resume_john_doe.pdf'. The model reads John Doe's PDF resume, extracts his skills and achievements, and calls `write_file` to persist `summary_john_doe.txt` into a new `summaries` folder."*

---

### [2:15 – 2:45] Verification & Conclusion
* **Screen Display:** Open `summaries/summary_john_doe.txt` to show the persisted file.
* **Spoken Script:**
  > *"Opening `summary_john_doe.txt`, we see the complete structured profile created directly by the tool call. All code, sample datasets, and documentation are committed and uploaded to my GitHub repository. Thank you for watching!"*

---

## 3. Quick Commands Reference for Recording

```bash
# 1. Run unit test suite
python -m unittest test_fs_tools.py -v

# 2. Run automated 3-query demo
python llm_file_assistant.py --demo

# 3. View the generated summary file
cat summaries/summary_john_doe.txt  # Or type: Get-Content summaries\summary_john_doe.txt

# 4. Optional: Run interactive query
python llm_file_assistant.py "Find resumes mentioning Python experience"
```
