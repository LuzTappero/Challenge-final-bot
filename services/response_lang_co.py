from langchain_cohere import ChatCohere
from langchain.prompts import PromptTemplate
from fastapi import HTTPException
from langchain.memory import ConversationBufferMemory
from config.cohere_config import cohere_config
from dotenv import load_dotenv
import os


load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere_config()

conversation_history = []
MAX_HISTORY_LENGTH = 5


preamble = """
Eres un asistente virtual especializado en proporcionar información precisa y detallada sobre preguntas especificas de medicamentos.
Sigue estrictamente las siguientes directrices para tus respuestas:

1. **Fuentes de información:**
    - Utiliza únicamente la información contenida en el documento proporcionado y repsonde especificamente a la pregnta realizada sin agregar contenido extra.
    - Si no dispones de la información solicitada, indica educadamente que no la tienes.

2. **Formato de las respuestas:**
    - Organiza la información de manera clara y ordenada.

3. **Estilo del lenguaje:**
    - Emplea un lenguaje profesional y científico.
    - Asegúrate de que las respuestas sean coherentes y consistentes ante preguntas similares o idénticas.
    - Conecta las ideas de manera fluida y proporcionando detalles completos.

4. **Idioma:**
    - Responde siempre en español, independientemente del idioma en que se formule la pregunta.

Recuerda: tu objetivo es ofrecer respuestas precisas, organizadas y fáciles de entender sobre medicamentos.
"""

def generate_response_with_db_langchain(relevant_text, query_text):
    """
    Generate a response based on the relevant text and query text using a language model.
    """
    try:
        if not relevant_text or not query_text:
            raise ValueError("Relevant text and query text are required.")

        context = "\n".join(
            [f"User: {item['query']}\nAsistent: {item['response']}" for item in conversation_history[-MAX_HISTORY_LENGTH:]]
        )
        cohere_model = ChatCohere(
            cohere_api_key= cohere_api_key,
            model="command-r-plus-08-2024",
            temperature=0.0,
            max_tokens=400
            )

        prompt = PromptTemplate(
            input_variables=["chat_history", "preamble", "relevant_text", "query_text"],
            template=(
                f"{preamble}\n\n"
                f"Chat History:\n{context}\n\n"
                f"Relevant text: {relevant_text}\n\nQuestion: {query_text}"
                f"\n\nQuestion:{query_text}"
                f"\n\nAnswer:"
            )
        )

        response = cohere_model.invoke(
            prompt.format(
                relevant_text=relevant_text,
                query_text=query_text)
        )

        response = response.content if hasattr(response, "content") else response
        if not response:
            raise HTTPException(status_code=500, detail="Lo siento, no pude generar una respuesta adecuada a partir de la información disponible.")

        conversation_history.append({
            "query": query_text,
            "response": response,
            "relevant_text": relevant_text
        })
        return response
    except Exception as e:
        print(f"Error during response generation: {e}")
        raise


