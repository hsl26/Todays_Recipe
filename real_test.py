from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.memory import ConversationBufferMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
import json
from dotenv import load_dotenv
import os
import time

embedding_model=AzureOpenAIEmbeddings(
        model="text-embedding-3-large"
    )

db3 = Chroma(persist_directory=r"C:\Users\wp3wk\OneDrive\바탕 화면\국민대학교\3학년 여름방학\LLM_Project4\LLM_bootcamp-elecXsoft\test\batch_0",
             embedding_function=embedding_model)


print(db3.get())
