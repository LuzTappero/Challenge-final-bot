import os
import pdfplumber

pdf_folder = '../documents'
output_folder = '../output'
os.makedirs(output_folder, exist_ok=True)

def extract_text_from_pdf(pdf_path, output_path):
    """
    Extracts text from a PDF file and saves it to a text file.

    Parameters:
    - pdf_path (str): Path to the input PDF file.
    - output_path (str): Path where the extracted text will be saved as a text file.

    Returns:
    None
    """
    try:
        # Open the PDF file
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() + "\n"

        with open(output_path, "w", encoding="utf-8") as archivo_texto:
            archivo_texto.write(text)
        print(f"Extracted text saved to: {output_path}")
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")

# Process all pdf files in the folder
for archive in os.listdir(pdf_folder):
    if archive.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, archive)
        output_path = os.path.join(output_folder, f"{os.path.splitext(archive)[0]}.txt")
        extract_text_from_pdf(pdf_path, output_path)


def count_total_characters(folder_path):
    """
    Count the total number of characters in all text files in a folder.
    """
    total_characters = 0
    for archive in os.listdir(folder_path):
        if archive.endswith(".txt"):
            archivo_path = os.path.join(folder_path, archive)
            with open(archivo_path, "r", encoding="utf-8") as f:
                contenido = f.read()
                total_characters += len(contenido)
    return total_characters

# Example usage
# folder_path = './output'
# total_characters = count_total_characters(folder_path)
# print(f"Total characters: {total_characters}")
#Total characters: : 136409