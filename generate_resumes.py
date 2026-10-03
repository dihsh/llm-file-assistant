"""
generate_resumes.py - Programmatically creates 8 diverse, realistic resume files
in PDF, DOCX, and TXT formats for testing and grading.
"""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import docx

RESUMES_DIR = Path("resumes")
RESUMES_DIR.mkdir(parents=True, exist_ok=True)


def create_pdf(filepath: Path, title: str, contact: str, summary: str, skills: list, experience: list, education: str):
    doc = SimpleDocTemplate(str(filepath), pagesize=letter, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'ResumeTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=4
    )
    contact_style = ParagraphStyle(
        'ResumeContact',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=12
    )
    section_style = ParagraphStyle(
        'ResumeSection',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1F2937'),
        spaceBefore=10,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#111827'),
        spaceAfter=6
    )

    story = [
        Paragraph(title, title_style),
        Paragraph(contact, contact_style),
        Paragraph("Professional Summary", section_style),
        Paragraph(summary, body_style),
        Paragraph("Technical Skills", section_style),
        Paragraph(", ".join(skills), body_style),
        Paragraph("Work Experience", section_style),
    ]

    for role, company, desc in experience:
        story.append(Paragraph(f"<b>{role}</b> - <i>{company}</i>", body_style))
        story.append(Paragraph(desc, body_style))
        story.append(Spacer(1, 4))

    story.append(Paragraph("Education", section_style))
    story.append(Paragraph(education, body_style))

    doc.build(story)


def create_docx(filepath: Path, title: str, contact: str, summary: str, skills: list, experience: list, education: str):
    doc = docx.Document()
    doc.add_heading(title, level=0)
    p_contact = doc.add_paragraph(contact)
    p_contact.style.font.color.rgb = docx.shared.RGBColor(100, 100, 100)

    doc.add_heading("Professional Summary", level=1)
    doc.add_paragraph(summary)

    doc.add_heading("Technical Skills", level=1)
    doc.add_paragraph(", ".join(skills))

    doc.add_heading("Work Experience", level=1)
    for role, company, desc in experience:
        p_role = doc.add_paragraph()
        r1 = p_role.add_run(role)
        r1.bold = True
        r2 = p_role.add_run(f" | {company}")
        r2.italic = True
        doc.add_paragraph(desc)

    doc.add_heading("Education", level=1)
    doc.add_paragraph(education)

    doc.save(str(filepath))


def create_txt(filepath: Path, title: str, contact: str, summary: str, skills: list, experience: list, education: str):
    exp_str = "\n".join([f"- {role} at {company}:\n  {desc}\n" for role, company, desc in experience])
    content = f"""=======================================================
{title}
{contact}
=======================================================

PROFESSIONAL SUMMARY:
{summary}

TECHNICAL SKILLS:
{', '.join(skills)}

WORK EXPERIENCE:
{exp_str}
EDUCATION:
{education}
=======================================================
"""
    filepath.write_text(content.strip(), encoding="utf-8")


