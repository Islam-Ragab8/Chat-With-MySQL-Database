import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()

from langchain_core.messages import AIMessage, HumanMessage
from modules.sql_chain import  get_sql_chain
from modules.database import create_mysql
from modules.response_chain import get_response
    
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        AIMessage(content="Hello! I,m a SQL assistant. Ask me anything about your database.")
    ]


st.set_page_config(page_title="chat with MySQL",page_icon=":speech_balloon:")
st.title("Chat with MySQL Database :speech_balloon:")

with st.sidebar:
    st.header("Configuration")
    st.write("This is a simple app to chat with your MySQL database.")
    host = st.text_input("MySQL Host", value= "localhost",key="host")
    port = st.number_input("MySQL Port", value=3306, key="port")
    user = st.text_input("MySQL User", value="root", key="user")
    password = st.text_input("MySQL Password", type="password", value= "admin", key="password")
    database = st.text_input("Database Name", value="Chinook", key="database")

    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            db=create_mysql(
                st.session_state["host"],
                st.session_state["port"],
                st.session_state["user"],
                st.session_state["password"],
                st.session_state["database"],
            )
            st.session_state["db"]=db
            st.success("Connected to database!")


for message in st.session_state["chat_history"]:
    if isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
            
user_query=st.chat_input("Ask a question about your database:")
if user_query is not None and user_query.strip()!="":
    st.session_state["chat_history"].append(HumanMessage(content=user_query))
    
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        response= get_response(
            user_query,
            st.session_state["chat_history"],
            st.session_state["db"]
        )
        st.markdown(response)

    st.session_state["chat_history"].append(AIMessage(content=response))