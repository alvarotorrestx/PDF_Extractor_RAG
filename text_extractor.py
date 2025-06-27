import os
import re
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path="Outline Plan for Leprechaun Animation Implementation.pdf"):
    """
    Extracts text from a PDF file, collapses whitespace, writes the text to a file,
    and returns the full text.
    """
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File '{pdf_path}' not found.")
        return ""

    try:
        reader = PdfReader(pdf_path)
        full_text = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

        # Collapse multiple spaces, newlines, and tabs
        full_text = re.sub(r'\s+', ' ', full_text).strip()

        with open("Selected_Document.txt", "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"✅ Text successfully extracted and saved to 'Selected_Document.txt'.")
        return full_text

    except Exception as e:
        print(f"❌ Failed to read or process the PDF: {e}")
        return ""

def main():
    extract_text_from_pdf()

if __name__ == '__main__':
    main()
