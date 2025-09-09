from rag.config.path import PDF_PATH
import os
from dotenv import load_dotenv

from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_upstage import UpstageEmbeddings, ChatUpstage
from langchain.chains import RetrievalQA

def init_rag():
    # 청킹
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
    )

    loader = UnstructuredPDFLoader(PDF_PATH)
    document_list = loader.load_and_split(text_splitter=text_splitter)

    embedding = UpstageEmbeddings(model="solar-embedding-1-large")

    index_name = 'm14'
    database = PineconeVectorStore.from_documents(
        documents=document_list,
        embedding=embedding,
        index_name=index_name
    )

    retriever = database.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    llm = ChatUpstage(temperature=0.0)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain

def ask_question(qa_chain, message: str):
    result = qa_chain({"query": message})
    return {
        "answer": result["result"],
        "sources": [
            {"source": doc.metadata.get("source"), "content": doc.page_content[:200]}
            for doc in result["source_documents"]
        ]
    }
