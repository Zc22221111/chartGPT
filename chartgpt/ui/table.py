import math
import streamlit as st
from chartgpt.db import db, sql


table_names = db.get_usable_table_names()
size = math.ceil(len(table_names) / 3)
table_names_groups = [table_names[i:i+size] for i in range(0, len(table_names), size)]


def table():
    with st.expander(f"🍞 DATABASE TABLES ({len(table_names)})", False):
        cols = st.columns(3)

        for index, group in enumerate(table_names_groups):
            with cols[index]:
                tabs = st.tabs([f'🏷️ {t}' for t in group])

                for table_name, tab in zip(group, tabs):
                    with tab:
                        res = sql(f"select * from {table_name};", "all")
                        st.dataframe(res, hide_index=True)
