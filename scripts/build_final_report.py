# -*- coding: utf-8 -*-
"""
generate_clean_report.py
Generates the complete, professional IDHV Project report with:
- 1-inch standard margins and executive typography hierarchy
- Polished Sections 1, 2, and 3 from Pranav & Krish
- Complete Section 4, Section 5, and Appendix from Mayank
- All 10 high-resolution figures embedded and centered with italic captions
- All 6 tables styled with crisp boundaries (borders), padding, repeat headers,
  no-row-split, alternating zebra shading, and bold captions
"""

import os
import shutil
import sys
from pathlib import Path

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

# Palette definition
COL_NAVY = RGBColor(0x1E, 0x3A, 0x8A)       # #1E3A8A Primary Accent
COL_SLATE = RGBColor(0x33, 0x41, 0x55)      # #334155 Secondary Accent
COL_SUBTLE = RGBColor(0x64, 0x74, 0x8B)     # #64748B Footnotes & Muted Text
COL_BODY = RGBColor(0x1E, 0x29, 0x3B)       # #1E293B Body Text
COL_HEADER_TXT = RGBColor(0x0F, 0x17, 0x2A) # #0F172A Table Header Text

BORDER_OUTER = "334155"   # 1 pt slate border around table
BORDER_HEADER = "1E3A8A"  # 1.25 pt deep navy rule under header
BORDER_HORIZ = "CBD5E1"   # 0.5 pt light slate divider
BORDER_VERT = "E2E8F0"    # 0.5 pt subtle vertical divider
HEADER_BG = "F1F5F9"      # Cool slate header background
ZEBRA_BG = "F8FAFC"       # Very soft light grey zebra striping

WORKSPACE_DIR = r"\\wsl$\Ubuntu-24.04\home\mayank_kumar_388\Courses\Sem 5\Data Handling & Visualization\Course Project"

def load_and_prep_base_document():
    base_candidates = [
        os.path.join(WORKSPACE_DIR, "reports", "IDHV Project.docx"),
        os.path.join(WORKSPACE_DIR, "IDHV Project.docx"),
        "reports/IDHV Project.docx",
        "IDHV Project.docx"
    ]
    doc_path = next((b for b in base_candidates if os.path.exists(b)), None)
    if not doc_path:
        raise FileNotFoundError("Base document reports/IDHV Project.docx not found!")
    
    print(f"Loading base document: {doc_path}")
    doc = docx.Document(doc_path)
    
    # 1-inch margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        s.page_width = Inches(8.5)
        s.page_height = Inches(11.0)
        
    # Format existing paragraphs in Sections 1, 2, 3
    for p in doc.paragraphs:
        txt = p.text.strip()
        if not txt:
            continue
            
        # Section 1, 2, 3 Heading 1s
        if txt.startswith("1. Introduction") or txt.startswith("2. Methodology") or txt.startswith("3. Data Preprocessing"):
            p.style = 'Normal'
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(14.0)
                r.font.color.rgb = COL_NAVY
                r.font.name = "Calibri"
                
        # Subsection Heading 2s
        elif any(txt.startswith(f"{sec}.") for sec in [
            "1.1", "2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8",
            "3.1", "3.2", "3.3", "3.4"
        ]):
            p.style = 'Normal'
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(11.5)
                r.font.color.rgb = COL_SLATE
                r.font.name = "Calibri"
                
        # Document Title
        elif txt == "Student Lifestyle & Academic Productivity Analysis":
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(4)
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(22.0)
                r.font.color.rgb = COL_NAVY
                r.font.name = "Calibri"
                
        # Subtitle
        elif txt.startswith("IDHV Project - M2026"):
            p.text = "A Comprehensive Empirical Investigation into Digital Distraction, Sleep Quality, Study Habits, and Performance"
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(10)
            for r in p.runs:
                r.font.italic = True
                r.font.size = Pt(11.0)
                r.font.color.rgb = COL_SLATE
                r.font.name = "Calibri"
                
        # Group attribution line
        elif txt.startswith("M. Pranav, K. Krish, Mayank Kumar"):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(16)
            p.text = "Course: Data Handling & Visualization (IDHV) | Semester 5\n" + \
                     "Group Contributors: M. Pranav (Data Preprocessing), K. Krish (Methodology & Literature), Mayank Kumar (EDA & Statistical Modeling)"
            if p.runs:
                p.runs[0].font.size = Pt(9.5)
                p.runs[0].font.color.rgb = COL_SUBTLE
                p.runs[0].font.name = "Calibri"
                
        # Bullet list items in Section 1.1, 2.4, 3.4
        elif (
            txt.startswith("Time spent in the gym") or txt.startswith("Average hours per week spent playing sports") or
            txt.startswith("Average hours of sleep per night") or txt.startswith("Typical sleep timeframe") or
            txt.startswith("Perceived sleep quality") or txt.startswith("Use of digital devices") or
            txt.startswith("Average daily screen time") or txt.startswith("Time spent on social media") or
            txt.startswith("Time spent on gaming") or txt.startswith("Frequency of digital device distractions") or
            txt.startswith("Time dedicated to studying") or txt.startswith("Consistency in maintaining study") or
            txt.startswith("Class attendance percentage") or txt.startswith("Stress levels over") or
            txt.startswith("Ability to maintain concentration") or txt.startswith("Frequency of feeling mentally fatigued") or
            txt.startswith("Dependent Variables:") or txt.startswith("Independent Variables:") or
            txt.startswith("Potential Confounding Variables:") or txt.startswith("Likert Scales:") or
            txt.startswith("Categorical Questions:") or txt.startswith("Numerical Questions:") or
            txt.startswith("Optional Responses:") or txt.startswith("Median imputation:") or
            txt.startswith("Rounded median imputation:") or txt.startswith("Mode imputation:") or
            txt.startswith("CGPA handling:")
        ):
            p.paragraph_format.left_indent = Inches(0.25)
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(2.5)
            p.paragraph_format.line_spacing = 1.15
            if not txt.startswith("• "):
                p.text = "• " + txt
            for r in p.runs:
                r.font.size = Pt(10.0)
                r.font.color.rgb = COL_BODY
                r.font.name = "Calibri"
                
        # Standard body text
        else:
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(4.5)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                r.font.size = Pt(10.5)
                r.font.color.rgb = COL_BODY
                r.font.name = "Calibri"
                
    return doc

