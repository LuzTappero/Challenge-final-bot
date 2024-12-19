# API Documentation

## Tabla de Contenidos
1. [Descripción](#descripción)
2. [Requisitos](#requisitos)
3. [Instalación y Configuración](#instalación-y-configuración)
4. [Herramientas utilizadas](#Herramientas-utilizadas)
5. [EndPoints](#endpoints)
   1. [POST /ask_question](#post-users)
6. [Errores](#errores)
7. [Ejemplos de Uso](#ejemplos-de-uso)
8. [Licencia](#licencia)

---

## Descripción

Esta API está desarrollada en Python utilizando Flask como framework y basada en arquitectura RAG (Retrieval-Augmented Generation), busca resolver el problema de la subutilización de la información contenida en los prospectos de medicamentos, ya que a pesar de ser una fuente de máximo valor, se encuentra desperdiciada, tanto en su formato físico (generando impactos medioambientales), cómo en su presentación dígital existente ya que la lectura de los mismos resulta tediosa y dificil de comprender.
El modelo fue entrenado con prospectos de medicamentos, lo que permite extraer y presentar la información de manera rápida, dinámica y accesible. El propósito de la API es facilitar el acceso a equipos médicos, investigadores, profesional de salud, agilizando el tiempo de tomas de decisiones. Además, tiene como objetivo promover la educación de los pacientes (como consumidores finales) proporcionándoles información clara y comprensible sobre medicamentos, sus usos, efectos secundarios y demás aspectos importantes.

---

## Requisitos

Lenguaje:
- Python 3.8 o superior
Librerias y herramientas:
- FastAPI
- Cohere
- Langchain
- Chroma DB
- nltk

---

## Instalación

1. Clonar el repositorio a un directorio local con el siguiente comando

    git clone [https://github.com/LuzTappero/Challenge-final-bot]

2. Creación de un entorno virtual con python

    python venv -m venv

3. Instalación de dependencias

    pip install -r requirements.txt

4. Configuración de variables de entorno

    COHERE_APY_KEY = "tu_clave_de_cohere"

5. Configuración de Chroma db(config/chromadb_config)

    Establecer un directorio local para almacenamiento de la información
    Asignar un nombre a la colección.

6.  Ejecución única de funciones para la creación de embeddings y almacenamiento en una base de datos vectorial
    La ejecución de estas funciones se realiza mediante la función process_file, ubicada en la carpeta utils. Esta función toma como parámetro la ruta (path) del archivo a procesar y ejecuta los siguientes pasos:
     - Creación de chunks: Divide el contenido del archivo en fragmentos manejables.
     -Generación de embeddings: Crea representaciones vectoriales de los fragmentos.
     - Almacenamiento en Chroma: Guarda los embeddings generados en la base de datos vectorial.

         Ejemplo de ejecución
         file_path = './output/CARDILIPEN-Bisoprolol fumarato.txt'
         process_file(file_path)

         Mensaje de salida
         "Documents added to Chroma with IDs: {ids} and embeddings: {len(embeddings)} embedding info {embeddings[0]}"
      

## Herramientas utilizadas

Este proyecto se desarrolló con una seria de herramientas y configuraciones para garantizar la eficiencia y escalabilidad. A continuación, se detallan las decisiones clave:

1. pdfplumber para la extracción de texto

    - Razón de elección: pdfplumber fue seleccionado por su capacidad robusta para manejar documentos PDF complejos, permitiendo extraer texto incluso de estructuras avanzadas como tablas, encabezados y pies de página.
    - Beneficio clave: La herramienta sobresale en el procesamiento de PDFs que contienen múltiples formatos de texto y diseño, lo que garantiza que el contenido del prospecto médico se extraiga con precisión sin pérdida de información relevante.

2. LangChain Recursive Text Splitter

- Razón de elección:
    Herramienta para generación de chunks.
    El tamaño del chunk size elegido fue de 2000 caracteres ya que de ésta manera garantiza un balance entre la retención del contexto y la capacidad del modelo de embeddings para procesar cada fragmento.
    El solapamiento elegido fue de 200 caracteres, ésto asegura que no se pierda información clave del documento, especialmente en textos donde cada palabra es sumamente importante.

- Beneficio clave:
    Esta técnica permite dividir el texto en fragmentos procesables sin sacrificar la coherencia contextual, optimizando tanto el rendimiento como la relevancia en las búsquedas posteriores.
- Experimentos realizados:
    Durante pruebas iniciales, chunks más grandes disminuían la precisión del modelo y chunks más pequeños fragmentaban demasiado el contenido.

3. Modelo de embeddings embed-multilingual-v3.0 de Cohere

- Razón de elección:
    Este modelo fue seleccionado debido a su capacidad multilingüe, esencial para procesar prospectos médicos en diferentes idiomas (importante para escalabilidad del proyecto, por más que actualmente solo procese documentos en español)
    Ofrece representaciones vectoriales de alta calidad, optimizadas para tareas como búsqueda semántica y clasificación.
- Beneficio clave:
    Su diseño lo hace ideal para dominios técnicos, garantizando que conceptos médicos complejos se representen con precisión en el espacio vectorial.


4. Base de datos Chroma como vector store persistente

- Razón de elección:
    Chroma fue seleccionada por su capacidad de almacenar embeddings de manera persistente, asegurando que los datos procesados no se pierdan tras reinicios del sistema.
    Su rendimiento en búsquedas vectoriales es óptimo para escenarios de consulta rápida y frecuente.
    Es sencilla de instalar y ejecutar, lo que permite integrarla fácilmente al flujo de trabajo de desarrollo.
  
- Beneficio clave:
    Permite manejar grandes volúmenes de datos vectoriales con búsquedas eficientes y escalabilidad.
    Inicialmente, los datos se almacenan en un directorio local en la computadora, lo que facilita la configuración en entornos de desarrollo o pruebas.
    En un futuro, podría configurarse para almacenar los datos en un servidor dedicado, lo que permitiría escalar el sistema para un mayor volumen de datos o accesos concurrentes.

5. Acceso a la base de datos y reranking de los documentos obtenidos

* Cohere Reranker (de langchain_cohere) y ContextualCompressionRetriever (de langchain.retrievers)

- Razón de elección:
    El modelo rerank-english-v2.0 de Cohere fue seleccionado como base para el reranking debido a su capacidad para realizar una clasificación precisa de documentos, asignando un puntaje de relevancia a cada uno de los resultados. Este modelo es especialmente eficaz en la optimización del ranking de documentos al filtrar los menos relevantes.

    El ContextualCompressionRetriever optimiza la búsqueda inicial realizada en el vector store, utilizando el método .as_retriever junto con el modelo de reranking rerank-english-v2.0 de Cohere. Este enfoque asegura que solo los documentos más relevantes sean retenidos, eliminando aquellos que no cumplen con un umbral mínimo de relevancia, definido como compression_threshold = 0.5 (lo que implica que los documentos con un puntaje menor a 0.5 serán descartados). Además, el parámetro search_kwargs={'k': 3} permite configurar el número de resultados iniciales a evaluar, asegurando que solo se consideren los tres documentos más relevantes en la búsqueda inicial.

- Beneficios clave:

    Optimización de la búsqueda: La utilización de este enfoque reduce el número de documentos que pasan por el proceso de análisis detallado, mejorando la velocidad y eficiencia del sistema. De este modo, se optimiza el tiempo de procesamiento al centrarse solo en los documentos más relevantes.

Flujo de funcionamiento:

base_retriever: Realiza la búsqueda inicial en el vector store utilizando el método .as_retriever().
base_compressor: Aplica el modelo de reranking de Cohere para reorganizar y asignar relevancia a los resultados obtenidos.
compression_threshold: Filtra los documentos eliminando aquellos con un puntaje de relevancia inferior a 0.5, garantizando que solo los documentos más relevantes sean considerados.

* Método invoke para la ejecución de la consulta:

- El método invoke(query_text) proporciona una interfaz directa para ejecutar una consulta con el retriever, lo que permite obtener los resultados rerankeados de manera rápida y eficiente.
- Simplicidad en la ejecución: Este método permite combinar búsqueda, reranking y filtrado en una sola llamada, eliminando la necesidad de realizar operaciones manuales por separado.
- Transparencia en los resultados: El método invoke también muestra el score de relevancia para cada documento, lo que facilita la evaluación de la calidad de los resultados y ayuda a tomar decisiones informadas.

* Uso del relevance_score para medir la confiabilidad de la respuesta:

- El relevance_score, proporcionado por el modelo de reranking, es un indicador cuantitativo que evalúa qué tan bien un documento responde a la consulta del usuario, permitiendo una medición objetiva de la relevancia.
- Transparencia en la respuesta: Este puntaje proporciona al usuario un contexto detallado sobre el origen de la información (documento, categoría, fecha de creación), lo que facilita la comprensión de la fiabilidad de la respuesta proporcionada.
- Medición objetiva: El relevance_score permite identificar fácilmente respuestas potencialmente poco confiables si el puntaje es bajo, ayudando a garantizar que solo se proporcionen respuestas basadas en documentos altamente relevantes.

6. Justificación para el uso de ChatCohere con LangChain en la generación de respuestas

1. Uso de ChatCohere
- Razón de elección:
    Se ha elegido el modelo ChatCohere por su capacidad avanzada en procesamiento de lenguaje natural, específicamente en la generación de respuestas conversacionales.
    El modelo command-r-plus-08-2024 de Cohere es ideal para tareas de generación de texto en entornos interactivos, ya que maneja de manera eficiente el contexto de la conversación previa y proporciona respuestas coherentes basadas en la consulta del usuario.
- Beneficio clave:
    Precisión en la respuesta: El modelo está optimizado para generar respuestas más contextualizadas, utilizando tanto el historial de conversación como el texto relevante extraído de la base de datos.
    Configuración flexible: La posibilidad de ajustar la temperature (en este caso 0.0) permite generar respuestas más deterministas y precisas, lo que es importante cuando se necesita una respuesta coherente y clara en el contexto médico o técnico.


2. Integración con LangChain

- Razón de elección:
    LangChain se utiliza para estructurar de manera flexible y poderosa las interacciones entre los diferentes componentes del sistema. En este caso, se ha combinado con ChatCohere para proporcionar un flujo de trabajo robusto en la generación de respuestas.
    El uso de PromptTemplate en LangChain permite crear un formato consistente para las entradas de texto que se pasan al modelo. Esto asegura que el modelo reciba siempre un contexto coherente para generar una respuesta precisa.
- Beneficio clave:
    Interoperabilidad: LangChain facilita la integración de diferentes herramientas y componentes de generación de respuestas, incluyendo el acceso a bases de datos, la gestión de estados de conversación y la estructuración de prompts complejos.
    - Manejo de contexto: LangChain permite mantener y estructurar de manera eficiente el contexto de la conversación anterior, lo que mejora la calidad de las respuestas generadas. Esto es esencial en sistemas interactivos que requieren consistencia y continuidad en las respuestas.
3. Estructura del prompt

-Razón de elección:
    El prompt diseñado dentro de PromptTemplate incluye varias piezas clave de información:
    Historial de conversación: .................
    Texto relevante: Proporciona el contexto específico relacionado con la consulta actual del usuario, extraído de la base de datos.
    Pregunta del usuario: Especifica la consulta exacta que el modelo debe abordar, lo que asegura que la respuesta esté alineada con la solicitud.
- Beneficio clave:
    Contexto completo: El uso de varias variables en el prompt ayuda a garantizar que el modelo de lenguaje genere respuestas precisas y relevantes, ya que el modelo tiene acceso tanto al contexto general (historial) como a la información específica de la consulta.
    Eficiencia: La plantilla de prompt estructurada facilita la reutilización y modificación de la lógica de generación de respuestas, mejorando la escalabilidad y mantenibilidad del código.

4. Manejo de Respuesta
- Razón de elección:
    El código maneja la respuesta generada asegurando que se capture correctamente el contenido de la respuesta y se controle adecuadamente el caso donde no se genera una respuesta.
    En caso de que no se obtenga una respuesta válida, se proporciona un mensaje predeterminado que mantiene la calidad de la experiencia del usuario.
- Beneficio clave:
    Resiliencia: La capacidad de manejar excepciones y errores garantiza que el sistema no falle ante entradas inválidas o problemas en la generación de la respuesta.
    Experiencia de usuario: Si no se genera una respuesta, se ofrece un mensaje claro que informa al usuario de manera amigable, sin interrumpir el flujo de la aplicación.
5. Uso de conversation_history
- Razón de elección:
    El uso del conversation_history para mantener un historial de interacciones anteriores es esencial para garantizar que el modelo responda de manera coherente a lo largo de la conversación.
    El parámetro MAX_HISTORY_LENGTH limita el tamaño del historial almacenado, lo que permite un balance entre contexto y rendimiento, evitando que el modelo reciba una cantidad excesiva de datos innecesarios.
- Beneficio clave:
    Coherencia en la interacción: Mantener un historial de conversación permite que el modelo responda de manera natural y fluida, recordando las preguntas anteriores del usuario y ofreciendo respuestas más personalizadas.
- Optimización de recursos: Limitar el tamaño del historial a un número fijo de interacciones evita sobrecargar al modelo con demasiada información, lo que mejora el rendimiento y reduce el costo computacional.

6. Justificación para el uso del temperature=0.0
- Razón de elección:
    Se ha elegido un valor de temperature=0.0 para el modelo, lo que implica que las respuestas generadas serán más deterministas y coherentes.
    Este valor es útil cuando se requiere que el modelo produzca respuestas precisas y controladas, especialmente en un contexto profesional y técnico.
- Beneficio clave:
    Precisión: Garantiza respuestas menos variadas y más directas, lo cual es esencial cuando se busca proporcionar información precisa y confiable, como en el contexto médico o técnico.




## Endpoints

POST/ask_question

Este endpoint permite realizar consultas a la base de datos y obtener respuestas relevantes basadas en el procesamiento de prospectos de remedios.

Descripción: El endpoint recibe una consulta (query) en formato de texto y utiliza el modelo entrenado para recuperar la información más relevante relacionada con la consulta. La información recuperada es procesada y devuelta en forma de respuesta.

Parámetros de entrada:
query (string): Una cadena de texto que contiene la pregunta o consulta que el usuario desea realizar. Este parámetro es utilizado por el modelo para realizar una búsqueda en la base de datos y generar una respuesta relevante.

Flujo:
1. El usuario envía una solicitud POST con el parámetro query al endpoint /ask_question.
2. El servidor invoca la función orquestadora, que maneja la consulta y obtiene la información relevante.
3. La función orquestadora pasa la query a la base de datos, realiza el proceso de búsqueda, recuperación, re-ranking y finalmente genera una respuesta.
4. La respuesta se devuelve al usuario en el formato { "final_response": response }.

POST /ask_question

    {
        "query": "¿Cuál es la acción farmacológica del cilostazol ?"
    }

Ejemplo de Respuesta Exitosa (status code = 200):

    {
        "response": "El cilostazol produce su efecto vasodilatador y antiagregante plaquetario a través de la inhibición específica de la enzima fosfodiesterasa tipo III de AMP cíclico (AMPc PDE tipo III). Esta inhibición disminuye la degradación del AMPc y provoca un aumento en la concentración de AMPc en el músculo liso vascular y en las plaquetas. En estudios in vitro, el cilostazol inhibe la agregación plaquetaria inducida por ADP, colágeno, ácido araquidónico o epinefrina, así como la agregación secundaria de plaquetas humanas inducida por ADP o epinefrina."
    }

## Errores

Errores comunes

1. 400 Bad Request
    - Descripción: El parámetro query no está presente o es inválido.
    - Causa: Si el parámetro query no se proporciona en la solicitud o no es una cadena de  texto válida, el servidor devuelve un error 400.
    - Solución: Asegúrate de enviar una cadena de texto válida como parámetro query.

    {
        "detail": "Query parameter is missing or invalid."
    }

2. 404 Not Found

    {
        "status": 404,
        "message": "Lo siento, no encontré información relevante en la base de datos para   responder tu consulta."
    }

3. Internal Server Error:

    - Descripción: Ocurrió un error inesperado en el servidor al procesar la solicitud.
    - Causa: Puede ser un error en la configuración de la base de datos, un problema con el modelo o un error en el código del servidor.
    - Solución: Realizar prints en diferentes flujos del código para encontrar el error.

    {
        "detail": "An unexpected error occurred. Please try again later."
    }
