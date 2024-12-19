# Documentación de API

# BACKEND
## Tabla de Contenidos
1. [Descripción de Backend](#descripción)
2. [Requisitos](#requisitos)
3. [Instalación y Configuración](#instalación-y-configuración)
4. [Herramientas utilizadas](#Herramientas-utilizadas)
5. [EndPoints](#endpoints)
   1. [POST /ask_question](#post-users)
6. [Errores](#errores)
7. [Ejemplos de Uso](#ejemplos-de-uso)
8. [Licencia](#licencia)

# FRONTEND
1. [Descripción de Frontend](#descripción)
2. [Requisitos](#requisitos)
3. [Instalación y Configuración](#instalación-y-configuración)
4. [Herramientas utilizadas](#Herramientas-utilizadas)
5. [Ejemplos de Uso](#ejemplos-de-uso)


## Descripción de Backend

Esta API está desarrollada en Python utilizando Flask como framework y basada en arquitectura RAG (Retrieval-Augmented Generation), busca resolver el problema de la subutilización de la información contenida en los prospectos de medicamentos, ya que a pesar de ser una fuente de máximo valor, se encuentra desperdiciada, tanto en su formato físico (generando impactos medioambientales), cómo en su presentación dígital existente siendo la lectura de los mismos tediosa y dificil de comprender en muchas ocaciones.
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

    Crear un directorio local para almacenamiento de la información
    Asignar un nombre a la colección.

6.  Ejecución única de funciones para la creación de embeddings y almacenamiento en la base de datos vectorial
    La ejecución de estas funciones se realiza mediante la función process_file(file_path), ubicada en la carpeta 'utils'. Esta función toma como parámetro la ruta (file_path) de los archivos a procesar (ubicados en la carpeta outout) y ejecuta los siguientes funciones:
     - Creación de chunks: Divide el contenido del archivo en fragmentos manejables.
     - Generación de embeddings: Crea representaciones vectoriales de los fragmentos.
     - Almacenamiento en Chroma: Guarda los embeddings generados en la base de datos vectorial.

         Ejemplo de ejecución:
         Se declara la variable 'file_path' y se le asigna la ruta del archivo de interes ubicado en la carpeta 'output'
            file_path = './output/CARDILIPEN-Bisoprolol fumarato.txt'

        Ejecución de la función:
            process_file(file_path)

        Mensaje de salida
        "Documents added to Chroma with IDs: {ids} and embeddings: {len(embeddings)} embedding info {embeddings[0]}"

7. Una vez que ya está todo instalado y los embeddings creados se puede proceder a interactuar con la API a través de herramientas como POSTMAN. (ver [EndPoints](#endpoints))


## Herramientas utilizadas

Este proyecto se desarrolló con una seria de herramientas y configuraciones para garantizar la eficiencia y escalabilidad. A continuación, se detallan las decisiones clave:

1. pdfplumber para la extracción de texto

    - Razón de elección: pdfplumber fue seleccionado por su capacidad robusta para manejar documentos PDF complejos, permitiendo extraer texto incluso de estructuras avanzadas como tablas, encabezados y pies de página.
    - Beneficio clave: La herramienta sobresale en el procesamiento de PDFs que contienen múltiples formatos de texto y diseño, lo que garantiza que el contenido del prospecto médico se extraiga con precisión sin pérdida de información relevante.

2. LangChain Recursive Text Splitter

- Razón de elección:
    Herramienta para generación de chunks.
    El tamaño del chunk elegido fue de 2000 caracteres ya que de ésta manera garantiza un balance entre la retención del contexto y la capacidad del modelo de embeddings para procesar cada fragmento.
    El solapamiento elegido fue de 200 caracteres, ésto asegura que no se pierda información clave del documento, especialmente en textos donde cada palabra es sumamente importante.

- Beneficio clave:
    Esta técnica permite dividir el texto en fragmentos procesables sin sacrificar la coherencia contextual, optimizando tanto el rendimiento como la relevancia en las búsquedas posteriores.
- Experimentos realizados:
    Durante pruebas iniciales chunks más pequeños fragmentaban demasiado el contenido.

3. Modelo de embeddings embed-multilingual-v3.0 de Cohere

- Razón de elección:
    Este modelo fue seleccionado debido a su capacidad multilingüe, esencial para procesar prospectos médicos en diferentes idiomas (importante para escalabilidad del proyecto, por más que actualmente procese documentos en español)
    Ofrece representaciones vectoriales de alta calidad, optimizadas para tareas como búsqueda semántica y clasificación.
- Beneficio clave:
    Su diseño lo hace ideal para dominios técnicos, garantizando que conceptos médicos complejos se representen con precisión en el espacio vectorial.


4. Base de datos Chroma como vector store persistente

- Razón de elección:
    Chroma fue seleccionada por su capacidad de almacenar embeddings de manera persistente, asegurando que los datos procesados no se pierdan tras reinicios del sistema.
    Su rendimiento en búsquedas vectoriales es óptimo para escenarios de consulta rápida y frecuente.
    Es sencilla de instalar y ejecutar, lo que permite integrarla fácilmente al flujo de trabajo de desarrollo.

- Beneficio clave:
    Permite manejar grandes volúmenes de datos vectoriales con búsquedas eficientes.
    Inicialmente, los datos se almacenan en un directorio local, lo que facilita la configuración en entornos de desarrollo o pruebas.
    En un futuro, podría configurarse para almacenar los datos en un servidor dedicado, lo que permitiría escalar el sistema para un mayor volumen de datos o accesos concurrentes.

5. Acceso a la base de datos y reranking de los documentos obtenidos

* Cohere Reranker (de langchain_cohere) y ContextualCompressionRetriever (de langchain.retrievers)

- Razón de elección:
    El modelo rerank-english-v2.0 de Cohere fue seleccionado como base para el reranking debido a su capacidad para realizar una clasificación precisa de documentos, asignando un puntaje de relevancia a cada uno de los resultados. Este modelo es especialmente eficaz en la optimización del ranking de documentos al filtrar los menos relevantes.

    El ContextualCompressionRetriever optimiza la búsqueda inicial realizada en el vector store, utilizando el método '.as_retriever' junto con el modelo de reranking 'rerank-english-v2.0' de Cohere. Este enfoque asegura que solo los documentos más relevantes sean retenidos, eliminando aquellos que no cumplen con un umbral mínimo de relevancia, definido como compression_threshold = 0.5 (lo que implica que los documentos con un puntaje menor a 0.5 serán descartados). Además, el parámetro search_kwargs={'k': 3} permite configurar el número de resultados iniciales a evaluar, asegurando que solo se consideren los tres documentos más relevantes en la búsqueda inicial.

- Beneficios clave:

    Optimización de la búsqueda: La utilización de este enfoque reduce el número de documentos que pasan por el proceso de análisis detallado, mejorando la velocidad y eficiencia del sistema. De este modo, se optimiza el tiempo de procesamiento al centrarse solo en los documentos más relevantes.

- Flujo de funcionamiento:

      - base_retriever: Realiza la búsqueda inicial en el vector store utilizando el método .as_retriever().
      - base_compressor: Aplica el modelo de reranking de Cohere configurado para reorganizar y asignar relevancia a los resultados obtenidos.
      - compression_threshold: Filtra los documentos eliminando aquellos con un puntaje de relevancia inferior a 0.5, garantizando que solo los documentos más relevantes sean considerados.

* Método invoke para la ejecución de la consulta:

   El método invoke(query_text) proporciona una interfaz directa para ejecutar una consulta (query:str) con el retriever, lo que permite obtener los resultados rerankeados de manera rápida y eficiente.
   Simplicidad en la ejecución: Este método permite combinar búsqueda, reranking y filtrado en una sola llamada, eliminando la necesidad de realizar operaciones manuales por separado (por ejemplo, no es necesario realizar el embedding de la query ya que se ejecute por detras del método invoke)
   Transparencia en los resultados: El método invoke también muestra el score de relevancia para cada documento, lo que facilita la evaluación de la calidad de los resultados y ayuda a tomar decisiones informadas.

* Uso del relevance_score para medir la confiabilidad de la respuesta:

  El relevance_score, proporcionado por el modelo de reranking, es un indicador cuantitativo que evalúa qué tan bien un documento responde a la consulta del usuario, permitiendo una medición objetiva de la relevancia.

6. Justificación para el uso de Generación de Respuestas con Cohere y Langchain

1. Uso de ChatCohere
- Razón de elección:
    Se ha optado por el modelo ChatCohere debido a su capacidad avanzada de procesamiento de lenguaje natural, especialmente en tareas de generación de respuestas conversacionales. El modelo command-r-plus-08-2024 de Cohere es ideal para generar respuestas coherentes y relevantes en entornos interactivos, proporcionando respuestas precisas basadas en la consulta del usuario.
- Beneficio clave:
    Precisión en la respuesta: El modelo está optimizado para generar respuestas altamente contextualizadas, utilizando texto relevante extraído de la base de datos.
    Configuración flexible: Ajustar parámetros como temperature=0.0 permite que el modelo adopte una actitud más determinista y genere respuestas precisas y coherentes en cada interacción.

2. Integración con LangChain

- Razón de elección:
    La biblioteca Langchain proporciona una forma intuitiva de organizar las interacciones con los modelos de lenguaje, facilitando la creación de prompts y el manejo de las respuestas. Al utilizar HumanMessage, se establece un contexto conversacional claro para el modelo.

- Beneficio clave:
    Interoperabilidad: LangChain facilita la integración de diferentes herramientas y componentes de generación de respuestas.
    Estructuración eficiente de prompts: LangChain permite agregar múltiples mensajes al prompt, lo que es útil para proporcionar información adicional o modificar el comportamiento del modelo.

3. Estructura del prompt

El prompt se compone de tres partes principales: un preámbulo que establece las instrucciones generales de comportamiento para el modelo, la consulta del usuario y el contenido relevante obtenido de la base de datos. Esta estructura garantiza que el modelo tenga acceso a toda la información necesaria para generar respuestas precisas y contextualizadas.

-Razón de elección:
     Esta estructura permite que el modelo comprenda tanto el contexto general del tema (a través del preámbulo y el contenido relevante) como la pregunta específica del usuario.
- Beneficio clave:
    Contexto completo: Al incluir el preámbulo, la consulta del usuario y el contenido relevante en el prompt, se proporciona al modelo un contexto rico y completo, lo que mejora la calidad de las respuestas.
    Eficiencia: La estructura clara y concisa del prompt optimiza el proceso de generación de respuestas, reduciendo el tiempo de procesamiento y mejorando la eficiencia.

4. Manejo de Respuesta
- Razón de elección:
    El código maneja las respuestas generadas asegurándose de capturar correctamente el contenido y controlando los casos en los que no se obtiene una respuesta válida.
- Beneficio clave:
    Resiliencia: La capacidad de manejar excepciones y errores garantiza que el sistema no falle ante entradas inválidas o problemas en la generación de la respuesta.
    Experiencia de usuario: Si no se genera una respuesta, se ofrece un mensaje claro que informa al usuario de manera amigable, sin interrumpir el flujo de la aplicación.

6. Justificación para el uso del temperature=0.0
- Razón de elección:
    Se ha elegido un valor de temperature=0.0 para el modelo, lo que implica que las respuestas generadas serán más deterministas, precisas y coherentes.
    Este valor es útil cuando se requiere que el modelo produzca respuestas precisas y controladas, especialmente en un contexto profesional y técnico.
- Beneficio clave:
    Precisión: Garantiza respuestas menos variadas y más directas, lo cual es esencial cuando se busca proporcionar información precisa y confiable.


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


## Ejemplos de uso
A continuación se detallan algunos de las pruebas realizadas, las mismas fueron realizadas a través de la interfaz gráfica realizada con REACT.Js-
----------------------------------------------------------------------------------
### Ejemplo de prueba 1

- Consulta del usuario:
        ¿Qué es el medicamento Aclusin?

- Respuesta:
        El medicamento Aclusin es un fármaco que contiene el principio activo cilostazol. Está indicado para el tratamiento de los síntomas isquémicos de los miembros, como úlceras, dolor, claudicación intermitente y sensación de frío, causados por la enfermedad arterial oclusiva crónica.
        Su mecanismo de acción se basa en la inhibición de la enzima fosfodiesterasa tipo III de AMP cíclico (AMPc PDE tipo III), lo que resulta en una mayor concentración de AMPc en el músculo liso vascular y en las plaquetas, produciendo un efecto vasodilatador y antiagregante plaquetario.

- Metadata de la respuesta:
El documento más relevante se obtuvo del archivo'ACLUSIL-Cilostazol', perteneciente a la categoria de farmacos de Medicamentos Cardiovasculares  cargado el 2024-12-18, con una puntuación de relevancia de 0.98.
---------------------------------------------------------------------------------
### Ejemplo de prueba 2

- Consulta del usuario:
        ¿Cuál es la fórmula del medicamento ALBICAR L-CARNITINA?

- Respuesta:
        La fórmula del medicamento Albicar L-Carnitina varía según la presentación:
    * Fórmula inyectable (IM y EV):
        - Cada ampolla contiene L-Carnitina 1,000 g.
        - Excipientes: Ácido Clorhídrico 10% 0,014 ml, agua destilada estéril y apirógena c.s.p. 5 ml solución.
    * Fórmula oral:
        - Cada ampolla contiene L-Carnitina 1,0000 g.
        - Excipientes: Ciclamato de sodio 0,0030 g, Ácido Clorhídrico c.s., Sorbato de potasio 0,0100 g, Cetrimida 0,0005 g, Alcohol 0,1500 ml, Aroma naranjas 0,0585 g, Sacarina sódica 0,0040 g, Agua purificada c.s.p. 10,0000 ml.

- Metadata de la respuesta:
El documento más relevante se obtuvo del archivo'ALBICAR-Lcarnitina', perteneciente a la categoria de farmacos de Medicamentos Cardiovasculares  cargado el 2024-12-18, con una puntuación de relevancia de 1.00.
-----------------------------------------------------------------------------------
### Ejemplo de prueba 3

- Consulta del usuario:
       ¿A qué se conoce como deficiencia de levocarnitina?

- Respuesta:
        La deficiencia de levocarnitina se define bioquímicamente como niveles anormalmente bajos de carnitina plasmática libre (menos de 20 μmol/l a la semana post término) y puede estar asociada con bajos niveles tisulares o urinarios. Esta condición puede asociarse con una relación éster/levocarnitina libre plasmática mayor de 0,4 o niveles normalmente elevados de levocarnitina esterificada en la orina. En niños prematuros y recién nacidos, la deficiencia secundaria se define como niveles de levocarnitina plasmática libre por debajo de los niveles normales que corresponden a la edad.

- Metadata de la respuesta:
El documento más relevante se obtuvo del archivo'ALBICAR-Lcarnitina', perteneciente a la categoria de farmacos de Medicamentos Cardiovasculares  cargado el 2024-12-18, con una puntuación de relevancia de 1.00.
-----------------------------------------------------------------------------------
### Ejemplo de prueba 4

- Consulta del usuario:
       ¿Que es el Bemplas clorhidrato de clonidina?

- Respuesta:
        El Bemplas clorhidrato de clonidina es un medicamento antihipertensivo y diurético. Está autorizado por el Ministerio de Salud y su venta es bajo receta.
        Su fórmula contiene los siguientes componentes:
            - Clonidina clorhidrato 0,075 mg
            - Clortalidona 50,000 mg
            - Excipientes: almidón de maíz 20,000 mg, lactosa 126,895 mg, croscarmelosa sódica 1,000 mg, estearato de magnesio 2,000 mg, azul patente 0,030 mg.
        La acción terapéutica se basa en la combinación de la clonidina, que estimula receptores alfa adrenérgicos centrales reduciendo el tono simpático central y la resistencia periférica, y la clortalidona, que actúa como diurético inhibiendo la reabsorción distal de sodio a nivel nefronal.

- Metadata de la respuesta:
El documento más relevante se obtuvo del archivo'BEMPLAS- Clorhidrato de Clonidina clortalidon', perteneciente a la categoria de farmacos de Medicamentos Cardiovasculares  cargado el 2024-12-18, con una puntuación de relevancia de 1.00.
-----------------------------------------------------------------------------------
### Ejemplo de prueba 5

- Consulta del usuario:
        ¿Como se describe el uso de bemplas en pediatría y geriatría?

- Respuesta:
        - Uso en pediatría: La seguridad y eficacia de la clortalidona y la clonidina no han sido establecidas en menores de 12 años.
        - Uso en geriatría: La eliminación de la clortalidona es menor en pacientes ancianos en comparación con adultos jóvenes sanos. Por lo tanto, se recomienda un cuidadoso seguimiento clínico e incluso una reducción de la dosis en algunos casos en que se trate a pacientes ancianos.

- Metadata de la respuesta:
El documento más relevante se obtuvo del archivo'BEMPLAS- Clorhidrato de Clonidina clortalidon', perteneciente a la categoria de farmacos de Medicamentos Cardiovasculares  cargado el 2024-12-18, con una puntuación de relevancia de 0.69.
-----------------------------------------------------------------------------------
### Ejemplo de prueba 6

- Consulta del usuaio:
        ¿Que es el Cardilipen bisoprolol fumarato?

- Respuesta:
        El Cardilipen bisoprolol fumarato es un medicamento autorizado por el Ministerio de Salud y su venta es bajo receta. Es un betabloqueante selectivo utilizado para el tratamiento de la hipertensión arterial, la prevención de las crisis de angina de pecho y el tratamiento de la insuficiencia cardíaca crónica estable moderada a severa. Su fórmula contiene bisoprolol fumarato en diferentes concentraciones (2,5 mg, 5 mg y 10 mg) y excipientes como celulosa microcristalina, almidón pregelatinizado, hidroxipropilcelulosa, dióxido de silicio coloidal, crospovidona, estearato de magnesio, hidroxipropilmetilcelulosa, polietilenglicol 6000, dióxido de titanio, talco y povidona K30.

- Metadata de la respuesta:
        El documento más relevante se obtuvo del archivo'CARDILIPEN-Bisoprolol fumarato', perteneciente a la categoria de farmacos de Medicamentos Cardiovasculares  cargado el 2024-12-18, con una puntuación de relevancia de 1.00

-----------------------------------------------------------------------------------
### Ejemplo de prueba 7

- Consulta del usuario:
        ¿Qué es el AMPLIAR® 40 ATORVASTATIN?

- Respuesta:
        El AMPLIAR® 40 ATORVASTATIN es un medicamento autorizado por el Ministerio de Salud y su venta es bajo receta. Está indicado como tratamiento adyuvante para reducir los niveles elevados de colesterol total, LDL-colesterol, apolipoproteína B y triglicéridos en pacientes con hipercolesterolemia primaria y dislipemia mixta.
        Su fórmula contiene atorvastatina cálcica (equivalente a 40 mg de atorvastatina) y excipientes como lactosa, celulosa microcristalina, carboximetilcelulosa cálcica, povidona K30, crospovidona, dióxido de silicio coloidal, estearato de magnesio, dióxido de titanio, hidroxipropilmetilcelulosa, talco y polietilenglicol 6000.
        La acción terapéutica de este medicamento es hipocolesterolemiante, ya que la atorvastatina actúa reduciendo los niveles de lípidos en la sangre al inhibir la enzima HMG-CoA reductasa, la cual es clave en la biosíntesis de colesterol.

- Metadata de la respuesta:
        El documento más relevante se obtuvo del archivo'AMPLIAR40-Atorvastatina', perteneciente a la categoria de farmacos de Medicamentos Cardiovasculares  cargado el 2024-12-18, con una puntuación de relevancia de 1.00.
-----------------------------------------------------------------------------------
### Ejemplo de prueba 8

- Consulta del usuario:
        Describe la posología y modos de administración de Ampliar duo

- Respuesta:
        La posología y modo de administración de Ampliar duo es la siguiente:
            - La dosis inicial recomendada es de 10 mg de atorvastatina y 10 mg de ezetimibe una vez al día.
            - El medicamento debe ser administrado en una sola toma diaria, en cualquier momento del día, antes o después de la comida.
            - El comprimido de atorvastatina (identificado con la letra A) y el de ezetimibe (identificado con la letra E) deben ingerirse en la misma toma.
            - El tratamiento debe adecuarse a la respuesta individual y al objetivo terapéutico.
            - Después de iniciar el tratamiento y durante la titulación de la dosis, los niveles plasmáticos de lípidos deben controlarse cada 2 a 4 semanas para realizar el ajuste de dosis.
            - El objetivo es reducir los niveles de LDL, por lo que se recomienda utilizar la concentración de LDL como dato previo al inicio del tratamiento y como valor de control de la respuesta terapéutica.
            - En pacientes sin respuesta adecuada a la dosis de 20 mg diarios de atorvastatina, se debe iniciar el tratamiento directamente con Ampliar duo 20/10.
            - En pacientes con respuesta inadecuada a 10 mg diarios de ezetimibe como monoterapia, el tratamiento debe iniciarse con Ampliar duo 10/10.
        En el caso de la hipercolesterolemia familiar homocigota, Ampliar duo se utiliza como tratamiento adjunto a otros para disminuir la concentración plasmática de lípidos o cuando estos no puedan utilizarse o no estén disponibles.

- Metadata de la respuesta:
        El documento más relevante se obtuvo del archivo'AMPLIARDUO-Atorvastatin ezetimibe', perteneciente a la categoria de farmacos de Medicamentos Cardiovasculares  cargado el 2024-12-18, con una puntuación de relevancia de 1.00.

-----------------------------------------------------------------------------------

# FRONTEND
## Descripción de Frontend

El frontend de la aplicación ha sido desarrollado utilizando React.js y se encuentra en un servidor diferente que interactúa con la API proporcionada en el backend. Esta separación permite una arquitectura más escalable y modular.
Este servidor frontend se comunica con la API del backend para generar respuestas y proporcionar funcionalidades interactivas al usuario.


## Requisitos
 - Node.js (recomendado: versión 16 o superior): puedes verificar si tienes instalado Node.js   desde tu terminal con el siguiente comando:

    node -v

 - Clona el repositorio del frontend: Clona el repositorio del frontend usando Git. Abre una terminal y ejecuta el siguiente comando:

    git clone <URL_DEL_REPOSITORIO>


 - Navegar al directorio del proyecto:

    Una vez clonado el repositorio, navega dentro del directorio del proyecto:

    cd <https://github.com/LuzTappero/MEDICABOT-Frontend.git>

    - Instalar las dependencias: Instala las dependencias necesarias para el proyecto ejecutando el siguiente comando:

        npm install


    - Ejecutar el servidor de desarrollo: Para iniciar el servidor de desarrollo, ejecuta el siguiente comando:

        npm run dev

    Este comando ejecutará Vite, el servidor de desarrollo configurado en el proyecto, y podrás acceder a la aplicación en tu navegador.

Acceso a la aplicación:
Cuando el servidor se haya iniciado correctamente, verás un mensaje similar al siguiente en la terminal:

    VITE v6.0.3  ready in 1300 ms

    ➜  Local:   http://localhost:5173/
    ➜  press h + enter to show help


