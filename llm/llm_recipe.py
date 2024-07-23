from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
import os


def GetInformation(input_text) :    
    load_dotenv()
    
    # 모델 셋팅 
    model = AzureChatOpenAI(
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"), 
        temperature=1.0
    )

    # 프롬프트 템플릿 구성. 
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. 답변은 한국어로 해줘."),
        ("system", '''사용자가 입력한 음식에 대한 레시피를 알려줘. 형식은 마크타운으로.
        '''),
        ("human", "{input}")   
    ])

    output_parser = StrOutputParser()

    # 체인 구성.
    chain = prompt_template | model | output_parser
    
    output = chain.invoke({
        "input" : input_text,
    })

    return output
