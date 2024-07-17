# Generate SQL queries from a free form quesion

In this PoC, we'll show how to use a large language model to generate a sql statement that answers a question from a user.

This project contains the code for running an small demo database, or you can decide to bring your own schema and generate the sql accordingly.

To run the project, create a virtual environment, install dependancies and run the main file.

```
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

python app.py

```

This will start a gradio based web frontend, containing 2 tabs.

On the first tab, you'll be able to setup a local demo sqlite database, with some demo data. This demo will show both the generated sql data, as well as the result from running that query against the demo database.

The second tab will allow you bring your own schema (sql create statements for your database), and use the llm to generate the sql queries. You can simply copy/paste that sql and run it against your database. BEWARE: this project does not guarantee that the generated SQL is correct and/or doesn't do harm, always use caution.
