import pandas as pd
from typing import List, Optional
from langchain.utilities.sql_database import SQLDatabase
from langchain.utilities.sql_database import truncate_word
from chartgpt.config import settings


class Database(SQLDatabase):
   
   def get_table_info(self, table_names: List[str] | None = None) -> str:
        res = super().get_table_info(table_names)
      
        if self.dialect == "sqlite":
            schemas = db._execute("SELECT name, sql FROM sqlite_master WHERE type='table';", fetch="all")
            create_mapping = { i["name"]: i["sql"] for i in schemas }

            table_infos = res.split('\n\n')
            for (index, line) in enumerate(table_infos):
                for name, sql in create_mapping.items():
                    if line.startswith(f'\nCREATE TABLE {name}'):
                        table_infos[index] = create_mapping[name]

            return '\n\n'.join(table_infos)

        return res
         
      
db: Database = Database.from_uri(settings.db.uri)


def sql(command: str, fetch: str = "all") -> pd.DataFrame:
    if not command:
        return []
    
    with db._engine.begin() as connection:
        return pd.read_sql(command, con=connection)
