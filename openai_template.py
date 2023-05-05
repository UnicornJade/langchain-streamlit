import os
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


"""----------------------------------------------------------------"""


def translate(lang, role,text):
    en2zh = "Hi,my friend {role}.Please translate english to chinese:{text}"
    zh2en = "Hi,my friend {role}.Please translate chinese to english:{text}"
    if lang == 'English':
        template = zh2en
    elif lang == '简体中文':
        template = en2zh

    llm = OpenAI(temperature=0)
    prompt = PromptTemplate(
        input_variables=["role","text"],  # 提示词·可控变量
        template=template,
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(role,text).strip()
