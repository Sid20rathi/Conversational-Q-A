import streamlit as st
import os
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.runnables.history import RunnableWithMessageHistory


from dotenv import load_dotenv
load_dotenv()

st.title("Conversational Q&A")

os.environ["HUGGING_FACE"] = os.getenv("HUGGING_FACE")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

st.write("upload pdf and chat with their content")
api_key = st.text_input("Enter your  Groq Api key:",type="password")

if api_key:
    llm=ChatGroq(api_key=api_key,model_name="Gemma2-9b-It")

    session_id = st.text_input("Session ID",value ="default_session")
    if 'store' not in st.session_state:
        st.session_state.store = {}

    uploaded_files = st.file_uploader("choose A pdf file ",type="pdf",accept_multiple_files=False)
    if uploaded_files is not None:
        documents=[]
        for uploaded_file in uploaded_files:
            temppdf = f"./temp.pdf"
            with open(temppdf,"wb") as file:
                file.write(uploaded_file)

               

            loader = PyPDFLoader(temppdf)
            docs = loader.load()
            documents.extend(docs)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size= 5000,chunk_overlap=500)
        splits = text_splitter.split_documents(documents)
        vectorstore = Chroma.from_documents(documents=splits,embedding = embeddings)
        retriever = vectorstore.as_retriever()

        contextulize_q_system_prompt=(
            "Given a chat history and the last user question"
            "which might reference context in the chat history"
            "formulate a standalone question which can be understood"
            "without the chat history .Do not answer the question"
            "just reformulate it if needed and otherwise return it as it"
        )    

        contextulize_q_prompt=ChatPromptTemplate.from_messages(
            [
                ("system",contextulize_q_system_prompt),
                MessagesPlaceholder("chat history"),
                ("human","{input}"),

            ]
        ) 

        history_aware_retriever = create_history_aware_retriever(llm,retriever,contextulize_q_prompt,session_id)

        system_prompt = (
            "you are an assistant for question answering tasks"
            "Use the following pieces of retrieved context to answer"
            "the question. if you dont know the answer , say that you "
            "dont know .use three sentences maximum and keep the "
            "answer concise"
            "\n\n"
            "{context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system",system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human","{input}")

            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm,qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever,question_answer_chain)

        def get_session_history(session:str)->BaseChatMessageHistory:
            if session_id not in st.session_state.store:
                st.session_state.store[session_id]=ChatMessageHistory()
            return st.session_state.store[session_id]
        
        conversatonal_rag_chain = RunnableWithMessageHistory(
            
            rag_chain,get_session_history,
            input_messages_key="input",
            history_messages_key = "chat_history",
            output_messages_key = "answer"

        )
        user_input = st.text_input("your Question:")
        if user_input:
            session_history= get_session_history(session_id)
            response = conversatonal_rag_chain.invoke({
                "input":user_input
            },config={
                "configurable":{"session_id":session_id}
            },)

            st.write(st.session_state.store)
            st.write("Assistant",response['answer'])
            st.write("chat History",session_history.messages)
else:
    st.warning("Please enter your groq api key")

        













