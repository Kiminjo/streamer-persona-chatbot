from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

import pandas as pd
from pathlib import Path 
from typing import Union, List
from tqdm import tqdm
import re

def get_data(src: Union[str, Path]) -> List[List]:
    df = pd.read_csv(src)
    qustions = df["question"].values
    answers = df["answer"].values
    return qustions, answers

def get_api_key(src: Union[str, Path]):
    with open(src, 'r') as f:
        return f.read()
    
def make_llm_chain(api_key: str):
    template = """너는 데이터를 증강하는 역할을 하는 챗봇이야. 
                내가 질문과 이에 매칭되는 답변을 입력하면 이에 유사한 질문을 3개 생성해줘. 

                예를 들어, 내가 
                질문: '방장님 어디 살아요?'
                답변: '저 성수동에 살아요' 
                라는 문서를 입력했다고 가정해봐.

                그러면 너는 질문과 유사하면서도 기존에 있는 답변과 매칭이 되는 새로운 질문 3가지를 생성해줘.
                예를 들어 
                1. '방장아 너는 어디 살아?' 
                2. '방장! 니 어디 사는데?' 
                3. '방장님은 어디에 살고 있나요?'
                이렇게 3개의 문장을 생성해줘.
                
                질문: 침착맨님, {question}
                답변: {answer}"""

    prompt = PromptTemplate.from_template(template)

    llm = OpenAI(openai_api_key=api_key)
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain

def get_answer(llm_chain: LLMChain, question: str, answer: str):
    input_variables = {
        "question": question,
        "answer": answer
    }

    output = llm_chain.run(input_variables)
    output = sentence_cleaning(output)
    return output

def sentence_cleaning(sentence: str) -> List:
    pattern = r'\d+\.\s(.+?)(?=\n|$)'
    return re.findall(pattern, sentence) 
    

def main():
    # Get data and API key source 
    # data_src = "../data/raw_data.csv"
    # api_src = "../openai_api.txt"
    data_src = "data/raw_data.csv"
    api_src = "openai_api.txt"

    # Get data and API key
    questions, answers = get_data(data_src)
    api_key = get_api_key(api_src)

    # Make LLM chain
    llm_chain = make_llm_chain(api_key)

    # Get augmented questions
    augmented_questions = []
    for q, a in zip(questions, answers):
        augmented_questions.append(get_answer(llm_chain, q, a))
        print("here")

if __name__ == "__main__":
    main()