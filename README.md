# AI-Driven Executive Application Pipeline

An asynchronous, data-driven profile mapping engine designed to orchestrate large language models (LLMs) and programmatically compile hyper-tailored, executive-ready application packages. 

This repository decouples structural candidate data from behavioral recruiter heuristics. By feeding raw multi-source career data ("artifacts") into an automated backend data pipeline, the orchestration layer evaluates context-specific dependencies against an incoming job specification, strips out non-contextual noise, and renders visually cohesive, pixel-perfect A4 documents via a layout compilation layer.

## Architecture & Execution Strategy

1. **Decoupled Data Infrastructure Layer:** Reads raw, unparsed `.txt`, `.docx`, and `.pdf` professional histories from an isolated local boundary.
2. **Contextual Tokenization & Orchestration Layer:** Feeds a hyper-parameterized `gpt-4o-mini` engine through independent prompt vectors (`prompt.txt` and `prompt_cl.txt`). This structure isolates instructions from source text, applying strict conditional logic to include/omit domain dependencies (e.g., security clearances) dynamically based on target requirements.
3. **Behavioral Business Layer:** Inverts traditional achievement framing to implement a **Metrics-First "So-What?" Architecture**. Sentence structures are algorithmically guided to assert quantified commercial, financial, and operational ROI before explaining the underlying engineering or team leadership mechanisms.
4. **Document Layout Compilation Layer:** Consumes optimized markdown text and programmatically maps layout components onto a geometric layout engine utilizing `ReportLab` flowables to enforce strict multi-page ceilings and a uniform typographic layout.

---

## Technical Stack & Dependencies

* **Language:** Python 3.x
* **AI Core Layer:** OpenAI API Client (Contextual Chat Completions Pipeline)
* **Data Processing:** PyPDF2 (PDF ingestion), python-docx (OpenXML extraction), glob (Pattern-matching file discovery)
* **Document Compilation Assembly:** ReportLab (Flowables, SimpleDocTemplate, ParagraphStyle mapping, Canvas draw callbacks)

---

## File System Topology

```text
├── artifacts/
│   ├── sample_profile.txt       # Public mockup blueprint for master professional files
│   └── [private_dossiers].txt   # Real career master profiles (Git-ignored)
├── job_descriptions/
│   ├── sample_job.txt           # Public mockup blueprint for target requirements
│   └── [target_roles].txt       # Active target job descriptions (Git-ignored)
├── output_resumes/              # Dynamically compiled output directory (Git-ignored)
│   ├── Blake_Violette_Resume_[Job].pdf
│   └── Blake_Violette_CoverLetter_[Job].pdf
├── .gitignore                   # Production-grade system and security boundary map
├── apikey.txt                   # Secure local Open AI credential map (Git-ignored)
├── generator.py                 # Core backend automation and layout assembly pipeline
├── prompt.txt                   # Production engineering prompts for resume compilation
├── prompt_cl.txt                # Production engineering prompts for cover letter generation
└── README.md                    # System documentation