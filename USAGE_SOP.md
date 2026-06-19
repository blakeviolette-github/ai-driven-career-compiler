# Internal SOP: Application Tailoring Runbook

This document defines the operational workflow for formatting inputs, managing local credentials, and executing the `ai-driven-career-compiler` pipeline to generate targeted application assets.

---

## 1. Directory Structure Blueprint
Ensure your local root directory matches the following layout before execution:

```text
.
├── artifacts/
│   ├── sample_profile.txt       # Public reference mockup
│   └── Real_Master_Profile.txt  # Your actual unedited career ledger (Git-ignored)
├── job_descriptions/
│   ├── sample_job.txt           # Public reference mockup
│   └── target_role_name.txt     # The JD you want to apply to (Git-ignored)
├── apikey.txt                   # Local raw OpenAI API Key string (Git-ignored)
├── generator.py                 # Pipeline execution script
├── prompt.txt                   # Resume engineering core prompt
├── prompt_cl.txt                # Cover letter engineering core prompt
└── USAGE_SOP.md                 # This runbook

```

---

## 2. Input File Preparation Guide

### A. The Master Profile (`/artifacts/`)

* **File Naming:** Keep it simple (e.g., `master_profile.txt`).
* **Formatting:** Use raw text (`.txt`). Organize it chronologically or by project blocks.
* **Data Depth:** Include everything. Do not pre-edit or shorten metrics. Write out raw descriptions of team size, software stacks, budgets, and project names. The LLM orchestration engine will handle the stripping of noise dynamically.

### B. The Target Job Description (`/job_descriptions/`)

* **File Naming:** Use clear lowercase slugs based on the company and role (e.g., `apple_operations_pm.txt`, `nvidia_data_lead.txt`).
* **Formatting:** Copy and paste the entire raw text from LinkedIn, Indeed, or the corporate careers page directly into the text file. Include the company summary, requirements, and minimum qualifications.

---

## 3. Step-by-Step Execution Workflow

### Step 1: Verification Checklist

1. Ensure your OpenAI API key inside `apikey.txt` is active and contains no leading or trailing spaces.
2. Confirm that `output_resumes/` is clear or that you are ready for existing files matching the target slug to be overwritten.

### Step 2: Running the Engine

Open your terminal inside the project root directory and execute:

```bash
python generator.py

```

### Step 3: Interactive Prompt Input

The script will output a numbered list of all available job description files discovered in your folder.

* Type the exact file name (including `.txt`) when prompted:

```text
Enter the filename of the job description to run: apple_operations_pm.txt

```

### Step 4: Asset Retrieval & Quality Audit

Once the console returns `[SUCCESS]`, navigate to your local `/output_resumes` directory. Review the generated PDF files against these operational baselines:

* **Resume Geometry:** Did it comfortably fill 2 pages without triggering a trailing 3rd page?
* **Cover Letter Hook:** Does the introductory paragraph lead immediately with a high-impact, metrics-driven yield statement?
* **Bolding Verification:** Verify that corporate entities and universities are cleanly bolded using the backend canvas style.

---

## 4. Maintenance & Security Contingencies

* **Credential Rotations:** If you encounter authentication errors, rotate your OpenAI API token, update `apikey.txt`, and verify that the file remains uncommitted via `git status`.
* **Prompt Engineering Tweak Optimization:** To adjust the linguistic tone or the structural balance of the outputs, edit the core instructions inside `prompt.txt` (Resume) or `prompt_cl.txt` (Cover Letter). Do not edit the core script logic for simple copy adjustments.

```

```