from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

from sql_formatter.core import format_sql


llm = ChatOllama(
    model = "llama3:instruct"
)
system_template = """
You are a database expert. 
You use the provided database scheme to generate a sql statement that answers the question below. 
Only answer the sql statement itself, no commentary, no opening or closing quotes"""
user_template = """
database schema: {database_scheme}
question: {question}"""
prompt_template = ChatPromptTemplate.from_messages(
[("system", system_template), ("user", user_template)])
parser = StrOutputParser()
chain = prompt_template | llm | parser 

def generateQueryByLmm(schema, question, wellFormatted=True):
    sql = chain.invoke({"database_scheme": schema, "question": question})
    if (wellFormatted):
        sql = format_sql(sql)
    print(sql)
    return sql