import streamlit as st
from chartgpt.config import settings
from chartgpt import __version__

page = settings.st.page


def sidebar():
    with st.sidebar:
        st.success(f"""
## {page.icon} {page.title}
{page.title} 让你与数据库聊天，给你生成可视化图表与数据洞察。

## 怎么使用?
{page.help_text}
""")
        st.divider()

        st.image("./assets/images/cover.jpeg", output_format="auto")

        st.caption(f":blue[version]: {__version__}")