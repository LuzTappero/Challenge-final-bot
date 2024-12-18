import nltk
from nltk.tokenize import word_tokenize

#NLTK(Natural Language Toolkit) is a Python package for natural language processing (NLP). It provides tools for tokenization, stemming, lemmatization, and other natural language processing tasks. This toolkit is used to analyze and manipulate natural language data, such as text, speech, and other forms of language.

def handle_predefined_queries(query_text):
    """
    Check if the query text matches a predefined query, and return a predefined response if it does.

    Parameters:
    - query_text (str): The query text to check.

    Returns:
    - str: The predefined response if the query text matches a predefined query, None otherwise.
    """
    print("entrando a handle predefined")
    tokens = word_tokenize(query_text.lower())
    # Check if the query text contains a greeting
    if any(token in ["hola", "buenas", "qué tal", "saludos"] for token in tokens):
        return "¡Hola! ¿En qué puedo ayudarte? Solo tengo información sobre medicamentos."
    # Check if the query text asks for user information
    elif any(token in ["¿quién soy?", "información de usuario"] for token in tokens):
        return "Lo siento, no manejo información personal de usuarios."
    # If none of the above, return None
    return None


