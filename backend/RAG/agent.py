
print("--------------------------------------------------------------------------")
print("TESING  MY - Agent Application!!!")
print("--------------------------------------------------------------------------")

from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain_chroma import Chroma
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain import hub
from langchain_community.document_loaders import UnstructuredHTMLLoader, DirectoryLoader
from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold, GoogleGenerativeAIEmbeddings
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import AgentExecutor, create_json_chat_agent
#from langchain_community.tools.python.tool import PythonREPLTool
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

"""Added API Keys in the bashrc env File  """
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest",temperature=0, safety_settings = { HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, },  api_key=google_api_key)

"""a vector database where a set of documents in a variety of formats, 
generates vector embeddings for them, and then inserts them into """
vectorstore = Chroma(
    embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query"),
    persist_directory="./local_data/.chromadb"
)
"""RAG Application Document Loader similar to HW1"""
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")
def load_docs(docs):
    """Load documents and add them to the vector store."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=10)
    splits = text_splitter.split_documents(docs)
    vectorstore.add_documents(documents=splits)

def load_html(directory):
    """Load HTML files from a directory."""
    load_docs(DirectoryLoader(directory, glob="**/*.html", loader_cls=UnstructuredHTMLLoader).load())

html_directory = "local_data/html"
print(f"Loading HTML files from: {html_directory}")
load_html(html_directory)
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
"""
RAG chain that performs the document querying. 
It pulls the related document chunks from the retriever and concatenates them together, 
setting the context key with the result. 
"""
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
"""Instruction and Prompt of the LLM"""
instructions = """I am Agent written By Sanad will Answer Questions using APIs"""
base_prompt = hub.pull("langchain-ai/react-agent-template")
prompt = base_prompt.partial(instructions=instructions)

"""All the Tools that are available to thi LLM
request_all is the new one that i added"""
#tools = load_tools([ "requests_all", "llm-math","wikipedia","terminal"], llm=llm, allow_dangerous_tools=True)
tools = load_tools(["requests_all", "llm-math", "wikipedia"], llm=llm, allow_dangerous_tools=True)


""" Creating Reach Agent using list of Tools Promt and LLM of our Choice"""
agent = create_json_chat_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

"""Prompt of the LLM where users can Type their Questions"""
print(f"Welcome to my application.  I am configured with these tools")
for tool in tools:
  print(f'  Tool: {tool.name} = {tool.description}')

while True:
        line = input("llm>> ")
        """Invoke RAG chain App in input Starts with htmlQ:"""
      #  if line.startswith("htmlQ:"):
        result = rag_chain.invoke(line)
        print(result)
  
        """Invoke Lang Chain Agent if Input Does not start with htmlQ:"""
        # elif line: 
        #     result = agent_executor.invoke({"input":line})
        #     print(result)
      
       # else:
        #    break