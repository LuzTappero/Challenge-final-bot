from config.cohere_config import cohere_config
# from langchain_cohere import ChatCohere
# from langchain.prompts import ChatPromptTemplate
# from langchain.chains import LLMChain
# from langchain.memory import ConversationBufferMemory

co = cohere_config()
conversation_history = []

def generate_response_with_db(relevant_text, query_text):
    """
    Generate a response based on the relevant text and query text using a language model.

    Parameters:
    - relevant_text (str): The text containing relevant information to answer the query.
    - query_text (str): The question or query to be answered.

    Returns:
    - str: The generated response from the language model.
    """
    # Define the system prompt with instructions for generating responses
    preamble  ="""
        *Eres un asistente especializado en información sobre medicamentos.
        *Utiliza solo la información contenida en el documento para elaborar tus respuestas, si no dispones de dicha información, indica que no la tienes.
        *Presenta la información de manera organizada y clara, utilizando listas con items simples.
        *Utiliza un lenguaje profesional y científico en tus respuestas.
        *Asegúrate de proporcionar respuestas consistentes y coherentes ante preguntas similares o idénticas.
        *Asegúrate de usar un estilo conversacional, conectando las ideas de manera coherente y proporcionando detalles completos.
        *Responde siempre en español, independientemente del idioma en que se haga la pregunta.
    """
    try:
        if not relevant_text or not query_text:
            raise ValueError("El texto relevante o la consulta no pueden estar vacíos.")
        context = "\n".join(
            [f"User: {item['query']}\nAsistent: {item['response']}" for item in conversation_history]
        )
        prompt_instrucctions = (
            f"{preamble}\n\nChat History:\n{context}\n\nRelevant text: {relevant_text}\n\nQuestion: {query_text}"
        )

        # Generate a response using the language model with specified parameters
        response = co.chat(
            model="command-r-plus-08-2024",
            messages=[{"role": "user", "content": prompt_instrucctions}],
            max_tokens=650,
            temperature=0.2
        )
        generated_response = response.message.content[0].text

        # Add the generated response to the conversation history
        conversation_history.append({
            "query": query_text,
            "response": generated_response,
            "relevant_text": relevant_text
        })

        # Return the generated response
        return generated_response

    except Exception as e:
        print(f"Error al generar respuesta con Cohere: {e}")
        raise