def generate_all():
    # 1. John Doe (PDF) - Senior Python & Backend Engineer
    create_pdf(
        RESUMES_DIR / "resume_john_doe.pdf",
        title="John Doe",
        contact="Email: john.doe@email.com | Phone: +1-555-0101 | Location: San Francisco, CA | GitHub: github.com/johndoe",
        summary="Senior Backend Engineer with 7+ years of experience architecting scalable distributed systems, microservices, and REST APIs using Python, FastAPI, and Django. Passionate about asynchronous performance and clean architecture.",
        skills=["Python (FastAPI, Django, Flask)", "PostgreSQL", "Redis", "Docker", "Kubernetes", "AWS", "Celery", "Kafka", "Git"],
        experience=[
            ("Staff Python Engineer", "Apex Cloud Systems (2022 - Present)",
             "Engineered high-throughput event processing pipelines in Python processing over 10M events daily with Redis & Kafka. Optimized query performance by 40%."),
            ("Backend Software Developer", "FinTech Nexus (2019 - 2022)",
             "Developed modular Python REST APIs for digital payment workflows using FastAPI and PostgreSQL, guaranteeing 99.99% system availability.")
        ],
        education="B.S. in Computer Science - University of California, Berkeley (2018)"
    )

    # 2. Jane Smith (DOCX) - Full Stack Developer
    create_docx(
        RESUMES_DIR / "resume_jane_smith.docx",
        title="Jane Smith",
        contact="Email: jane.smith@techdomain.com | Phone: +1-555-0102 | Location: Austin, TX | Portfolio: janesmith.dev",
        summary="Versatile Full Stack Developer with 5 years of experience building modern web applications. Deep expertise in React and Node.js on the frontend, alongside Python scripting and backend API integration.",
        skills=["Python", "JavaScript", "TypeScript", "React", "Node.js", "Express", "MongoDB", "PostgreSQL", "TailwindCSS"],
        experience=[
            ("Senior Full Stack Developer", "OmniWeb Solutions (2021 - Present)",
             "Spearheaded responsive enterprise dashboard redesign in React, integrating Python Flask microservices for real-time document analytics."),
            ("Frontend Engineer", "Creative Pixels Studio (2019 - 2021)",
             "Delivered single-page web applications with React, TypeScript, and Redux, improving user retention by 28%.")
        ],
        education="B.S. in Software Engineering - University of Texas at Austin (2019)"
    )

    # 3. Alex Kumar (TXT) - Machine Learning Engineer
    create_txt(
        RESUMES_DIR / "resume_alex_kumar.txt",
        title="Alex Kumar",
        contact="Email: alex.kumar@ai-research.org | Phone: +1-555-0103 | Location: Seattle, WA",
        summary="Machine Learning Engineer with 4 years of hands-on experience developing deep learning architectures and LLM applications using Python, PyTorch, and LangChain. Strong focus on fine-tuning transformer models and vector databases.",
        skills=["Python", "PyTorch", "TensorFlow", "HuggingFace", "LangChain", "Vector DBs (Chroma, Pinecone)", "Docker", "FastAPI"],
        experience=[
            ("Machine Learning Engineer", "Cognitive AI Labs (2022 - Present)",
             "Built Retrieval-Augmented Generation (RAG) pipelines in Python with LangChain and FAISS, boosting customer support automation by 65%."),
            ("Data & AI Developer", "DataWave Analytics (2020 - 2022)",
             "Trained and evaluated computer vision and NLP classification models in Python and PyTorch on AWS GPU instances.")
        ],
        education="M.S. in Artificial Intelligence - University of Washington (2020)"
    )

    # 4. Emily Chen (PDF) - Senior Data Scientist
    create_pdf(
        RESUMES_DIR / "resume_emily_chen.pdf",
        title="Emily Chen",
        contact="Email: emily.chen@analytics.io | Phone: +1-555-0104 | Location: New York, NY",
        summary="Data Scientist with 6 years of expertise delivering actionable business insights through predictive modeling, statistical inference, and big data visualization. Advanced proficiency in Python, Pandas, and SQL.",
        skills=["Python (Pandas, NumPy, Scikit-Learn)", "SQL (PostgreSQL, Snowflake)", "Tableau", "PowerBI", "A/B Testing", "Spark", "Airflow"],
        experience=[
            ("Lead Data Scientist", "Metro Metrics Corp (2021 - Present)",
             "Constructed predictive customer churn models in Python with Scikit-Learn, yielding $1.8M annual savings in subscriber retention."),
            ("Quantitative Analyst", "Beacon Capital (2018 - 2021)",
             "Formulated automated portfolio attribution pipelines using Python and SQL, cutting daily reporting latency by 75%.")
        ],
        education="M.S. in Applied Statistics - Columbia University (2018)"
    )

    # 5. Michael Brown (DOCX) - DevOps & Cloud Architect
    create_docx(
        RESUMES_DIR / "resume_michael_brown.docx",
        title="Michael Brown",
        contact="Email: michael.brown@cloudops.net | Phone: +1-555-0105 | Location: Chicago, IL",
        summary="Cloud Infrastructure Engineer with 8 years of experience building secure multi-region environments on AWS and GCP. Expert in Terraform, Kubernetes, Helm, and zero-downtime CI/CD automation. Background in Go and Bash.",
        skills=["Kubernetes", "Docker", "Terraform", "AWS", "GCP", "Go (Golang)", "Bash", "GitHub Actions", "Prometheus", "ArgoCD"],
        experience=[
            ("Principal DevOps Engineer", "Stratus Cloud Tech (2020 - Present)",
             "Migrated bare-metal monolithic systems to AWS EKS using Terraform and Helm, improving deployment cadence by 300%."),
            ("Site Reliability Engineer", "Apex Logistics (2016 - 2020)",
             "Authored Golang daemon monitoring tools and automated disaster recovery failover with Bash and Ansible.")
        ],
        education="B.S. in Computer Engineering - University of Illinois at Urbana-Champaign (2016)"
    )

    # 6. Sarah Patel (TXT) - Frontend Engineer
    create_txt(
        RESUMES_DIR / "resume_sarah_patel.txt",
        title="Sarah Patel",
        contact="Email: sarah.patel@webcraft.com | Phone: +1-555-0106 | Location: Boston, MA",
        summary="Frontend UI/UX Engineer with 3 years of expertise building accessible, ultra-responsive web applications. Passionate about design systems, WCAG compliance, and modern JavaScript frameworks.",
        skills=["JavaScript", "TypeScript", "React", "Vue.js", "Next.js", "HTML5", "CSS3", "TailwindCSS", "Figma", "Jest"],
        experience=[
            ("Frontend Developer", "PixelCraft Studios (2022 - Present)",
             "Engineered interactive SaaS components using React, TypeScript, and TailwindCSS, achieving 98+ Google Lighthouse scores."),
            ("Junior Web Designer & Dev", "Elevate Creative (2021 - 2022)",
             "Built responsive landing pages and customized Vue.js storefront widgets for global e-commerce brands.")
        ],
        education="B.A. in Digital Media & Web Design - Northeastern University (2021)"
    )

    # 7. David Wilson (PDF) - Cybersecurity & SRE
    create_pdf(
        RESUMES_DIR / "resume_david_wilson.pdf",
        title="David Wilson",
        contact="Email: david.wilson@infosec.org | Phone: +1-555-0107 | Location: Washington, DC",
        summary="Cybersecurity specialist and DevSecOps engineer with 5 years of experience in vulnerability assessments, penetration testing, and incident response automation using Python scripts and Linux tooling.",
        skills=["Python (Scripting & Automation)", "Linux / Bash", "SIEM (Splunk, Elastic)", "Wireshark", "OWASP Top 10", "SOC 2", "AWS IAM", "NIST"],
        experience=[
            ("Security Engineer", "Vanguard Cyber Defense (2021 - Present)",
             "Authored automated Python triage scripts that parse firewall logs and alert on brute-force attempts in real-time."),
            ("SOC Analyst", "Federal Data Guard (2019 - 2021)",
             "Monitored threat vectors across 500+ endpoints, conducting forensic root-cause analysis and intrusion response.")
        ],
        education="B.S. in Cybersecurity - George Mason University (2019)"
    )

    # 8. Priya Sharma (DOCX) - AI Research Engineer
    create_docx(
        RESUMES_DIR / "resume_priya_sharma.docx",
        title="Priya Sharma",
        contact="Email: priya.sharma@deeplearning.ai | Phone: +1-555-0108 | Location: San Jose, CA",
        summary="AI Research Scientist with 4 years of background in Natural Language Processing, Transformer architectures, and LLM fine-tuning. Experienced with Python, PyTorch, HuggingFace, and agentic workflows.",
        skills=["Python", "PyTorch", "HuggingFace Transformers", "LangChain", "vLLM", "Deep Learning", "FastAPI", "MLOps", "Git"],
        experience=[
            ("AI Research Scientist", "NeuralEdge Technologies (2022 - Present)",
             "Researched and fine-tuned open-source 7B/13B parameter LLMs in Python using LoRA/QLoRA on multi-node GPU clusters."),
            ("NLP Research Intern", "Stanford AI Lab (2021 - 2022)",
             "Published empirical evaluations on semantic text parsing and context retrieval benchmarking in Python.")
        ],
        education="M.S. in Computer Science (AI Track) - Stanford University (2022)"
    )

    print("Successfully generated 8 diverse resumes in PDF, DOCX, and TXT formats inside './resumes'.")


if __name__ == "__main__":
    generate_all()
