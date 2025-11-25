from langchain_community.utilities import SQLDatabase 
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os



def get_sql_chain(db:SQLDatabase):
    template="""
    you are a data analyst at a company. you are interacting with a user who is asking you questions about the company's database.
    based on the table schema, write sql queries to answer the user's questions.
    take the conversation history into account when generating the queries.
    <SCHEMA>{schema}</SCHEMA>
    conversation history: {chat_history}

    write sql query to answer and nothing else. do not wrap the sql query in any other text, not even backticks.
    for example:
      Question: which 3 artists have the most tracks?
        sql query: SELECT ArtistId, COUNT(*) AS TrackCount FROM Track GROUP BY ArtistId ORDER BY TrackCount DESC LIMIT 3;
        Question:  Name 10 artists 
        sql query: SELECT Name FROM Artist LIMIT 10;

        Your turn:

        Question: {question}
        sql query:
        """
    prompt=PromptTemplate.from_template(
        template=template
      )

    llm=ChatGroq(temperature=0, model_name="meta-llama/llama-4-scout-17b-16e-instruct",groq_api_key=os.getenv("GROQ_API_KEY"))

    def get_schema(_):
        return db.get_table_info()
    
    return (
        RunnablePassthrough.assign(schema=get_schema) | prompt | llm | StrOutputParser()
    )
