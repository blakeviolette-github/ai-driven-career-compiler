import os
import glob
from openai import OpenAI
from docx import Document
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Read the API key from your local file
try:
    with open("apikey.txt", "r", encoding="utf-8") as f:
        api_key_from_file = f.read().strip()
except FileNotFoundError:
    api_key_from_file = None

client = OpenAI(api_key=api_key_from_file)

# --- STEP 1: PARSE ARTIFACTS ---
def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    try:
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        elif ext == '.docx':
            doc = Document(file_path)
            text = "\n".join([p.text for p in doc.paragraphs])
        elif ext == '.pdf':
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return text

def load_all_artifacts(folder):
    combined_text = ""
    files = glob.glob(os.path.join(folder, "*.*"))
    for file in files:
        print(f"Reading artifact: {os.path.basename(file)}")
        combined_text += f"\n--- ARTIFACT: {os.path.basename(file)} ---\n"
        combined_text += extract_text_from_file(file)
    return combined_text

# --- STEP 2: AI ORCHESTRATION LAYERS ---
def generate_tailored_content(master_profile, job_description, prompt_filename):
    truncated_profile = master_profile[:95000] 
    
    with open(prompt_filename, "r", encoding="utf-8") as f:
        raw_prompt_template = f.read()
    
    final_prompt = raw_prompt_template.replace("{master_profile}", truncated_profile).replace("{job_description}", job_description)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": final_prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

# --- STEP 3: RUNNING FOOTER DRAW CALLBACK ---
def add_custom_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica-Oblique', 8)
    canvas.setFillColor('#555555') 
    footer_text = "Compiled via Blake Violette's custom Python/OpenAI orchestration engine | Verified authentic career data map"
    canvas.drawCentredString(A4[0] / 2.0, 20, footer_text)
    canvas.restoreState()

# --- STEP 4: PARSING ENGINE AND PDF BUILD ---
def convert_markdown_to_pdf(markdown_text, output_pdf_path):
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'ResumeTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', 
        fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=8, textColor='#000000'
    )
    h2_style = ParagraphStyle(
        'ResumeH2', parent=styles['Heading2'], fontName='Helvetica-Bold', 
        fontSize=11, leading=14, spaceBefore=14, spaceAfter=4, textColor='#000000',
        keepWithNext=True 
    )
    h3_style = ParagraphStyle(
        'ResumeH3', parent=styles['Heading3'], fontName='Helvetica', 
        fontSize=9.5, leading=13, spaceBefore=11, spaceAfter=3, textColor='#000000',
        keepWithNext=True 
    )
    body_style = ParagraphStyle(
        'ResumeBody', parent=styles['Normal'], fontName='Helvetica', 
        fontSize=9, leading=13, spaceAfter=8, alignment=TA_LEFT, textColor='#000000'
    )
    bullet_style = ParagraphStyle(
        'ResumeBullet', parent=styles['Normal'], fontName='Helvetica', 
        fontSize=9, leading=12.5, spaceAfter=3, alignment=TA_LEFT, textColor='#000000',
        leftIndent=7, firstLineIndent=-7
    )

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=50
    )

    story = []
    lines = markdown_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or "(CONTINUED)" in line.upper():
            continue  
            
        line = line.replace('***', '').replace('**', '')
        
        if line.startswith('# '):
            story.append(Paragraph(line[2:], title_style))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:].upper(), h2_style))
        elif line.startswith('### '):
            story.append(Paragraph(line[4:], h3_style))
        elif line.startswith('* ') or line.startswith('- ') or line.startswith('• '):
            if line.startswith('* ') or line.startswith('- '):
                clean_bullet = line[2:]
            else:
                clean_bullet = line[1:].strip()
            
            bullet_text = f"&bull;&nbsp;{clean_bullet}"
            story.append(Paragraph(bullet_text, bullet_style))
        else:
            story.append(Paragraph(line, body_style))

    doc.build(story, onFirstPage=add_custom_footer, onLaterPages=add_custom_footer)

# --- STEP 5: TARGETED APPLICATION RUNNER ---
def main():
    artifacts_dir = "./artifacts"
    jd_dir = "./job_descriptions"
    output_dir = "./output_resumes"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Read available job description files
    jd_files = glob.glob(os.path.join(jd_dir, "*.txt"))
    if not jd_files:
        print(f"Error: No .txt files found in '{jd_dir}'. Please drop a job description text file there first.")
        return
        
    print("\n--- Available Job Descriptions ---")
    for file in jd_files:
        print(f" - {os.path.basename(file)}")
    print("-----------------------------------\n")
    
    # 2. Interactive Input
    user_input = input("Enter the filename of the job description to run (e.g., amazon_pm.txt): ").strip()
    
    # Clean up input if user accidentally typed the whole path or dropped it in
    target_filename = os.path.basename(user_input)
    target_path = os.path.join(jd_dir, target_filename)
    
    if not os.path.exists(target_path):
        print(f"\nError: File '{target_filename}' not found in '{jd_dir}'. Execution aborted.")
        return

    # 3. Process the selected profile only
    print("\nStep 1: Compiling career artifacts...")
    master_profile = load_all_artifacts(artifacts_dir)
    
    if not master_profile.strip():
        print("Error: No artifacts found or extracted.")
        return

    job_name = os.path.splitext(target_filename)[0]
    print(f"\nProcessing target package for: {job_name}...")
    
    with open(target_path, 'r', encoding='utf-8') as f:
        job_description = f.read()
        
    # --- PART A: TAILORED RESUME GENERATION ---
    print(" -> Querying resume intelligence layer...")
    resume_markdown = generate_tailored_content(master_profile, job_description, "prompt.txt")
    output_resume_path = os.path.join(output_dir, f"Blake_Violette_Resume_{job_name}.pdf")
    print(" -> Compiling text into clean A4 Resume PDF...")
    convert_markdown_to_pdf(resume_markdown, output_resume_path)
    
    # --- PART B: TAILORED COVER LETTER GENERATION ---
    print(" -> Querying cover letter intelligence layer...")
    cl_markdown = generate_tailored_content(master_profile, job_description, "prompt_cl.txt")
    output_cl_path = os.path.join(output_dir, f"Blake_Violette_CoverLetter_{job_name}.pdf")
    print(" -> Compiling text into clean A4 Cover Letter PDF...")
    convert_markdown_to_pdf(cl_markdown, output_cl_path)
    
    print(f"\n[SUCCESS] Custom application package successfully compiled into '{output_dir}'!\n")

if __name__ == '__main__':
    main()