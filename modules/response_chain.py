
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from modules.sql_chain import  get_sql_chain
from modules.database import create_mysql
from langchain_community.utilities import SQLDatabase 
import os

def get_response(user_query:str, chat_history:list , db:SQLDatabase)-> str:
    sql_chain=get_sql_chain(db)
    template= """
          you are a data analyst at a company. you are interacting with a user who is asking you questions about the company's database.
          based on the table schema below, question, sql_query, and sql response, write a natural language response.
            <SCHEMA>{schema}</SCHEMA>

            conversation history: {chat_history}
            sql query: <SQL>{query}</SQL>
            Question: {question}
            SQL Response: {response} """
    prompt=PromptTemplate.from_template(
        template=template
    )
    llm=ChatGroq(temperature=0, model_name="meta-llama/llama-4-scout-17b-16e-instruct",groq_api_key=os.getenv("GROQ_API_KEY"))

    chain= (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            response=lambda vars: db.run(vars["query"])  
        ) | prompt | llm | StrOutputParser()
    )
    
    return chain.invoke({
        "chat_history": chat_history,
        "question": user_query
    })
