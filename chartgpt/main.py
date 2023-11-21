import json, random, time
from datetime import datetime
import streamlit as st

from chartgpt.config import settings
from chartgpt.db import db, sql
from chartgpt.llm import query_chain, answer_chain
from chartgpt.utils import output_to_json
from chartgpt.ui.sidebar import sidebar
from chartgpt.ui.table import table
from chartgpt.ui.components import tag


page = settings.st.page


chart_type_mapping = {
    '面积图': st.area_chart,
    '折线图': st.line_chart,
    '柱状图': st.bar_chart
}

st.set_page_config(
    page_title=page.title, 
    page_icon=page.icon, 
    layout=page.layout
)

st.image(image='./assets/images/logo.png', width=150)
st.header(f"{page.icon} {page.title}")

sidebar()

# style
st.markdown("""
<style>
summary span div p {
    font-weight: bold;
}
</style>""", unsafe_allow_html=True)

table()

with st.form(key="question_form"):
    query = st.text_area("Ask a question about the tables", placeholder=page.input_placeholder)
    submit = st.form_submit_button("Submit")


if submit:
    start = time.time()
    answer_col, sources_col = st.columns([2, 1])

    with answer_col:
        emojis = ["🎊", "🎃", "🎄", "🎀", "✨", "🎉", "🎁"]
        random.shuffle(emojis)
        with st.status(f'LLM is answering, it may take a while. ⏳', expanded=True, state="running"):
            if not query:
                st.stop()
    
            # Output Columns
            with sources_col:
                with st.expander(f"{emojis.pop()} SQL Prompt", False):
                    tag(key="time", value=datetime.now(), start=start)
                    st.code(
                        query_chain.prompt.format(
                            question=query,
                            dialect=db.dialect,
                            table_info=db.get_table_info()
                        ), 
                        language="json"
                    )

            # 转换SQL
            answer = query_chain.predict(
                question=query,
                dialect=db.dialect,
                table_info=db.get_table_info()
            )

            prev_result = output_to_json(answer)

            with sources_col:
                with st.expander(f"{emojis.pop()} SQL Answer", False):
                    tag(key="time", value=datetime.now(), start=start)
                    st.code(json.dumps(prev_result, indent=2, ensure_ascii=False), language="json")

            sql_result = sql(prev_result.get("sql_query", ''))
            chart_result = sql(prev_result.get("chart_sql", ''))

            with sources_col:
                with st.expander(f"{emojis.pop()} SQL Result.", False):
                    tag(key="time", value=datetime.now(), start=start)
                    cols = st.columns(2)
                    with cols[0]:
                        st.dataframe(sql_result)
                    with cols[1]:
                        st.dataframe(chart_result)

            if sql_result.empty:
                st.error("对不起, 大模型没有理解你的问题.\n\n" + page.help_text, icon="😦")
                st.stop()

            st_chart = chart_type_mapping[prev_result.get("chart_type", '柱状图')]

            with sources_col:
                with st.expander(f"{emojis.pop()} Summary Prompt", False):
                    tag(key="time", value=datetime.now(), start=start)
                    st.code(
                        answer_chain.prompt.format(
                            prev_result=answer,
                            question=query,
                            sql_result=sql_result.to_string(index=False),
                            chart_result=chart_result.to_string(index=False),
                        ), 
                        language="json"
                    )

            final_anwser = answer_chain.predict(
                prev_result=answer,
                question=query,
                sql_result=sql_result.to_string(index=False),
                chart_result=chart_result.to_string(index=False),
            )

            final_result = output_to_json(final_anwser)

            with sources_col:
                with st.expander(f"{emojis.pop()} Summary Answer", False):
                    tag(key="time", value=datetime.now(), start=start)
                    st.code(json.dumps(final_result, indent=2, ensure_ascii=False), language="json")

            if final_result["color"] in ("green", "blue"):
                st.success("**" + final_result["header"] + '** \n\n' + final_result["summary"], icon="✨")
            else:
                st.error("**" + final_result["header"] + '** \n\n' + final_result["summary"], icon="😦")

            chart_arguments = dict(
                data=final_result["chart"]['data'],
                x=final_result["chart"]["x_column"], 
                y=final_result["chart"]["y_column"],
            )

            if st.bar_chart == st_chart:
                chart_arguments["color"] = final_result["chart"]["x_column"]

            st_chart(**chart_arguments)







