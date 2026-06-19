# Internal SOP: Application Tailoring Runbook

This document defines the operational workflow for formatting inputs, managing local credentials, interpreting fit checkpoint logs, and executing the `ai-driven-career-compiler` pipeline.

---

## 1. Directory Structure Blueprint

Ensure your local root directory matches the layout outlined in the primary `README.md` before initiating execution. The `artifacts/Real_Master_Profile.txt` and target job configurations must be fully populated.

---

## 2. Input File Preparation Guide

### A. The Master Profile (`/artifacts/`)
*   **File Naming:** Must be named exactly `Real_Master_Profile.txt` or `master_profile.txt`.
*   **Data Depth:** Include all chronological metrics, software stacks, budgets, and operational scale data. Do not pre-edit; the orchestration matrix strips noise dynamically during execution.

### B. The Target Job Description (`/job_descriptions/`)
*   **File Naming:** Save as explicit lowercase slugs denoting the company or job title (e.g., `nato_program_manager.txt`).
*   **Formatting:** Paste the entire text block from the job board directly into the file.

---

## 3. Step-by-Step Execution Workflow

### Step 1: Initialize the Engine
Open your terminal inside the project root directory and execute:
```bash
python generator.py

```

### Step 2: Select Target Matrix Role

The script will display a numbered roster of available job description text files discovered in your environment.

* **Action:** Type the **integer index number** (e.g., `3`) corresponding to your target role and hit Enter. Do not type out the string filename.

### Step 3: Evaluate Phase 1 Fit Assessment Logs

The platform will automatically parse both inputs and display an alignment scorecard:

* **💎 CORE ALIGNMENT STRENGTHS:** Highlights exactly where your background matches critical keywords and scales.
* **⚠️ POTENTIAL GAPS & BLINDSPOTS:** Displays architectural or tool gaps that could trigger interview questions or ATS automated rejections.

### Step 4: Acknowledge Gating Thresholds

* **If Match Score $\ge 80\%$:** The script logs a validation clearance success indicator and bypasses directly into asset compilation automatically.
* **If Match Score $< 80\%$:** The pipeline encounters a hard code halt condition. It warns you of high rejection probability.
* *To abort:* Type `n` to safely terminate the process without burning token resources.
* *To bypass:* Type `y` to acknowledge the technical gaps and override the compiler to build assets anyway.



### Step 5: Asset Retrieval & Quality Audit

Once the terminal logs `[COMPLETE]`, navigate to your newly created local `/output_resumes` directory to review the generated markdown files (`_resume.md` and `_cover_letter.md`).

---

## 4. Maintenance & Security Contingencies

* **Authentication Faults:** If you hit API call restrictions, rotate your token in `apikey.txt` and verify that the file remains properly tracked by your `.gitignore`.
* **Prompt Architecture Modification:** To alter structural formatting, language tone, or styling rules, directly adjust instructions within `prompt.txt` (Resume) or `prompt_cl.txt` (Cover Letter). Avoid altering core backend orchestration loops inside `generator.py`.