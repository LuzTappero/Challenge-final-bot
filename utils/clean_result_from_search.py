import re

def clean_relevant_text(results):
    """
    Clean and process text from search results.

    Parameters:
    - results (list): List of search results with relevant text.

    Returns:
    - str: Cleaned and processed text.
    """
    # Replace newlines with spaces
    cleaned_text = results.replace("\n", " ")

    # Convert to lowercase
    cleaned_text = cleaned_text.lower()

    # Make sure units of measurement are spaced correctly.
    cleaned_text = re.sub(r'(\d+\.\d+|\d+)\s*(mg|g|ml|cm|l|u)', r'\1 \2', cleaned_text)

    #Remove unwanted special characters, except some such as letters, numbers, periods, commas, etc..
    cleaned_text = re.sub(r'[^a-z0-9\s\.\-\,\(\)\%]', '', cleaned_text)
    return cleaned_text