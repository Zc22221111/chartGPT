from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from chartgpt.utils import load_llm_from_config
from chartgpt.config import settings
from chartgpt.prompts import query_prompt, answer_prompt


llm: ChatOpenAI = load_llm_from_config(settings.llm)

# 查询链，通过自然语言转化SQL
query_chain = LLMChain(prompt=query_prompt, llm=llm)

# 答案链，总结答案（根据自然语言的问题和sql查询结果）
answer_chain = LLMChain(prompt=answer_prompt, llm=llm)
