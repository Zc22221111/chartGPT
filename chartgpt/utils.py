import json
from typing import Any, List
from langchain.llms.loading import *


def _import_chat_openai() -> Any:
    from langchain.chat_models import ChatOpenAI
    return ChatOpenAI


def load_llm_from_config(config: dict) -> BaseLLM:
    """Load LLM from Config Dict."""
    if "_type" not in config:
        raise ValueError("Must specify an LLM Type in config")
    config_type = config.pop("_type")
    
    type_to_cls_dict = get_type_to_cls_dict()

    type_to_cls_dict["chatOpenai"] = _import_chat_openai

    if config_type not in type_to_cls_dict:
        raise ValueError(f"Loading {config_type} LLM not supported")

    llm_cls = type_to_cls_dict[config_type]()

    return llm_cls(**config)


def output_to_json(input: str) -> dict:
    try:
        data = json.loads(input)
        return data
    except Exception as e:
        raise e
