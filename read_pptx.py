import zipfile
import re

def extract_text_from_pptx(pptx_path):
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_xmls = [n for n in zf.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
        text_content = []
        for slide in sorted(slide_xmls):
            xml_content = zf.read(slide).decode('utf-8')
            # Extract all text between > and <
            matches = re.findall(r'>([^<]+)<', xml_content)
            # filter out pure whitespace
            matches = [m.strip() for m in matches if m.strip()]
            if matches:
                text_content.append(f"\n--- {slide} ---")
                text_content.append(" ".join(matches))
        return '\n'.join(text_content)

path = r"C:\Users\t3j4s\OneDrive\Desktop\SEBA\Smart-Expense-Behaviour-Analyser.pptx"
try:
    print(extract_text_from_pptx(path))
except Exception as e:
    print("Error:", e)
