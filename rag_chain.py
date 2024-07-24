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

# chain에 query 질의하는 함수.
def ask_something(chain, query): #

    print(f"User : {query}")

    chain_output = chain.invoke(
        {"input": query}
    )

    print(f"LLM : {chain_output}")
    
    return chain_output


# retriver 설정하는 함수.
def init_retriver():

    embedding_model=AzureOpenAIEmbeddings(
        model="text-embedding-3-large"
    )

    vector_store = Chroma(
                collection_name="vector_store",     # 저장한 컬렉션 이름
                embedding_function=embedding_model, # 임베딩 모델
                persist_directory= "vector_store"    # 저장한 디렉토리 경로(에서 불러온다)
    )

    # similarity_retriever = vector_store.as_retriever(search_type="similarity")
    mmr_retriever = vector_store.as_retriever(search_type="mmr")
    # similarity_score_retriever = vector_store.as_retriever(
    #         search_type="similarity_score_threshold", 
    #         search_kwargs={"score_threshold": 0.2}
    #     )

    # retriever = similarity_retriever
    retriever = mmr_retriever
    # retriever = similarity_score_retriever

    return retriever


def init_chain(retriever):

    azure_model = AzureChatOpenAI(
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version = os.getenv("OPENAI_API_VERSION")
    )


    #history aware retriever
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
        "please answer the question in Korean."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        azure_model, retriever, contextualize_q_prompt
    )


    #Answer Question
    qa_system_prompt_str = """
    You are an assistant for recommending recipe. 
    Answer for the question in Korean.
    사용자가 입력한 음식에 대한 레시피를 알려줘.
    요리 제목, 재료, 요리 순서, 요리에 필요한 재료로 구성되도록 만들어줘.
    이 외의 부가적인 텍스트는 포함하지 않았으면 좋겠어.
    요리 제목은 요리 이름 + 레시피 형태로 해주고, h2 형식으로 만들어줘.
    재료를 먼저 알려주고 자세한 요리 순서를 포함하여 번호를 매겨서 작성해주면 좋겠어.
    각 항목의 제목은 "재료", "요리 순서" 로 작성해주고 각각을 h4 형식으로 만들어줘.
    요리 순서의 제목 텍스트("요리 순서") 위에 선을 하나 만들어줘.
    요리 순서의 내용이 끝난 후 아래에 선을 하나 만들어줘.
    여기까지는 마크다운 형식으로 작성해줘.
    요리에 필요한 재료는 마크다운 형식 이후에 예시와 같이 출력해줘. 
    재료는 단어 형태로만 작성부탁할게.
    예시: ["재료1", "재료2", "재료3", "재료4", "재료5"]

    {context} """.strip()

    qa_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt_str),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(azure_model, qa_prompt_template)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    memory = ConversationBufferMemory(
            chat_memory=InMemoryChatMessageHistory(),        
            return_messages=True
        )

    load_context_runnable = RunnablePassthrough().assign(
        chat_history=RunnableLambda(lambda x:memory.chat_memory.messages)
    )

    def save_context(chain_output):
        memory.chat_memory.add_user_message(chain_output["input"])
        memory.chat_memory.add_ai_message(chain_output["answer"])
        return chain_output["answer"]

    save_context_runnable = RunnableLambda(save_context)

    rag_chain_with_history = load_context_runnable | rag_chain | save_context_runnable

    return rag_chain_with_history
