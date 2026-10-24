import pypdf
reader = pypdf.PdfReader('Project_Report.pdf')
for i in range(5, len(reader.pages)):
    print(f'--- PAGE {i+1} ---')
    print(reader.pages[i].extract_text()[:600])
