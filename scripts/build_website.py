import os
import re
import csv
import json
import glob
from datetime import datetime

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLR_FILE = os.path.join(BASE_DIR, "Cloud_Infrastructure_Drift_SLRV2.txt")
PDF_DIR = os.path.join(BASE_DIR, "paper_for_full_text_review")
CSV_156 = os.path.join(BASE_DIR, "156_papers_after_screening.csv")
INCLUDED_CSV = os.path.join(BASE_DIR, "44_papers_fulltext_included.csv")
OUTPUT_HTML = os.path.join(BASE_DIR, "index.html")

# Visualization Injection Map (Section Title Keyword -> Image Filename)
CHART_MAP = {
    "PRISMA": "prisma_flow_diagram.png",
    "Temporal Distribution": "temporal_distribution.png",
    "Study Types": "study_types_distribution.png",
    "Publication Venues": "publication_venues.png",
    "Geographic Distribution": "geographic_distribution.png",
    "Drift Detection Methods": "drift_detection_comparison.png",
    "Remediation Strategies": "remediation_strategies_comparison.png",
    "IaC Tools": "iac_tools_comparison.png",
    "Thematic Clusters": "thematic_clusters.png",
}

# ------------------------------------------------------------------
# 1. Load Data
# ------------------------------------------------------------------

def load_pdf_map():
    """Maps paper numbers (int) to PDF filenames."""
    pdf_map = {}
    if not os.path.exists(PDF_DIR):
        print(f"Warning: PDF directory not found: {PDF_DIR}")
        return pdf_map
    
    for f in os.listdir(PDF_DIR):
        if f.lower().endswith(".pdf"):
            # brightness check: filename starts with number?
            match = re.match(r"^(\d+)-", f)
            if match:
                num = int(match.group(1))
                pdf_map[num] = f
    print(f"Loaded {len(pdf_map)} PDFs from {PDF_DIR}")
    return pdf_map

