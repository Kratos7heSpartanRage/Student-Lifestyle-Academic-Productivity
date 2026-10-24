try:
    import pypdf
    reader = pypdf.PdfReader('Project_Report.pdf')
    print('Num pages:', len(reader.pages))
    for i in range(min(5, len(reader.pages))):
        print(f'--- PAGE {i+1} ---')
        print(reader.pages[i].extract_text()[:600])
except Exception as e:
    print('Error with pypdf:', e)
    # try pypdf2 or pdftotext
