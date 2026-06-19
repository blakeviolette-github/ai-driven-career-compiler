# AI Career Compiler

## What is this?
This tool acts as a selective, highly critical executive recruiter that evaluates your background against a specific job application *before* you apply. It tells you exactly how well you match, exposes potential interview traps or gaps, and automatically builds a resume and cover letter tailored to survive strict automated corporate filtering (ATS).

---

## What problem does it solve?
1. **Rejection Blindness:** Most applicants apply blindly to jobs without realizing their resume is missing explicit keywords, scales, or tools requested by the job post, leading to automated rejections.
2. **Burnout from Manual Tailoring:** Rewriting your resume and cover letter for every single job application takes hours. This system handles the alignment instantly without losing your actual metrics or career scale.

---

## How it works (In Plain English)

### 1. The Gatekeeper (Fit Check)
When you point the tool at a job description, it doesn't just start writing. It runs a deep evaluation comparison first and breaks its findings down on your screen:
* **Your Strengths:** Where your background perfectly satisfies the role's constraints.
* **Your Blindspots:** Where you are weak, missing software keywords, or lacking specific scale (e.g., if the job asks for a $5M budget and your history only shows $1M).
* **The 80% Rule:** If your background matches less than 80% of what the employer wants, the tool halts. It warns you that you are at high risk of a fast rejection, saving you from spending time or effort on a bad-fit application unless you explicitly tell it to force a build anyway.

### 2. The Tailoring Engine
If you pass the 80% match requirement (or force an override), the engine analyzes your master career history, filters out irrelevant noise, and reformats your experience to align perfectly with what the hiring manager is looking for. 

It outputs two ready-to-use files inside an output folder:
* A tailored, data-driven **Resume**.
* A highly specific **Cover Letter** built around structural hooks found in that job description.

---

## Technical Specifications

An automated, two-phase prompt orchestration engine that evaluates executive-level profiles against specific job descriptions, calculates an ATS compliance fit score, reports strengths and alignment blindspots, and compiles hyper-tailored application assets (Resumes & Cover Letters).

### 🚀 Key Engineering Features

*   **Phase 1: Deep Fit Check Matrix:** Evaluates your master ledger against a target job description using an LLM-driven ATS validation prompt. Returns structural strengths and interview blindspots.
*   **Automated 80% Compliance Gate:** Automatically pauses execution if your background matches less than 80% of the target role's core constraints, protecting token usage and warning you of high rejection risks.
*   **Phase 2: Contextual Tailoring:** Deeply injects structural hooks and metrics alignment into your tailored assets using dedicated engineering prompt templates.

### 📁 Project Directory Layout

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

### 🛠️ Quick Start

1. Provide your OpenAI API key in a raw text file named `apikey.txt` in the root folder.
2. Drop your master career ledger into `artifacts/Real_Master_Profile.txt`.
3. Drop your target job descriptions as text files into the `job_descriptions/` directory.
4. Execute the pipeline terminal script:

```bash
   python generator.py

```

5. Enter the numeric option corresponding to your target job when prompted by the terminal menu.