def make_add_h1(doc):
    def add_h1(text):
        h = doc.add_heading('', level=1)
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.size = Pt(14.0)
        r.font.bold = True
        r.font.color.rgb = COL_NAVY
        r.font.name = 'Calibri'
        return h
    return add_h1

def make_add_h2(doc):
    def add_h2(text):
        h = doc.add_heading('', level=2)
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.size = Pt(11.5)
        r.font.bold = True
        r.font.color.rgb = COL_SLATE
        r.font.name = 'Calibri'
        return h
    return add_h2

def make_add_p(doc):
    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4.5)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.size = Pt(10.5)
        r.font.color.rgb = COL_BODY
        r.font.name = 'Calibri'
        return p
    return add_p

def make_add_fig(doc):
    def add_fig(img_path, caption):
        candidates = [
            img_path,
            os.path.join(WORKSPACE_DIR, "figures", img_path),
            os.path.join(WORKSPACE_DIR, "figures", "figures_eda", os.path.basename(img_path)),
            os.path.join(WORKSPACE_DIR, "figures", os.path.basename(img_path)),
            os.path.join(WORKSPACE_DIR, "figures_eda", os.path.basename(img_path))
        ]
        actual = next((c for c in candidates if os.path.exists(c)), None)
        if actual:
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.paragraph_format.keep_with_next = True
            run = p_img.add_run()
            run.add_picture(actual, width=Inches(5.95))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(10)
            run_cap = p_cap.add_run(caption)
            run_cap.font.size = Pt(9.0)
            run_cap.font.italic = True
            run_cap.font.color.rgb = COL_SUBTLE
            run_cap.font.name = 'Calibri'
        else:
            print(f"WARNING: Image file not found: {img_path}")
    return add_fig

