# Conversational RAG with PDF Uploads and Chat History

This repository contains a **Streamlit-based application** that allows users to upload PDF files, ask questions about their content, and maintain a conversational chat history. The application uses **LangChain**, **ChromaDB**, and **Groq API** to implement a **Retrieval-Augmented Generation (RAG)** system.

---

## **Features**

- **PDF Upload**: Upload one or more PDF files to extract and analyze their content.
- **Conversational Q&A**: Ask questions about the uploaded PDFs and get concise answers.
- **Chat History**: Maintains a session-based chat history for a seamless conversational experience.
- **RAG Pipeline**: Uses LangChain's RAG pipeline to retrieve relevant information from the PDFs and generate answers using the Groq API.
- **Session Management**: Supports multiple sessions with unique session IDs.

---

## **Technologies Used**

- **Streamlit**: For building the web interface.
- **LangChain**: For creating the RAG pipeline and managing chat history.
- **ChromaDB**: For vector storage and retrieval of document embeddings.
- **Groq API**: For generating responses using the `Gemma2-9b-It` model.
- **Hugging Face Embeddings**: For generating document embeddings using the `all-MiniLM-L6-v2` model.
- **PyPDF**: For loading and processing PDF files.

---

## **Setup Instructions**

### **1. Prerequisites**

- Python 3.8 or higher.
- A **Groq API key** (sign up at [Groq](https://groq.com/)).
- A **Hugging Face token** (optional, for using custom embeddings).

### **2. Clone the Repository**

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
