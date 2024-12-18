import re

def clean_relevant_text(results):
    """
    Limpia y formatea el texto relevante extraído.

    Parameters:
    - results (list): Lista de resultados donde 'page_content' contiene el texto.

    Returns:
    - str: Texto limpio y procesado.
    """
    # Reemplazar saltos de línea por espacios
    cleaned_text = results.replace("\n", " ")

    # Convertir todo el texto a minúsculas
    cleaned_text = cleaned_text.lower()

    # Asegurar que las unidades de medida tengan un espacio correcto
    cleaned_text = re.sub(r'(\d+\.\d+|\d+)\s*(mg|g|ml|cm|l|u)', r'\1 \2', cleaned_text)

    # Eliminar caracteres especiales no deseados, excepto algunos como letras, números, puntos, comas, etc.
    cleaned_text = re.sub(r'[^a-z0-9\s\.\-\,\(\)\%]', '', cleaned_text)
    return cleaned_text