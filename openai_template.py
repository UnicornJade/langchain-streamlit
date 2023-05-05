import os
import streamlit
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

"""----------------------------------------------------------------"""

def translate(lang, text):
    en2zh = "Please translate english to chinese:{text}"
    zh2en = "Please translate chinese to english:{text}"
    if lang == 'English':
        template = zh2en
    elif lang == '简体中文':
        template = en2zh

    llm = OpenAI(temperature=0)
    prompt = PromptTemplate(
        input_variables=["text"],  # 提示词·可控变量
        template=template,
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(text).strip()

def planMaker(content):
    template = """You are a coach. You will be responsible to me to the end. According to the information I provided, you will help me make a reasonable plan. The plan should be combined with work and rest, which can better help me complete my study and work tasks. Your answer should be as short and clear as possible and in Chinese.Here are my latest plans：'{content}'"""
    llm = OpenAI(temperature=0.9)
    prompt = PromptTemplate(
        input_variables=["content"],  # 提示词·可控变量
        template=template,
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(content).strip()
