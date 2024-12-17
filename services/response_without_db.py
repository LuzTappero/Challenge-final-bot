from config.cohere_config import cohere_config
from models.query_model import Query

co = cohere_config()

def generate_response_without_db(query: Query):
    """
    Generar una respuesta directamente usando LangChain con Cohere.

    Parameters:
    - query_text (str): La consulta del usuario.

    Returns:
    - str: La respuesta generada por el modelo.
    """
    # Definir el template del prompt
    try:
        # Instrucciones del prompt para guiar al modelo
        prompt_instructions = (
            f"Eres un asistente especializado en medicamentos. Responde de manera precisa "
            f"y profesional a la siguiente consulta: {query}"
        )

        # Llamar al modelo Cohere con las instrucciones
        response = co.chat(
            model="command-r-plus-08-2024",
            messages=[{"role": "user", "content": prompt_instructions}],
        )
        # Extraer el contenido del mensaje generado
        final_response = response.message.content[0].text
        print(final_response)
        return final_response
    except Exception as e:
        print(f"Error al generar la respuesta: {e}")
        return {"response": "Error al generar la respuesta"}


