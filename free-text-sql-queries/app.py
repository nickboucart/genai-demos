import gradio as gr
from llm4sql import generateQueryByLmm
from tickets_db import create_tables_query, runQueryAndReturnDF

def doDemoQuery(question):
    sql= generateQueryByLmm('\n'.join(create_tables_query), question)
    if "can't answer this question" in sql:
        return ("I cannot answer this question, please reformulate.", None)
    resultAsDf =  runQueryAndReturnDF(sql)
    return (sql, resultAsDf)

def generateQuery(schema, question):
    return generateQueryByLmm(schema, question)

with gr.Blocks() as demo:
    gr.Markdown('''
    # genAI SQL-generation demo
    Wouldn't it be cool if your users can use **natural language** to query your database. Instead of providing them with predefined reports, or complex wizzards, just let them write their question in natural language, and let llms do the rest.
   
    This demo illustrates how this can be done.
                
    Use a simple provided sqlite database to see it in action immediately, or bring your own schema and experiment on that.
                
''')
    
    with gr.Tab("Use our demo database"):
        gr.Markdown('''Use a demo ticketing database with 3 tables: authors, tickets and comments.
                    
                    The demo shows both the generated query, as the result of running that query against the demo database.
                    
                    Start by using questions like **show me all users**, **list all tickets** or **how many comments are there** to get a feeling of the data itself, and explore away.''')
        question = gr.Textbox(label="Your Question", lines=3, max_lines=5)
        doQuery = gr.Button(value="Get SQL statement and perfrom query")
        sqlQuery = gr.Code(language="sql", label="Generated SQL statement")
        df = gr.DataFrame()
        doQuery.click(doDemoQuery, inputs=[question], outputs=[sqlQuery, df])
    with gr.Tab("Bring your own schema"):
        gr.Markdown('''Generate sql queries based on your own database schema. 
                    
                    **Disclaimer**: this demo does not guarantee that the queries it generates are correct. Worst case scenario, they might alter or delete data. Use with caution.
                    ''')
        schema = gr.Code(language="sql", label="Your database scheme - create table statements")
        question = gr.Textbox(label="Your Question", lines=3, max_lines=5)
        getSql = gr.Button(value="Get SQL statement")
        sqlQuery = gr.Code(language="sql")
        getSql.click(generateQuery, inputs=[schema, question], outputs=sqlQuery)

if __name__ == "__main__":
    demo.launch(show_api=False)