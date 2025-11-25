from langchain_community.utilities import SQLDatabase 

def create_mysql(host, port, user, password, database)-> SQLDatabase:
    db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_url)
