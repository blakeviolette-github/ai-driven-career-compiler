import os
import json
import sys
from openai import OpenAI

def load_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip()

def get_api_key():
    if os.path.exists("apikey.txt"):
        return load_file("apikey.txt")
    elif "OPENAI_API_KEY" in os.environ:
        return os.environ["OPENAI_API_KEY"]
    else:
        print("[ERROR] No API key found. Place your key in 'apikey.txt'.")
        sys.exit(1)

def run_fit_assessment(client, profile, jd):
    """
    Phase 1: Evaluates the candidate profile against the JD.
    Forces OpenAI to return a strict JSON payload tracking strengths and gaps.
    """
    print("\n[PHASE 1] Initializing Core Executive Fit Assessment...")
    
    system_prompt = (
        "You are an elite executive recruiter and automated applicant tracking system (ATS) validator.\n"
        "Compare the provided Master Profile against the target Job Description.\n"
        "Evaluate technical stack alignment, operational scale, metrics, and core experience constraints.\n"
        "Identify major strengths and any gaps (even minor ones if the profile is a strong match).\n"
        "You MUST respond ONLY with a strictly valid JSON object matching this identical schema:\n"
        "{\n"
        '  "fit_score": 85,\n'
        '  "strengths": [\n'
        '    "Perfect alignment on SQL/Python pipeline orchestration scale (150PB+ data scale)."\n'
        '  ],\n'
        '  "gaps": [\n'
        '    "Minor Gap: Job mentions Snowflake, but profile explicitly focuses on AWS Redshift."\n'
        "  ]\n"
        "}\n"
        "Do not include markdown wrappers like ```json or any conversational text. Return raw JSON text only."
    )
    
    user_prompt = f"MASTER PROFILE:\n{profile}\n\nJOB DESCRIPTION:\n{jd}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
        )
        
        raw_content = response.choices[0].message.content.strip()
        
        # Clean up markdown code block wrappers if the model returns them
        if raw_content.startswith("```"):
            raw_content = raw_content.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
            if raw_content.startswith("json"):
                raw_content = raw_content.split("\n", 1)[1].strip()
                
        return json.loads(raw_content)
        
    except Exception as e:
        print(f"[ERROR] Fit Check pipeline failed: {e}")
        sys.exit(1)

def generate_asset(client, prompt_template, profile, jd, output_filename):
    """
    Phase 2: Tailoring execution loop (Resume or Cover Letter).
    """
    final_prompt = prompt_template.replace("{master_profile}", profile).replace("{job_description}", jd)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0.4
        )
        output_content = response.choices[0].message.content.strip()
        
        os.makedirs("output_resumes", exist_ok=True)
        filepath = os.path.join("output_resumes", output_filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(output_content)
        print(f"[SUCCESS] Asset successfully compiled and written to: {filepath}")
        
    except Exception as e:
        print(f"[ERROR] Failed to compile asset: {e}")

def main():
    api_key = get_api_key()
    client = OpenAI(api_key=api_key)
    
    # 1. Scan available Job Descriptions
    jd_dir = "job_descriptions"
    if not os.path.exists(jd_dir) or not os.listdir(jd_dir):
        print(f"[ERROR] The directory '{jd_dir}' is empty or missing.")
        sys.exit(1)
        
    jds = [f for f in os.listdir(jd_dir) if f.endswith(".txt") and "sample" not in f]
    if not jds:
        print("[ERROR] No targeted Job Description (.txt) files found.")
        sys.exit(1)
        
    print("\n--- Available Target Roles ---")
    for idx, jd_file in enumerate(jds, 1):
        print(f"[{idx}] {jd_file}")
        
    try:
        choice = int(input("\nSelect the target Job Description number to run: ")) - 1
        selected_jd_file = jds[choice]
    except (ValueError, IndexError):
        print("[ERROR] Invalid choice. Aborting execution.")
        sys.exit(1)
        
    # 2. Ingest base assets
    print(f"\n[INFO] Loading configurations for profile tailoring...")
    jd_content = load_file(os.path.join(jd_dir, selected_jd_file))
    
    profile_path = os.path.join("artifacts", "Real_Master_Profile.txt")
    if not os.path.exists(profile_path):
        profile_path = os.path.join("artifacts", "master_profile.txt")
    profile_content = load_file(profile_path)
    
    # 3. RUN THE GATING FIT CHECK
    assessment = run_fit_assessment(client, profile_content, jd_content)
    score = assessment.get("fit_score", 0)
    strengths = assessment.get("strengths", [])
    gaps = assessment.get("gaps", [])
    
    print("\n==================================================")
    print(f"📋 ATS MATCH RATIO RESULTS: {score}% Match")
    print("==================================================")
    
    # Always display Core Strengths
    if strengths:
        print("\n💎 CORE ALIGNMENT STRENGTHS:")
        for strength in strengths:
            print(f"  • {strength}")
            
    # Always display Potential Gaps / Areas to Watch
    if gaps:
        print("\n⚠️ POTENTIAL GAPS & INTERVIEW BLINDSPOTS:")
        for gap in gaps:
            print(f"  • {gap}")
            
    print("\n==================================================")
    
    # Gatekeeper check based on the 80% threshold
    if score >= 80:
        print("🟢 Strong Core Competency Alignment Verified. Proceeding automatically to compilation...")
    else:
        print("🛑 CRITICAL FAILURE: Fit score is below the 80% compliance threshold.")
        print("[WARNING] Applying with your current baseline profile runs a high risk of automated ATS rejection.")
        
        # Interactive user acknowledgment gate
        proceed = input("\nWould you like to force execution and build assets anyway? (y/n): ").strip().lower()
        if proceed != 'y':
            print("\n[ABORTED] Tailoring terminated by user to optimize profile compliance. No assets built.")
            sys.exit(0)
            
    # 4. RUN SYSTEM GENERATIONS IF CLEARED
    role_slug = selected_jd_file.replace(".txt", "")
    
    # Compile Tailored Resume
    if os.path.exists("prompt.txt"):
        print("\n[PHASE 2A] Executing Resume Optimization Matrix...")
        resume_prompt = load_file("prompt.txt")
        generate_asset(client, resume_prompt, profile_content, jd_content, f"{role_slug}_resume.md")
        
    # Compile Tailored Cover Letter
    if os.path.exists("prompt_cl.txt"):
        print("\n[PHASE 2B] Executing Cover Letter Structural Hook Matrix...")
        cl_prompt = load_file("prompt_cl.txt")
        generate_asset(client, cl_prompt, profile_content, jd_content, f"{role_slug}_cover_letter.md")
        
    print("\n[COMPLETE] Run complete. Check your '/output_resumes' folder.")

if __name__ == "__main__":
    main()