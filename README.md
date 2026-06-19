# AI-Driven Career Compiler

An automated, two-phase prompt orchestration engine that evaluates executive-level profiles against specific job descriptions, calculates an ATS compliance fit score, reports strengths and alignment blindspots, and compiles hyper-tailored application assets (Resumes & Cover Letters).

## 🚀 Key Features

*   **Phase 1: Deep Fit Check Matrix:** Evaluates your master ledger against a target job description using an LLM-driven ATS validation prompt. Returns structural strengths and interview blindspots.
*   **Automated 80% Compliance Gate:** Automatically pauses execution if your background matches less than 80% of the target role's core constraints, protecting token usage and warning you of high rejection risks.
*   **Phase 2: Contextual Tailoring:** Deeply injects structural hooks and metrics alignment into your tailored assets using dedicated engineering prompt templates.

---

## 📁 Project Directory Layout

Ensure your local directory structure perfectly matches the blueprint below:

```text
.
├── artifacts/
│   ├── sample_profile.txt       # Public reference mockup
│   └── Real_Master_Profile.txt  # Your actual unedited career ledger (Git-ignored)
├── job_descriptions/
│   ├── sample_job.txt           # Public reference mockup
│   └── target_role_name.txt     # The JDs you want to target (Git-ignored)
├── apikey.txt                   # Local raw OpenAI API Key string (Git-ignored)
├── generator.py                 # Core pipeline orchestration script
├── prompt.txt                   # Resume engineering core instructions
├── prompt_cl.txt                # Cover letter engineering core instructions
└── USAGE_SOP.md                 # Execution runbook

```

---

## 🛠️ Quick Start

1. Provide your OpenAI API key in a raw text file named `apikey.txt` in the root folder.
2. Drop your master career ledger into `artifacts/Real_Master_Profile.txt`.
3. Drop your target job descriptions as text files into the `job_descriptions/` directory.
4. Execute the pipeline terminal script:

```bash
   python generator.py

```

5. Enter the numeric option corresponding to your target job when prompted by the terminal menu.