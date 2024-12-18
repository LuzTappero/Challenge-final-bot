import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def calculate_similarity(query_text, document_text):
    tokens1 = word_tokenize(query_text.lower())
    tokens2 = word_tokenize(document_text.lower())
    stop_words = set(stopwords.words('spanish'))
    tokens1 = [token for token in tokens1 if token not in stop_words]
    tokens2 = [token for token in tokens2 if token not in stop_words]

    # Convertir las listas en conjuntos antes de calcular la distancia de Jaccard
    set_tokens1 = set(tokens1)
    set_tokens2 = set(tokens2)

    similitud = nltk.jaccard_distance(set_tokens1, set_tokens2)
    print(f"Similitud de Jaccard: {similitud}")