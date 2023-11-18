from dynaconf import Dynaconf, Validator

validators = {
    'llm.model_name': Validator(
        'llm.model_name',
        must_exist=True,
        condition=lambda v: isinstance(v, str),
    ),
    'llm.openai_api_key': Validator(
        'llm.openai_api_key',
        must_exist=True,
        condition=lambda v: isinstance(v, str),
    ),
     'db.uri': Validator(
        'db.uri',
        must_exist=True,
        condition=lambda v: isinstance(v, str),
    )
}

# 加载配置文件
settings = Dynaconf(
    envvar_prefix='CHART_GPT',
    load_dotenv=True,
    settings_files=[
        'settings.toml',
    ],
)
