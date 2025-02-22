# JSON-RAG-zfrqbl

# Linux Command Assistant

This repository contains a Python-based Retrieval Augmented Generation (RAG) application that uses Gemini for natural language understanding and LangChain for querying a structured JSON database of Linux commands. Users can ask questions about Linux commands and receive concise, informative responses with practical examples. The application includes features like context summarization for improved performance.

Key technologies used:

*   Gemini (Google)
*   LangChain
*   FAISS
*   Sentence Transformers
*   Python

## Table of Contents

*   [Project Description](#project-description)
*   [Code Walkthrough](#code-walkthrough)
*   [How to Run the Project](#how-to-run-the-project)
*   [Caution](#caution)

## Project Description

This application aims to provide a quick and easy way to access information about Linux commands.  It uses a RAG approach, meaning it retrieves relevant information from a knowledge base (the `commands.json` file) and then uses Gemini to generate a natural language response. This approach allows the application to provide accurate and contextually appropriate answers to user queries.

The quality of responses are dependent on most part on the contents of the commands.json file. While I have provided a sample commands.json file, I recommned reviewing the file and adding/improving the information about commands' switches and variations. You can also add more commands or improve the description for better response. 

*Important*: Use the validate_json.py script to validate the JSON file after you make any changes to the JSON file.

## Code Walkthrough

The code is organized into several key sections:

1.  **Imports and Setup:**  This section imports necessary libraries (like `langchain`, `sentence_transformers`, etc.), sets up logging, and loads the Gemini API key from a `.env` file.  Error handling is included to ensure the API key is loaded correctly.

2.  **Data Loading and Document Creation:** The `commands.json` file, containing information about Linux commands, is loaded. Each command is then converted into a LangChain `Document` object, which includes the command's content (command, summary, description, options, examples) and metadata (the command name).

3.  **FAISS Index Creation:**  Sentence Transformers are used to create embeddings for each command document.  These embeddings are then used to build a FAISS index, which enables efficient similarity searches.  FAISS is a powerful library for fast and scalable search of dense vectors.

4.  **LLM and Prompt Template:**  The Gemini LLM is initialized with the API key. A prompt template is created to guide the LLM's behavior. The prompt instructs the LLM to act as a Linux command assistant, format the output for readability, and prioritize relevant information.  It also includes example queries and responses to demonstrate the desired output format.

5.  **`summarize_context` Function:** This function is responsible for summarizing long contexts using the LLM. It's crucial for managing the LLM's context window. It takes the context and the LLM as input, and returns a summarized version of the context. Error handling is included to gracefully handle any issues during summarization.

6.  **`query_commands` Function:** This is the core function of the application. It takes a user query as input, performs a similarity search against the FAISS index to retrieve relevant documents (commands), constructs the context string, and then calls the LLM using the prompt template. The context is summarized if it exceeds a threshold. The function returns the LLM's response.  Rate limiting (using `time.sleep()`) is implemented in the `finally` block, although this will be replaced with a dynamic approach later.

7.  **Command-Line Interface:**  The `while True` loop creates a simple command-line interface.  The user can enter queries, and the application will display the LLM's responses. Typing "exit" will terminate the application.

**Logic Highlights:**

*   **Retrieval:** The `db.similarity_search(query)` function uses the FAISS index to efficiently retrieve the most relevant commands based on the user's query.

*   **Context Management:**  The `summarize_context` function and the context length threshold help manage the LLM's context window.

*   **Prompt Engineering:** The detailed prompt template is crucial for guiding the LLM to provide accurate and well-formatted responses.

*   **Caching:**  An in-memory cache using a dictionary is implemented to store responses for frequently asked questions. This significantly improves performance.

## How to Run the Project

1.  **Clone the repository:** `git clone https://github.com/your-username/your-repo-name.git`
2.  **Navigate to the directory:** `cd your-repo-name`
3.  **Create a virtual environment (recommended):** `python3 -m venv venv` (or `python -m venv venv` on Windows). Activate it using `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows).
4.  **Install the dependencies:** `pip install -r requirements.txt` (Create a `requirements.txt` file with all the project dependencies).
5.  **Create a `.env` file:** In the project directory, create a file named `.env` and add your Gemini API key:

    ```
    GOOGLE_API_KEY=your_actual_api_key
    ```

6.  **Create `commands.json`:**  Create a file named `commands.json` in the same directory. This file should contain the data about Linux commands in JSON format.  See the provided `commands.json` example for the required structure.
7.  **Run the application:** `python3 your_script_name.py` (replace `your_script_name.py` with the name of your Python script).

## Caution

*   **API Key Security:**  Do not commit your `.env` file to version control. It contains your API key, which is sensitive information.  The `.gitignore` file should include `.env` to prevent it from being committed.
*   **Rate Limiting:**  The current rate limiting implementation using `time.sleep()` is static.  A dynamic rate limiting mechanism using response headers will be implemented in a future update.  Be mindful of Gemini API rate limits.
*   **Context Window:**  The LLM has a limited context window.  Very long contexts might be truncated or summarized, which could affect the quality of the responses.
*   **Data Accuracy:**  The accuracy of the responses depends on the data in the `commands.json` file.  Ensure that the data is accurate and up-to-date.

