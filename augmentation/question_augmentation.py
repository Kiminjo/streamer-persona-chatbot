from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

import pandas as pd
from pathlib import Path 
from typing import Union, List
from tqdm import tqdm
import re

from prompts import template1

def get_data(src: Union[str, Path]) -> List[List]:
    df = pd.read_csv(src)
    qustions = df["question"].values
    answers = df["answer"].values
    return qustions, answers

def get_api_key(src: Union[str, Path]):
    with open(src, 'r') as f:
        return f.read()
    
def make_llm_chain(api_key: str, template: str):
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
    data_src = "data/test_data.csv"
    api_src = "openai_api.txt"

    # Set template 
    template = template1

    # Get data and API key
    questions, answers = get_data(data_src)
    api_key = get_api_key(api_src)

    # Make LLM chain
    llm_chain = make_llm_chain(api_key, template)

    # Get augmented questions
    augmented_questions = []
    for q, a in zip(questions, answers):
        augmented_questions.append(get_answer(llm_chain, q, a))
    print("here")

if __name__ == "__main__":
    main()