def load_reference_map(pdf_map):
    """
    Parses SLR References section to map citation numbers [1] to PDF links.
    Uses title/author similarity against available PDFs/CSVs if needed, 
    but primarily relies on the order in the text matching the reference list?
    Actually, the text uses [1], [2]. We need to know what [1] is.
    We'll parse the References section of the text file.
    """
    with open(SLR_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract References Section
    ref_section = re.split(r"8\.\s+References", content, flags=re.IGNORECASE)
    if len(ref_section) < 2:
        print("Warning: Could not find '8. References' section.")
        return {}
    
    refs_text = ref_section[1].strip()
    
    # Parse individual references: [1] ... [2] ...
    # Regex lookahead for next [n]
    ref_entries = re.findall(r"\[(\d+)\]\s+(.*?)(?=\[\d+\]|$)", refs_text, re.DOTALL)
    
    # We also need a way to link these to PDFs.
    # Strategy: 
    # 1. Check if the reference text contains a DOI. 
    # 2. Check title similarity with `156_papers_after_screening.csv` (which has IDs).
    # 3. Use the ID to find the PDF.
    
    # Load 156 CSV for metadata mapping
    csv_papers = []
    if os.path.exists(CSV_156):
        with open(CSV_156, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                csv_papers.append(row)
    
    # Load 44 included CSV for metadata mapping (higher priority)
    included_papers = []
    if os.path.exists(INCLUDED_CSV):
        with open(INCLUDED_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                included_papers.append(row)

    ref_link_map = {} # { "1": "paper_for_full_text_review/3-....pdf" }
    
    print(f"Parsing {len(ref_entries)} references...")
    
    for ref_id, ref_text in ref_entries:
        ref_text_lower = ref_text.lower()
        
        # Try to find a match in the papers (fuzzy title match)
        # Simple heuristic: split ref title by quote or just take longest chunk
        # Most refs format: Author, "Title", Journal...
        title_match = re.search(r"“([^”]+)”", ref_text)
        if not title_match:
            title_match = re.search(r"\"([^\"]+)\"", ref_text)
        
        target_pdf = None
        
        if title_match:
            search_title = title_match.group(1)
            # Find in CSVs
            # 1. Check Included
            for row in included_papers:
                if search_title.lower() in row.get("Title", "").lower() or \
                   row.get("Title", "").lower() in search_title.lower():
                    # Found match! Get Paper Number
                    p_num_str = row.get("Paper Number", "").strip()
                    if p_num_str and p_num_str.isdigit():
                        p_num = int(p_num_str)
                        if p_num in pdf_map:
                            target_pdf = pdf_map[p_num]
                            break
            
            # 2. Check 156 if not found
            if not target_pdf:
                for row in csv_papers:
                    if search_title.lower() in row.get("Paper Title", "").lower():
                        # We need the Paper Number. 156 csv might not have "Paper Number" col?
                        # It usually has line number or explicit col. Let's check keys.
                        # Assuming it corresponds to PDF numbers if 156 list is source.
                        # Wait, PDF maps are from "Paper_Number-Title".
                        # Let's search PDF filenames directly for title parts!
                        pass 

        # 3. Direct PDF filename search (robust fallback)
        if not target_pdf:
            # Tokenize title
            if title_match:
                title_tokens = [w for w in re.split(r"\W+", title_match.group(1)) if len(w) > 4]
                best_score = 0
                for p_num, p_file in pdf_map.items():
                    score = sum(1 for t in title_tokens if t.lower() in p_file.lower())
                    if score > best_score and score >= 2: # At least 2 keyword matches
                        best_score = score
                        target_pdf = p_file
                        
        if target_pdf:
            ref_link_map[ref_id] = f"paper_for_full_text_review/{target_pdf}"
            # print(f"  [{ref_id}] Mapped to {target_pdf}")
        else:
            # print(f"  [{ref_id}] No PDF found.")
            pass
            
    return ref_link_map

# ------------------------------------------------------------------
# 2. HTML Generation Helpers
# ------------------------------------------------------------------

HTML_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud Infrastructure Drift SLR (2019-2025)</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #1a1a2e;
            --bg-card: #16213e;
            --accent: #0f3460;
            --highlight: #e94560;
            --text-main: #e0e0e0;
            --text-muted: #a0a0a0;
            --neon-blue: #00d2ff;
        }
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            margin: 0;
            line-height: 1.6;
        }
        a { color: var(--neon-blue); text-decoration: none; transition: 0.3s; }
        a:hover { text-decoration: underline; color: #fff; }
        
        /* Nav */
        nav {
            position: sticky; top: 0; z-index: 1000;
            background: rgba(26, 26, 46, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--accent);
            padding: 1rem 2rem;
            display: flex; justify-content: space-between; align-items: center;
        }
        .nav-links { display: flex; gap: 1.5rem; }
        .nav-links a { font-weight: 600; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }
        .nav-logo { font-size: 1.2rem; font-weight: 800; color: #fff; }
        
        /* Container */
        .container { max-width: 1000px; margin: 0 auto; padding: 2rem; }
        .section { margin-bottom: 4rem; scroll-margin-top: 100px; padding-top: 2rem; border-bottom: 1px solid var(--accent); padding-bottom: 2rem; }
        
        /* Headings */
        h1, h2, h3 { color: #fff; margin-top: 2rem; }
        h1 { font-size: 2.5rem; background: linear-gradient(90deg, #fff, var(--neon-blue)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem; }
        h2 { font-size: 1.8rem; border-left: 4px solid var(--highlight); padding-left: 1rem; margin-bottom: 1.5rem; }
        h3 { font-size: 1.4rem; color: var(--neon-blue); margin-bottom: 1rem; }
        
        /* Cards */
        .card { background: var(--bg-card); padding: 1.5rem; border-radius: 12px; border: 1px solid var(--accent); margin-bottom: 1.5rem; transition: transform 0.2s; }
        .card:hover { transform: translateY(-5px); border-color: var(--neon-blue); }
        
        /* Figures */
        figure { margin: 2rem 0; text-align: center; background: #0002; padding: 1rem; border-radius: 8px; border: 1px solid var(--accent); }
        img { max-width: 100%; height: auto; border-radius: 4px; }
        figcaption { margin-top: 0.5rem; color: var(--text-muted); font-size: 0.9rem; font-style: italic; }
        
        /* Table */
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; font-size: 0.9rem; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid var(--accent); }
        th { background: var(--accent); color: #fff; position: sticky; top: 0; }
        tr:hover { background: #ffffff05; }
        
        /* Metrics */
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
        .metric-box { background: linear-gradient(135deg, var(--bg-card), var(--accent)); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid #ffffff10; }
        .metric-val { font-size: 2.5rem; font-weight: 800; color: #fff; display: block; margin-bottom: 0.5rem; }
        .metric-label { font-size: 0.9rem; color: var(--neon-blue); text-transform: uppercase; letter-spacing: 1px; }

        /* Code */
        pre { background: #0004; padding: 1rem; border-radius: 8px; overflow-x: auto; border: 1px solid var(--accent); }
        code { font-family: 'Consolas', monospace; color: var(--highlight); }

        /* References */
        .ref-link { color: var(--highlight); font-weight: bold; cursor: pointer; }
        .citation-box { font-size: 0.85rem; padding-left: 1rem; border-left: 2px solid var(--text-muted); color: var(--text-muted); margin-bottom: 0.5rem; }
        
        /* Mobile */
        @media (max-width: 768px) {
            .nav-links { display: none; }
            h1 { font-size: 1.8rem; }
        }
    </style>
</head>
<body>
    <nav>
        <div class="nav-logo">SLR 2025</div>
        <div class="nav-links">
            <a href="#home">Home</a>
            <a href="#findings">Findings</a>
            <a href="#slr-content">Read SLR</a>
            <a href="#papers">Papers</a>
            <a href="#methodology">Methodology</a>
            <a href="#reproducibility">Reproduce</a>
        </div>
    </nav>
"""

HTML_FOOTER = """
    <footer style="text-align: center; padding: 4rem 1rem; color: var(--text-muted); border-top: 1px solid var(--accent); margin-top: 4rem;">
        <p>Systematic Literature Review: Cloud Infrastructure Drift Detection & Remediation (2019-2025)</p>
        <p>Generated by Deepmind Agent • <a href="https://github.com/google-deepmind">GitHub</a></p>
    </footer>
    <script>
        // Smooth scroll for nav links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    </script>
</body>
</html>
"""

# ------------------------------------------------------------------
# 3. Content Parsers
# ------------------------------------------------------------------

def parse_slr_content(ref_map):
    """
    Reads SLR text, converts to HTML paragraphs/headers, 
    injects charts, and hyperlinks references.
    """
    with open(SLR_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    html = ""
    current_section = ""
    
    # Process line by line
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Headers (numbered sections)
        header_match = re.match(r"^(\d+(\.\d+)*)\.?\s+(.*)", line)
        if header_match:
            level = line.count('.')
            sec_num = header_match.group(1)
            sec_title = header_match.group(3)
            current_section = sec_title
            
            # Use H2 or H3 based on level
            tag = "h2" if level == 0 else "h3"
            html += f'<{tag} id="sec-{sec_num}">{sec_title}</{tag}>'
            
            # Check for chart injection based on title
            for key, filename in CHART_MAP.items():
                if key in sec_title and filename:
                    html += f'''
                    <figure>
                        <img src="images/{filename}" alt="{sec_title}">
                        <figcaption>Figure: {sec_title} Visualization</figcaption>
                    </figure>
                    '''
            continue
            
        # Reference Linking [1] -> <a href="...">[1]</a>
        def replace_ref(match):
            rid = match.group(1)
            pdf_link = ref_map.get(rid)
            if pdf_link:
                return f'<a href="{pdf_link}" class="ref-link" title="Open PDF for Reference {rid}" target="_blank">[{rid}]</a>'
            return f'[{rid}]'
            
        line = re.sub(r"\[(\d+)\]", replace_ref, line)
        
        # Regular paragraph
        html += f'<p>{line}</p>\n'
        
    return html

def generate_papers_table(pdf_map):
    """Generates an HTML table of papers from CSVs."""
    rows = []
    
    # Load included papers CSV
    if os.path.exists(INCLUDED_CSV):
        with open(INCLUDED_CSV, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            for row in reader:
                p_num = row.get("Paper Number", "").strip()
                title = row.get("Title", "") or row.get("Paper Title", "Untitled")
                year = row.get("Year", "") or row.get("Publication Year", "")
                authors = row.get("Authors", "") or row.get("Author Names", "")
                
                pdf_link = ""
                if p_num.isdigit():
                    pid = int(p_num)
                    if pid in pdf_map:
                        pdf_link = f'<a href="paper_for_full_text_review/{pdf_map[pid]}" target="_blank" style="color:var(--highlight)">PDF</a>'
                    else:
                        pdf_link = '<span style="color:var(--text-muted)">-</span>'
                
                rows.append(f"""
                <tr>
                    <td>{p_num}</td>
                    <td><b>{title}</b><br><span style="font-size:0.85em; color:var(--text-muted)">{authors}</span></td>
                    <td>{year}</td>
                    <td>{pdf_link}</td>
                </tr>
                """)
    else:
        rows.append("<tr><td colspan='4'>No paper data found.</td></tr>")
    
    return f"""
    <div style="overflow-x:auto;">
        <table>
            <thead>
                <tr>
                    <th style="width:50px">#</th>
                    <th>Title & Authors</th>
                    <th style="width:80px">Year</th>
                    <th style="width:80px">PDF</th>
                </tr>
            </thead>
            <tbody>
                {"".join(rows)}
            </tbody>
        </table>
    </div>
    """

# ------------------------------------------------------------------
# 4. Section Generators
# ------------------------------------------------------------------

def section_home():
    return """
    <section id="home" class="section">
        <h1>Cloud Infrastructure Drift Detection & Remediation</h1>
        <p style="font-size: 1.2rem; color: var(--text-muted); margin-bottom: 2rem;">
            A Systematic Literature Review (2019–2025) covering 830 searched papers, 96 included studies, and 44 full-text analyses.
        </p>
        <div class="metrics-grid">
            <div class="metric-box">
                <span class="metric-val">96</span>
                <span class="metric-label">Included Studies</span>
            </div>
            <div class="metric-box">
                <span class="metric-val">2019-25</span>
                <span class="metric-label">Temporal Scope</span>
            </div>
            <div class="metric-box">
                <span class="metric-val">104</span>
                <span class="metric-label">Full-Text Screened</span>
            </div>
            <div class="metric-box">
                <span class="metric-val">10</span>
                <span class="metric-label">Visualizations</span>
            </div>
        </div>
        <div style="display:flex; gap:1rem; flex-wrap:wrap;">
            <a href="#slr-content" style="background:var(--neon-blue); color:#000; padding:12px 24px; border-radius:6px; font-weight:bold;">Read Full SLR</a>
            <a href="#papers" style="border:1px solid var(--neon-blue); color:var(--neon-blue); padding:12px 24px; border-radius:6px; font-weight:bold;">Browse Papers</a>
        </div>
    </section>
    """

def section_findings():
    return """
    <section id="findings" class="section">
        <h2>Key Findings & Metrics</h2>
        <p>Overview of the critical metrics extracted from the literature.</p>
        <figure>
            <img src="images/key_metrics_dashboard.png" alt="Key Metrics Dashboard">
        </figure>
        
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 2rem;">
            <div class="card">
                <h3>Temporal Growth</h3>
                <img src="images/temporal_distribution.png" alt="Temporal Distribution">
                <p>380% growth in research publications from 2019 to 2025, reflecting the surge in IaC adoption.</p>
            </div>
            <div class="card">
                <h3>IaC Tools Market</h3>
                <img src="images/iac_tools_comparison.png" alt="IaC Tools">
                <p>Terraform dominates with 62% market share, followed by Ansible (34%) and CloudFormation.</p>
            </div>
        </div>
    </section>
    """

def section_slr_content(parsed_text):
    return f"""
    <section id="slr-content" class="section">
        <div style="background:var(--bg-card); padding:2rem; border-radius:12px; border:1px solid var(--accent);">
            {parsed_text}
        </div>
    </section>
    """

def section_papers(pdf_map):
    table_html = generate_papers_table(pdf_map)
    return f"""
    <section id="papers" class="section">
        <h2>Included Papers Database</h2>
        <p>Full list of 96 included papers. Download PDFs where available (44 full-text included).</p>
        {table_html}
    </section>
    """

def section_methodology():
    return """
    <section id="methodology" class="section">
        <h2>Methodology (PRISMA)</h2>
        <p>This review followed the PRISMA 2020 guidelines. 830 papers were identified, 683 screened after deduplication, leading to 96 final included studies.</p>
        <figure>
            <img src="images/prisma_flow_diagram.png" alt="PRISMA Flow Diagram" style="max-height:800px;">
        </figure>
    </section>
    """

def section_reproducibility():
    py_script_link = '<a href="scripts/generate_slr_charts.py" target="_blank">scripts/generate_slr_charts.py</a>'
    return f"""
    <section id="reproducibility" class="section">
        <h2>Reproducibility</h2>
        <p>Steps to reproduce this review and its artifacts:</p>
        <div class="card">
            <h3>1. Data Collection</h3>
            <p>Search queries were executed on SciSpace, Google Scholar, and ArXiv. Results saved to <code>Query_Results/</code>.</p>
        </div>
        <div class="card">
            <h3>2. Deduplication & Screening</h3>
            <p>Python scripts removed duplicates (DOI/Title fuzzy match). Abstract screening was performed on 683 unique records.</p>
            <pre><code>python scripts/deduplicate_papers.py</code></pre>
        </div>
        <div class="card">
            <h3>3. Visualization Generation</h3>
            <p>All charts in this report were generated programmatically using {py_script_link}.</p>
            <pre><code>python scripts/generate_slr_charts.py</code></pre>
        </div>
    </section>
    """

# ------------------------------------------------------------------
# Main Execution
# ------------------------------------------------------------------

def main():
    print("Starting website build...")
    
    # 1. Load Maps
    pdf_map = load_pdf_map()
    ref_map = load_reference_map(pdf_map)
    
    # 2. Parse SLR Content
    slr_html = parse_slr_content(ref_map)
    
    # 3. Assemble HTML
    full_html = (
        HTML_HEAD +
        "<div class='container'>" +
        section_home() +
        section_findings() +
        section_methodology() +
        section_slr_content(slr_html) +
        section_papers(pdf_map) +
        section_reproducibility() +
        "</div>" +
        HTML_FOOTER
    )
    
    # 4. Save
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(full_html)
    
    print(f"Website generated at: {OUTPUT_HTML}")

if __name__ == "__main__":
    main()
