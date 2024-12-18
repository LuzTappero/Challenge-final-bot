from langchain_cohere import ChatCohere
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from config.cohere_config import cohere_config
from dotenv import load_dotenv
import os
from services.history_chat import get_chat_history


load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere_config()

conversation_history = []
MAX_HISTORY_LENGTH = 5


preamble = """
Eres un asistente virtual especializado en proporcionar información precisa y detallada sobre medicamentos.
Sigue estrictamente las siguientes directrices para tus respuestas:

1. **Fuentes de información:**
    - Utiliza únicamente la información contenida en el documento proporcionado.
    - Si no dispones de la información solicitada, indica educadamente que no la tienes.

2. **Formato de las respuestas:**
    - Organiza la información de manera clara y ordenada.
    - Cuando identifiques un (: -) en la respuesta, acomodar los - en una nueva lista.

3. **Estilo del lenguaje:**
    - Emplea un lenguaje profesional y científico.
    - Asegúrate de que las respuestas sean coherentes y consistentes ante preguntas similares o idénticas.
    - Utiliza un estilo conversacional, conectando ideas de manera fluida y proporcionando detalles completos.

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
            raise ValueError("El texto relevante o la consulta no pueden estar vacíos.")

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
            response = "Lo siento, no pude generar una respuesta adecuada."

        conversation_history.append({
            "query": query_text,
            "response": response,
            "relevant_text": relevant_text
        })
        return response
    except Exception as e:
        print(f"Error al generar respuesta con LangChain y Cohere: {e}")
        raise


