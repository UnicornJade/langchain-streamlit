import os
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
openai_api_key = "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"
os.environ["OPENAI_API_KEY"] = openai_api_key

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
