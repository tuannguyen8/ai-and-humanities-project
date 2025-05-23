from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
import os


os.environ["OPENAI_API_KEY"] = "your-openai-api-key"


def load_documents(directory="documents"):
    from pathlib import Path
    docs = []
    for file in Path(directory).glob("*.txt"):
        loader = TextLoader(str(file))
        docs.extend(loader.load())
    return docs


def get_rag_response(question):
    documents = load_documents()

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    llm = OpenAI(temperature=0.3)

    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    result = qa.run(question)

    return result
