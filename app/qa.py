import os
import time

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_groq import ChatGroq

from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.environ["GROQ_API_KEY"]

def load_text_data(directory):

    texts = []
    
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
                texts.append(f.read())
    return texts


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

for i in range(3):
    raw_texts = load_text_data(f"./data/level_{str(i)}")

    texts = text_splitter.create_documents(raw_texts)
    
embedding = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en-v1.5",
                                     model_kwargs={"device":"cpu"},
                                     encode_kwargs={"normalize_embeddings":True},
                                     )

vectorstore = FAISS.from_documents(texts, embedding)

retriever=vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":3})


llm=ChatGroq(groq_api_key=groq_api_key,
model_name="mixtral-8x7b-32768")

template = """
You are helpful chat assistant. 
You will be provided with the texts scrapped from the website. 
User will ask questions about the website and to know information about the company.

You have to answer the question based on the provided context only.
Please provide the most accurate response based on the question.

If you don't know the answer, reply with "I don't know the answer."

<context>
{context}
<\context>

Question: {input}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)
document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

prompt = input("Enter your question here:  ")

if prompt:
    
    start = time.process_time()
    response = retrieval_chain.invoke({"input":prompt})
    print("Response time :",time.process_time()-start)
    print(response['answer'])