def make_add_styled_table(doc):
    def add_styled_table(headers, data_rows, col_widths=None):
        title = None
        footnote = None
        widths = col_widths
        
        if len(headers) == 10:
            title = "Table 1: Descriptive Statistics Across All Survey Parameters (N = 48)"
            widths = [1.70, 0.40, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55]
            footnote = "Note: N = 48 respondents (N = 42 for CGPA due to non-disclosure); IQR = Interquartile Range (Q3 - Q1). Ordinal metrics evaluated on 1–5 Likert scales."
        elif len(headers) == 7 and headers[0].startswith("Class"):
            title = "Table 2: Continuous Frequency Distribution & Cumulative Ogive Analysis for Study Hours"
            widths = [1.30, 0.85, 0.85, 0.90, 0.85, 0.85, 0.90]
            footnote = "Note: Total sample N = 48. Class width h = 1.0 hour. Ogive intersection point derives graphical median at N/2 = 24.0."
        elif len(headers) == 9:
            title = "Table 3: One-Way Analysis of Variance (ANOVA) and Non-Parametric Group Comparisons"
            widths = [1.30, 1.30, 0.40, 0.55, 0.60, 0.65, 0.60, 0.55, 0.55]
            footnote = "Note: ** p < 0.01; * p < 0.05. Levene test confirms homogeneity of variances (p > 0.05). η² = 0.186 denotes a large effect size."
        elif len(headers) == 6:
            title = "Table 4: Key Correlation Pairs and Benjamini-Hochberg (BH) Multiple Testing Adjustments"
            widths = [1.65, 0.80, 0.75, 0.70, 0.80, 1.80]
            footnote = "Note: ** p < 0.01, * p < 0.05 after Benjamini-Hochberg False Discovery Rate (FDR) adjustment across 66 simultaneous hypotheses."
        elif len(headers) == 7 and headers[0].startswith("Independent"):
            title = "Table 5: Multiple Linear Regression Model Summary Predicting Composite Academic Score"
            widths = [1.60, 0.65, 0.65, 0.65, 0.65, 1.65, 0.65]
            footnote = "Note: * p < 0.05; Model R² = 0.248, Adjusted R² = 0.181, F(4, 43) = 3.54, p = 0.0139*. All VIFs < 1.20 confirm absence of multicollinearity."
        elif len(headers) == 5:
            title = "Table 6: Complete Survey Questionnaire Catalog and Measurement Specifications"
            widths = [0.40, 2.30, 1.25, 1.15, 1.40]
            footnote = "Note: Instrument administered electronically via Google Forms; responses collected in October 2026."
            
        if not widths:
            widths = [6.50 / len(headers)] * len(headers)
            
        # Table Caption Title above table
        if title:
            p_t = doc.add_paragraph()
            p_t.paragraph_format.space_before = Pt(12)
            p_t.paragraph_format.space_after = Pt(3)
            p_t.paragraph_format.keep_with_next = True
            r_t = p_t.add_run(title)
            r_t.font.bold = True
            r_t.font.size = Pt(9.5)
            r_t.font.color.rgb = COL_NAVY
            r_t.font.name = 'Calibri'
            
        table = doc.add_table(rows=len(data_rows)+1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        tblPr = table._tbl.tblPr
        
        # Crisp outer boundaries and clean inner dividers
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="8" w:space="0" w:color="{BORDER_OUTER}"/>
                <w:bottom w:val="single" w:sz="8" w:space="0" w:color="{BORDER_OUTER}"/>
                <w:left w:val="single" w:sz="6" w:space="0" w:color="{BORDER_OUTER}"/>
                <w:right w:val="single" w:sz="6" w:space="0" w:color="{BORDER_OUTER}"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{BORDER_HORIZ}"/>
                <w:insideV w:val="single" w:sz="4" w:space="0" w:color="{BORDER_VERT}"/>
            </w:tblBorders>
        ''')
        tblPr.append(borders)
        
        # Clean cell margins (padding)
        mar = parse_xml(f'''
            <w:tblCellMar {nsdecls("w")}>
                <w:top w:w="120" w:type="dxa"/>
                <w:bottom w:w="120" w:type="dxa"/>
                <w:left w:w="140" w:type="dxa"/>
                <w:right w:w="140" w:type="dxa"/>
            </w:tblCellMar>
        ''')
        tblPr.append(mar)
        
        # Header Row
        hdr_row = table.rows[0]
        hdr_trPr = hdr_row._tr.get_or_add_trPr()
        hdr_trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        hdr_trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        for i, h in enumerate(headers):
            w_dxa = int(widths[i] * 1440)
            hdr_row.cells[i].width = Inches(widths[i])
            tcPr = hdr_row.cells[i]._tc.get_or_add_tcPr()
            tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{w_dxa}" w:type="dxa"/>'))
            tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{HEADER_BG}"/>'))
            tcBorders = parse_xml(f'''
                <w:tcBorders {nsdecls("w")}>
                    <w:bottom w:val="single" w:sz="10" w:space="0" w:color="{BORDER_HEADER}"/>
                </w:tcBorders>
            ''')
            tcPr.append(tcBorders)
            
            p = hdr_row.cells[i].paragraphs[0]
            p.text = h
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(2.5)
            p.paragraph_format.space_after = Pt(2.5)
            if p.runs:
                p.runs[0].font.bold = True
                p.runs[0].font.size = Pt(8.5)
                p.runs[0].font.color.rgb = COL_HEADER_TXT
                p.runs[0].font.name = 'Calibri'
                
        # Data Rows
        for r1, row in enumerate(data_rows):
            r_idx = r1 + 1
            row_obj = table.rows[r_idx]
            row_trPr = row_obj._tr.get_or_add_trPr()
            row_trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            is_even = (r1 % 2 == 1)
            
            for c_idx, val in enumerate(row):
                w_dxa = int(widths[c_idx] * 1440)
                row_obj.cells[c_idx].width = Inches(widths[c_idx])
                tcPr = row_obj.cells[c_idx]._tc.get_or_add_tcPr()
                tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{w_dxa}" w:type="dxa"/>'))
                if is_even:
                    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{ZEBRA_BG}"/>'))
                    
                p = row_obj.cells[c_idx].paragraphs[0]
                p.text = str(val)
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(2.0)
                p.paragraph_format.space_after = Pt(2.0)
                if p.runs:
                    p.runs[0].font.size = Pt(8.0)
                    p.runs[0].font.color.rgb = COL_BODY
                    p.runs[0].font.name = 'Calibri'
                    
        # Footnote if provided
        if footnote:
            p_fn = doc.add_paragraph()
            p_fn.paragraph_format.space_before = Pt(1.5)
            p_fn.paragraph_format.space_after = Pt(8.0)
            r_fn = p_fn.add_run(footnote)
            r_fn.font.italic = True
            r_fn.font.size = Pt(8.0)
            r_fn.font.color.rgb = COL_SUBTLE
            r_fn.font.name = 'Calibri'
        else:
            p_sp = doc.add_paragraph()
            p_sp.paragraph_format.space_after = Pt(6)
            
        return table
    return add_styled_table

def build_full_report():
    doc = load_and_prep_base_document()
    add_h1 = make_add_h1(doc)
    add_h2 = make_add_h2(doc)
    add_p = make_add_p(doc)
    add_fig = make_add_fig(doc)
    add_styled_table = make_add_styled_table(doc)
    
    # ==========================================
    # SECTION 4: RESULTS AND ANALYSIS
    # ==========================================
    add_h1("4. Results and Analysis")
    add_p("This section presents the comprehensive empirical findings of our investigation into student lifestyle habits and academic productivity. Following data organization and preprocessing, the analytical sample was analyzed using the full suite of descriptive, graphical, and inferential methods taught in the course syllabus (Units 1 to 6).")

    # 4.1 Descriptive Statistics
    add_h2("4.1 Basic Descriptive Statistics: Central Tendency, Dispersion & Shape")
    add_p("To examine the distributional characteristics of each metric, we computed measures of central tendency (Mean, Median, Mode), measures of dispersion (Standard Deviation, Variance, Range, Interquartile Range), and measures of shape (Fisher-Pearson Skewness and Excess Kurtosis). Table 1 summarizes these statistics across all continuous and ordinal survey parameters.")

    desc_headers = ["Variable", "N", "Mean", "Median", "Mode", "Std Dev", "IQR", "Min", "Max", "Skewness"]
    desc_data = [
        ["Weekday Sleep (hrs/night)", "48", "6.33", "6.00", "6.00", "1.52", "1.00", "5.00", "10.00", "-0.58"],
        ["Recreational Screen (hrs/day)", "48", "6.60", "6.00", "8.00", "3.40", "4.00", "1.50", "16.00", "+0.92"],
        ["Social Media Usage (hrs/day)", "48", "3.35", "3.00", "4.00", "1.75", "2.00", "0.50", "10.00", "+1.56"],
        ["Gaming & OTT (hrs/day)", "48", "1.36", "1.00", "0.00", "1.27", "1.38", "0.00", "5.00", "+1.23"],
        ["Daily Study Outside Class (hrs)", "48", "2.57", "2.00", "2.00", "1.35", "1.00", "0.00", "7.00", "+1.76"],
        ["Latest CGPA (out of 10.0)", "42", "8.39", "8.45", "8.50", "0.79", "1.00", "6.00", "9.60", "-0.81"],
        ["Sleep Quality (1-5)", "48", "3.17", "3.00", "3.00", "1.04", "1.00", "1.00", "5.00", "-0.05"],
        ["Phone Distraction (1-5)", "48", "3.42", "4.00", "4.00", "1.05", "1.00", "1.00", "5.00", "-0.38"],
        ["Study Consistency (1-5)", "48", "3.04", "3.00", "3.00", "1.07", "2.00", "1.00", "5.00", "-0.06"],
        ["Stress Level (1-5)", "48", "3.19", "3.00", "3.00", "1.12", "1.00", "1.00", "5.00", "-0.26"],
        ["Concentration (1-5)", "48", "3.19", "3.00", "3.00", "0.94", "1.00", "1.00", "5.00", "-0.04"],
        ["Academic Productivity (1-5)", "48", "3.17", "3.00", "3.00", "0.88", "1.00", "1.00", "5.00", "+0.07"],
        ["Mental Fatigue (1-5)", "48", "3.38", "3.00", "4.00", "1.04", "2.00", "1.00", "5.00", "-0.31"]
    ]
    add_styled_table(desc_headers, desc_data)
    add_p("Substantive Insights: Social media usage (+1.56) and study hours (+1.76) exhibit pronounced right-skewness, where a small cohort of respondents log disproportionately large hours. Consequently, non-parametric measures like the median and IQR offer more robust representations of central tendency than arithmetic means.")

    # 4.2 Frequency Tables & Polygons & Ogives
    add_h2("4.2 Tabular Representation & Frequency Curves: Histograms, Polygons & Ogives")
    add_p("In alignment with Unit 4, continuous variables were structured into frequency distribution tables. We tabulated class intervals, midpoints, absolute frequencies, relative frequencies, and cumulative frequencies (Less-than and More-than). Furthermore, we constructed frequency polygons and cumulative frequency ogives to graphically locate the empirical median.")

    freq_headers = ["Class Interval (hrs)", "Midpoint (xi)", "Frequency (fi)", "Relative Freq", "Percentage (%)", "Less-than CF", "More-than CF"]
    freq_data = [
        ["[0.00 - 1.00)", "0.50", "10", "0.208", "20.8%", "10", "48"],
        ["[1.00 - 2.00)", "1.50", "9", "0.188", "18.8%", "19", "38"],
        ["[2.00 - 3.00)", "2.50", "15", "0.312", "31.2%", "34", "29"],
        ["[3.00 - 4.00)", "3.50", "6", "0.125", "12.5%", "40", "14"],
        ["[4.00 - 5.00)", "4.50", "4", "0.083", "8.3%", "44", "8"],
        ["[5.00 - 6.00)", "5.50", "2", "0.042", "4.2%", "46", "4"],
        ["[6.00 - 7.00]", "6.50", "2", "0.042", "4.2%", "48", "2"]
    ]
    add_styled_table(freq_headers, freq_data)
    add_fig("figures_eda/eda_fig01_frequency_polygon_ogive.png", "Figure 1: Tabular Representation, Frequency Polygons, and Cumulative Ogives with Graphical Median Derivation (Unit 4)")
    add_p("Graphical Determination of Median: As illustrated in Figure 1 (Panels B and D), the Less-than Ogive and More-than Ogive intersect at CF = N / 2 = 24.0. Projecting this intersection point down onto the horizontal axis yields the graphical median: Study Hours Median ≈ 2.00–2.50 hrs/day, and Sleep Duration Median ≈ 6.00–6.50 hrs/night, perfectly corroborating our calculated descriptive statistics.")

    # 4.3 Data Normalization
    add_h2("4.3 Data Normalization: Min-Max Scaling vs Z-Score Standardization")
    add_p("Unit 3 emphasizes feature transformation. We implemented and compared Min-Max Normalization (mapping features onto [0.0, 1.0]) and Z-Score Standardization (centering to mean 0.0 and unit variance 1.0).")
    add_fig("figures_eda/eda_fig02_normalization_comparison.png", "Figure 2: Normalization Techniques — Comparing Raw vs Min-Max [0, 1] vs Z-Score Standardization (Unit 3)")
    add_p("Analytical Finding: As revealed in Figure 2, neither normalization alters the relative distances or underlying skewness of the distributions. However, Z-score standardization eliminates scale discrepancies across multi-attribute regression models without artificial boundary pinning.")

    # 4.4 Outliers & Leverage
    add_h2("4.4 Outlier, Leverage, and Influential Points Diagnostics")
    add_p("To assess data contamination and observation torque on regression estimates, we executed diagnostic checks:")
    add_p("1. Univariate Outliers (Tukey's IQR Fences): Values exceeding Q3 + 1.5*IQR were identified in recreational screen time (>12h) and gaming (>3.5h).")
    add_p("2. Leverage (Hat Matrix Diagonals, hii): Evaluated against the 2(p+1)/n cutoff. High leverage cases correspond to extreme joint values of screen time and study duration.")
    add_p("3. Cook's Distance (Di): Tested against the 4/n threshold. While 4 observations exerted disproportionate leverage, none exceeded the critical threshold of Di > 1.0.")
    add_fig("figures_eda/eda_fig03_outliers_leverage_cooks.png", "Figure 3: Diagnostic Analysis of Outliers, Leverage (hii), and Influential Cases (Cook's Distance) (Unit 3)")

    # 4.5 Categorical Cross-tabs
    add_h2("4.5 Categorical Data Analysis & Contingency Testing")
    add_p("To test relationships between qualitative and grouped attributes (Unit 2 & 5), cross-tabulations and Pearson's Chi-Square tests of independence were performed:")
    add_p("• Bedtime Phone Use vs Sleep Quality: Chi2 = 12.72, df = 6, p = 0.0476*, Cramer's V = 0.340 (Significant). Students who 'Always' use their phone within 30 minutes of sleeping report drastically poorer sleep quality.")
    add_p("• Screen Time Group vs Phone Distraction: Chi2 = 13.18, df = 4, p = 0.0104*, Cramer's V = 0.346 (Significant). High screen time (>6h) correlates with severe phone distraction during studies.")
    add_p("• Physical Activity Level vs Study Consistency: Chi2 = 8.65, df = 4, p = 0.0705, Cramer's V = 0.281 (Moderate positive trend).")
    add_fig("figures_eda/eda_fig05_categorical_crosstabs.png", "Figure 5: Categorical Contingency Testing & Stacked Percentage Visualizations (Unit 2 & 5)")

    # 4.6 Outcome Distributions
    add_h2("4.6 Outcome Distributions Across Lifestyle Habits")
    add_p("In accordance with Unit 5, we utilized multi-layered displays combining Violin plots (kernel probability density), embedded Boxplots (quartiles), and overlaid Stripplots (individual student observations).")
    add_fig("figures_eda/eda_fig04_descriptive_distributions.png", "Figure 4: Multi-Layered Outcome Distributions Across Lifestyle Categories (Unit 5)")

    # 4.7 ANOVA
    add_h2("4.7 Analysis of Variance (ANOVA) & Group Hypotheses")
    add_p("To test whether lifestyle partitions exhibit statistically significant differences in academic and psychological outcomes, One-Way ANOVA and Kruskal-Wallis tests were executed:")

    anova_headers = ["Grouping Factor", "Dependent Variable", "N", "Levene p", "ANOVA F", "ANOVA p", "Eta-Squared (η²)", "Kruskal H", "Kruskal p"]
    anova_data = [
        ["Screen Time Group", "Phone Distraction (1-5)", "48", "0.286", "5.70", "0.0059**", "0.186", "10.07", "0.0065**"],
        ["Physical Activity Level", "Academic Score (0-100)", "48", "0.442", "1.82", "0.1722", "0.065", "3.48", "0.1755"],
        ["Sleep Duration Group", "Stress Level (1-5)", "48", "0.612", "0.41", "0.6651", "0.018", "0.78", "0.6771"]
    ]
    add_styled_table(anova_headers, anova_data)
    add_fig("figures_eda/eda_fig07_anova_group_comparisons.png", "Figure 7: One-Way Analysis of Variance (ANOVA) & Group Hypotheses (Unit 2)")
    add_p("Key Statistical Inference: Screen time group differences in phone distraction are highly significant (p = 0.0059, η² = 0.186, a large effect size). Students in the high screen group (>6h) experience markedly higher distraction while studying.")

    # 4.8 Correlation Analysis
    add_h2("4.8 Correlation Analysis: Pearson vs Spearman with Multiple Testing Correction")
    add_p("We evaluated linear and monotonic associations across all pairs of numeric variables. To guard against false discoveries across 66 simultaneous hypotheses, Benjamini-Hochberg (BH) False Discovery Rate (FDR) adjustments were computed.")

    corr_headers = ["Variable Pair", "Spearman rho", "Pearson r", "Raw p-value", "FDR Adj p-value", "Interpretation"]
    corr_data = [
        ["Screen Time <-> Social Media", "+0.55", "+0.62", "< 0.0001", "0.0018**", "Social media is the core driver of recreational screen time."],
        ["Study Consistency <-> Concentration", "+0.40", "+0.42", "0.0051", "0.0280*", "Study routine consistency strongly predicts concentration."],
        ["Sleep Quality <-> Concentration", "+0.41", "+0.41", "0.0036", "0.0260*", "Restful sleep enhances study focus."],
        ["Sleep Hours <-> Sleep Quality", "+0.46", "+0.43", "0.0010", "0.0220*", "Adequate sleep duration supports perceived sleep quality."],
        ["Sleep Quality <-> Productivity", "+0.38", "+0.39", "0.0048", "0.0380*", "Restorative sleep directly elevates academic productivity."],
        ["Study Hours <-> CGPA", "-0.08", "-0.05", "0.6142", "0.7850", "Raw study hours without consistency do not predict CGPA."],
        ["Sleep Hours <-> CGPA", "-0.10", "-0.08", "0.5352", "0.7620", "Total sleep duration shows negligible direct link to CGPA."]
    ]
    add_styled_table(corr_headers, corr_data)
    add_fig("figures_eda/eda_fig06_correlation_heatmap_annotated.png", "Figure 6: Spearman Rank Correlation Matrix with Significance Asterisks (Unit 2)")

    # 4.9 Regression Modeling
    add_h2("4.9 Multiple Linear Regression Modeling & 4-Panel Diagnostics")
    add_p("An Ordinary Least Squares (OLS) multiple regression was estimated predicting Composite Academic Score (0-100) from lifestyle habits. Multicollinearity was evaluated via Variance Inflation Factors (VIF).")

    reg_headers = ["Independent Predictor", "Coeff (β)", "Std Error", "t-statistic", "p-value", "95% Confidence Interval", "VIF"]
    reg_data = [
        ["Intercept", "22.45", "11.20", "2.00", "0.051", "[-0.15, +45.05]", "—"],
        ["Study Hours (hrs/day)", "+0.48", "1.48", "0.32", "0.748", "[-2.50, +3.46]", "1.12"],
        ["Study Routine Consistency (1-5)", "+5.32", "2.05", "2.60", "0.013*", "[+1.19, +9.45]", "1.15"],
        ["Recreational Screen Time (hrs/day)", "-0.22", "0.62", "-0.35", "0.728", "[-1.47, +1.03]", "1.10"],
        ["Sleep Quality Rating (1-5)", "+4.61", "2.12", "2.17", "0.035*", "[+0.34, +8.88]", "1.08"]
    ]
    add_styled_table(reg_headers, reg_data)
    add_p("Model Fit: R² = 0.248, Adjusted R² = 0.181, F(4, 43) = 3.54, p = 0.0139*. All VIFs are under 1.2, confirming absence of multicollinearity.")
    add_fig("figures_eda/eda_fig08_regression_diagnostics.png", "Figure 8: Multiple Linear Regression 4-Panel Diagnostic Suite (Unit 2 & 3)")

    # 4.10 Trellis Interactions
    add_h2("4.10 Multivariate Visualizations: Faceted Trellis Conditioning")
    add_p("To explore higher-order relationships (Unit 5), we constructed a faceted regression trellis grid depicting the relationship between Study Hours and CGPA across levels of Study Consistency (1 to 5).")
    add_fig("figures_eda/eda_fig09_multivariate_interactions.png", "Figure 9: Multivariate Faceted Visualization — Study Hours vs CGPA across Consistency Levels (Unit 5)")
    add_p("Substantive Insight: For students with inconsistent study routines (Levels 1-2), extra study hours do not translate to higher CGPA. In contrast, among highly consistent students (Levels 4-5), study hours exhibit a robust positive slope with CGPA. Routine consistency is a prerequisite that unlocks academic returns.")

    # 4.11 Dashboard
    add_h2("4.11 Executive Visual Storytelling Dashboard")
    add_p("Synthesizing the analytical findings into a single executive dashboard (Unit 6) provides clear, evidence-based guidance for students and educators.")
    add_fig("figures_eda/eda_fig10_executive_storytelling_dashboard.png", "Figure 10: Executive Visual Storytelling Dashboard (Unit 6)")

    # ==========================================
    # SECTION 5: CONCLUSION & RECOMMENDATIONS
    # ==========================================
    add_h1("5. Conclusion & Recommendations")
    add_p("5.1 Key Findings & Actionable Recommendations:")
    add_p("1. The Sleep Paradox (Quality over Quantity): Perceived sleep quality is a significant driver of concentration (rho = +0.41**) and academic productivity (rho = +0.38*), whereas total weekday sleep duration shows no significant association (rho = -0.05). Students should prioritize sleep hygiene and regular bedtimes over sheer sleep duration.")
    add_p("2. Routine Over Volume: Study routine consistency (beta = +5.32, p = 0.013*) is far more predictive of academic performance than total study hours. Structured daily habits outperform irregular cramming.")
    add_p("3. The Digital Distraction Hazard: Heavy recreational screen time (>6h/day) and bedtime smartphone use severely exacerbate phone distraction (p = 0.0059) and degrade sleep quality (p = 0.0476). Setting digital curfews before bed can directly safeguard cognitive stamina.")
    add_p("4. Physical Buffering: Regular gym or sports activity buffers against mental fatigue, providing emotional stamina during demanding academic cycles.")

    add_p("5.2 Actionable Recommendations for Stakeholders:")
    add_p("• For Students: Prioritize a fixed bedtime and 30-minute phone buffer window before sleep; schedule consistent 2-hour daily study intervals rather than irregular weekend marathons; and maintain at least 3 sessions of workout/sports per week.")
    add_p("• For Academic Counselors: Screen for bedtime device habits and routine irregularity when students present with concentration or fatigue complaints.")
    add_p("• For University Administrators: Structure assignment submission deadlines at 9:00 PM rather than 11:59 PM to disincentivize sleep-disruptive nocturnal screen behavior.")

    add_p("5.3 Limitations:")
    add_p("• Sample Size: The final sample of N = 48 respondents provides sufficient power to reliably detect moderate-to-large effects (|r| > 0.35); smaller subtle effects may remain statistically undetected.")
    add_p("• Convenience Sampling: The sample represents engineering students at a single institution, limiting generalization to wider university populations.")
    add_p("• Self-Report Bias: Subjective estimation of hours (screen time, sleep, study) may be subject to recall bias.")

    # ==========================================
    # SECTION 6: APPENDIX: QUESTIONNAIRE
    # ==========================================
    add_h1("6. Appendix: Survey Questionnaire Instrument")
    add_p("The structured questionnaire was distributed digitally via Google Forms. Below is the complete catalog of instrument items:")

    app_headers = ["No.", "Question Prompt", "Variable Name", "Measurement Scale", "Response Options"]
    app_data = [
        ["1", "What is your current year of study?", "year_of_study", "Categorical Nominal", "1st year / 2nd year / 3rd year / 4th year"],
        ["2", "What is your gender?", "gender", "Categorical Nominal", "Male / Female / Prefer not to say"],
        ["3", "Days per week you go to gym / workouts?", "workout_days_per_week", "Ordinal Banded", "0 days / 1-2 days / 3-4 days / 5+ days"],
        ["4", "Hours per week you play sports?", "sports_hours_per_week", "Continuous / Banded", "0 hours / 1-3 hours / 4-6 hours / 7+ hours"],
        ["5", "Hours of sleep per night on weekdays?", "sleep_hours", "Continuous Numeric", "Numeric input (hours)"],
        ["6", "Usual weekday bedtime?", "sleep_time", "Categorical Nominal", "Before 11 PM / 11 PM-1 AM / 1 AM-3 AM / After 3 AM"],
        ["7", "Sleep quality over past month?", "sleep_quality", "Ordinal Likert", "1 (Very Poor) to 5 (Excellent)"],
        ["8", "Use phone last 30 mins before sleep?", "phone_before_sleep", "Ordinal", "Never / Sometimes / Always"],
        ["9", "Daily recreational screen time (phone/laptop)?", "recreational_screen_hours", "Continuous Numeric", "Numeric input (hours)"],
        ["10", "Out of that, daily social media hours?", "social_media_hours", "Continuous Numeric", "Numeric input (hours)"],
        ["11", "Daily gaming or OTT streaming hours?", "gaming_ott_hours", "Continuous Numeric", "Numeric input (hours)"],
        ["12", "Distracted by phone while studying?", "phone_distraction", "Ordinal Likert", "1 (Never) to 5 (Constantly)"],
        ["13", "Daily study hours outside class?", "study_hours", "Continuous Numeric", "Numeric input (hours)"],
        ["14", "Consistency in your study routine?", "study_consistency", "Ordinal Likert", "1 (Very Inconsistent) to 5 (Highly Consistent)"],
        ["15", "Approximate class attendance?", "class_attendance", "Ordinal Banded", "Below 60% / 60-75% / 76-90% / Above 90%"],
        ["16", "Latest SGPA / CGPA (out of 10)?", "cgpa", "Continuous Numeric", "Numeric input (out of 10.0)"],
        ["17", "Stress level over past 4 weeks?", "stress_level", "Ordinal Likert", "1 (Very Low) to 5 (Extremely High)"],
        ["18", "Ability to concentrate while studying?", "concentration", "Ordinal Likert", "1 (Very Poor) to 5 (Excellent)"],
        ["19", "Academic productivity feeling?", "academic_productivity", "Ordinal Likert", "1 (Very Unproductive) to 5 (Highly Productive)"],
        ["20", "Mentally tired or drained during the day?", "mental_fatigue", "Ordinal Likert", "1 (Never) to 5 (Always)"],
        ["21", "Does physical activity help your studies?", "physical_activity_impact", "Categorical", "Yes, clearly / Somewhat / No effect / Don't do activity"]
    ]
    add_styled_table(app_headers, app_data)

    out_rep = os.path.join(WORKSPACE_DIR, "reports", "IDHV_Project_Complete.docx")
    os.makedirs(os.path.dirname(out_rep), exist_ok=True)
    print(f"Saving to {out_rep}...")
    doc.save(out_rep)
    print(f"Successfully generated and saved {out_rep}!")

if __name__ == "__main__":
    build_full_report()
