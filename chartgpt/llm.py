from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from chartgpt.utils import load_llm_from_config
from chartgpt.config import settings
from chartgpt.prompts import query_prompt, answer_prompt


llm: ChatOpenAI = load_llm_from_config(settings.llm)

query_chain = LLMChain(prompt=query_prompt, llm=llm)
answer_chain = LLMChain(prompt=answer_prompt, llm=llm)
