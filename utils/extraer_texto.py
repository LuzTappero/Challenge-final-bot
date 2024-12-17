import os
import pdfplumber

pdf_folder = '../documents'
output_folder = '../output'
os.makedirs(output_folder, exist_ok=True)

def extract_text_from_pdf(pdf_path, output_path):
    try:
        #page by page text extraction
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()+ "\n"

        # Save the extracted text to a new file
            with open(output_path, "w", encoding="utf-8") as archivo_texto:
                archivo_texto.write(text)
        print(f"Texto extraído y guardado en: {output_path}")
    except Exception as e:
        print(f"Error procesando {pdf_path}: {e}")


# Process all pdf files in the folder
for archive in os.listdir(pdf_folder):
    if archive.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, archive)
        output_path = os.path.join(output_folder, f"{os.path.splitext(archive)[0]}.txt")
        extract_text_from_pdf(pdf_path, output_path)