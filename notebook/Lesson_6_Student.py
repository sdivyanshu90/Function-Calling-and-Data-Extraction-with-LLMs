# %% [markdown]
# Source notebook: Lesson_6_Student.ipynb
# Cell order and explanatory text are preserved; saved outputs are omitted.
# See SOURCE_FILES.md at the repository root for runtime requirements.

from IPython import get_ipython as _active_ipython

def get_ipython():
    """Use the active shell and expose this script namespace to line magics."""
    shell = _active_ipython()
    if shell is None:
        raise RuntimeError("This source uses IPython commands; run it with ipython instead of python.")
    import inspect
    caller = inspect.currentframe().f_back
    shell.user_ns.update(caller.f_globals)
    shell.user_ns.update(caller.f_locals)
    return shell

# %% [markdown]
# # Building A Dialogue Feature Extraction Pipeline Using Function Calling!

# %%
# Notebook cell 2
sample_data = \
"""Agent: Thank you for calling BrownBox Customer Support. My name is Tom. How may I assist you today?\nCustomer: Hi Tom, I'm trying to log in to my account to purchase an Oven Toaster Grill (OTG), but I'm unable to proceed as it's asking for mobile number or email verification. Can you help me with that?\nAgent: Sure, I can assist you with that. May I know your registered mobile number or email address, please?\nCustomer: My registered mobile number is +1 123-456-7890.\nAgent: Thank you. Let me check that for you. I'm sorry to inform you that we don't have this number on our records. Can you please confirm if this is the correct number?\nCustomer: Oh, I'm sorry. I might have registered with a different number. Can you please check with my email address instead? It's johndoe@email.com.\nAgent: Sure, let me check that for you. (After a few moments) I see that we have your email address on our records. We'll be sending you a verification code shortly. Please check your email and let me know once you receive it. Customer: Okay, I received the code. What do I do with it?\nAgent: Please enter the verification code in the field provided and click on 'Verify'. Once your email address is verified, you'll be able to proceed with your purchase.\nCustomer: Okay, I entered the code, and it's verified now. Thank you for your help.\nAgent: You're welcome. Is there anything else I can assist you with?\nCustomer: No, that's all. Thank you.\nAgent: You're welcome. Have a great day!"""

# %%
# Notebook cell 3
print (sample_data)

# %% [markdown]
# ### Defining What's Important

# %%
# Notebook cell 5
from utils import query_raven
from typing import List
from dataclasses import dataclass
# Warning control
import warnings
warnings.filterwarnings('ignore')

# %%
# Notebook cell 6
from dataclasses import dataclass
schema_id = ("agent_name", "customer_email", \
             "customer_order", "customer_phone", "customer_sentiment")

dataclass_schema_representation = '''
@dataclass
class Record:
    agent_name : str # The agent name
    customer_email : str # customer email if provided, else ''
    customer_order : str # The customer order number if provided, else ''
    customer_phone : str # the customer phone number if provided, else ''
    customer_sentiment : str # Overall customer sentiment, either 'frustrated', or 'happy'. Always MUST have a value.
'''

# Let's call exec to insert the dataclass into our python interpreter so it understands this. 
exec(dataclass_schema_representation)

# %% [markdown]
# ### Building The Database

# %%
# Notebook cell 8
def initialize_db():
    import sqlite3

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('extracted.db')
    cursor = conn.cursor()

    # Fixed table name
    table_name = "customer_information"

    # Fixed schema
    columns = """
    id INTEGER PRIMARY KEY, 
    agent_name TEXT, 
    customer_email TEXT, 
    customer_order TEXT, 
    customer_phone TEXT, 
    customer_sentiment TEXT
    """

    # Ensure the table name is enclosed in quotes if it contains special characters
    quoted_table_name = f'"{table_name}"'

    # Check if a table with the exact name already exists
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name={quoted_table_name}")
    if cursor.fetchone():
        print(f"Table {table_name} already exists.")
    else:
        # Create the new table with the fixed schema
        cursor.execute(f'''CREATE TABLE {quoted_table_name} ({columns})''')
        print(f"Table {table_name} created successfully.")

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

# %%
# Notebook cell 9
get_ipython().system('rm extracted.db')
initialize_db()

# %% [markdown]
# ### Adding in Tools To Populate The Database

# %%
# Notebook cell 11
from dataclasses import dataclass, fields
def update_knowledge(results_list : List[Record]):
    """
    Registers the information necessary
    """
    import sqlite3
    from sqlite3 import ProgrammingError

    # Reconnect to the existing SQLite database
    conn = sqlite3.connect('extracted.db')
    cursor = conn.cursor()

    # Fixed table name
    table_name = "customer_information"

    # Prepare SQL for inserting data with fixed column names
    column_names = "agent_name, customer_email, customer_order, customer_phone, customer_sentiment"
    placeholders = ", ".join(["?"] * 5) 
    sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

    # Insert each record
    for record in results_list:
        try:
            record_values = tuple(getattr(record, f.name) for f in fields(record))
            cursor.execute(sql, record_values)
        except ProgrammingError as e:
            print(f"Error with record. {e}")
            continue

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Records inserted successfully.")

# %%
# Notebook cell 12
my_record = Record(agent_name = "Agent Smith", \
                   customer_email = "", customer_order = "12346", \
                   customer_phone = "", customer_sentiment = "happy")

# %%
# Notebook cell 13
update_knowledge([my_record])

# %% [markdown]
# ### Building Tools To Pull Information Out

# %%
# Notebook cell 15
import sqlite3
def execute_sql(sql: str):
    """ Runs SQL code for the given schema. Make sure to properly leverage the schema to answer the user's question in the best way possible. """
    # Fixed table name, assuming it's not dynamically generated anymore
    table_name = "customer_information"

    # Establish a connection to the database
    conn = sqlite3.connect('extracted.db')
    cursor = conn.cursor()

    # Execute the SQL statement
    cursor.execute(sql)

    # Initialize an empty list to hold query results
    results = []

    results = cursor.fetchall()
    print("Query operation executed successfully. Number of rows returned:", len(results))

    # Close the connection to the database
    conn.close()

    # Return the results for SELECT operations; otherwise, return an empty list
    return results

# %%
# Notebook cell 16
sql = '''
    SELECT agent_name 
        FROM customer_information
        WHERE customer_sentiment = "happy"
    '''
# Print the final SQL command for debugging
print("Executing SQL:", sql)

execute_sql(sql)

# %% [markdown]
# -----

# %% [markdown]
# ## Building The Pipeline

# %%
# Notebook cell 19
get_ipython().system('rm extracted.db')
initialize_db()

# %% [markdown]
# ##### Attribution:
# We will be using a handful of samples (~10-15 samples) in this lesson from a publically-available customer_service_chatbot on HuggingFace.
# The link to the public dataset is here: https://huggingface.co/datasets/SantiagoPG/customer_service_chatbot

# %%
# Notebook cell 21
from datasets import load_dataset
import os

cwd = os.getcwd()
dialogue_data = load_dataset(cwd + "/data/customer_service_chatbot", cache_dir="./cache")["train"]

# %%
# Notebook cell 22
sample_zero = dialogue_data[6]
dialogue_string = sample_zero["conversation"].replace("\n\n", "\n")
print (dialogue_string)

# %%
# Notebook cell 23
import inspect

prompt = "\n" + dialogue_string

signature = inspect.signature(update_knowledge)
signature = str(signature).replace("__main__.Record", "Record")
docstring = update_knowledge.__doc__

raven_prompt = f'''{dataclass_schema_representation}\nFunction:\n{update_knowledge.__name__}{signature}\n    """{docstring}"""\n\n\nUser Query:{prompt}<human_end>'''
print (raven_prompt)

# %%
# Notebook cell 24
raven_call = query_raven(raven_prompt)
print (raven_call)

# %%
# Notebook cell 25
exec(raven_call)

# %%
# Notebook cell 26
import inspect

sample_zero = dialogue_data[10]
dialogue_string = sample_zero["conversation"].replace("\n\n", "\n")

prompt = "\n" + dialogue_string
signature = inspect.signature(update_knowledge)
docstring = update_knowledge.__doc__
raven_prompt = f'''{dataclass_schema_representation}\nFunction:\n{update_knowledge.__name__}{signature}\n    """{docstring}"""\n\n{prompt}<human_end>'''

raven_call = query_raven(raven_prompt)
print (raven_call)
exec(raven_call)

# %%
# Notebook cell 27
execute_sql(
    '''
    SELECT COUNT(customer_sentiment) 
    FROM customer_information
    WHERE agent_name = "John" AND customer_sentiment = "happy"
    ''')

# %%
# Notebook cell 28
prompt = "how many customers John has made happy."

signature = inspect.signature(execute_sql)

docstring = execute_sql.__doc__

sql_schema_representation = \
"""
CREATE TABLE customer_information (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT,
    customer_email TEXT,
    customer_order TEXT,
    customer_phone TEXT,
    customer_sentiment TEXT
);
"""

raven_prompt = f'''{sql_schema_representation}\nFunction:\n{execute_sql.__name__}{signature}\n    """{docstring}"""\n\n\nUser Query:{prompt}<human_end>'''

print (raven_prompt)

# %%
# Notebook cell 29
raven_call = query_raven(raven_prompt)

print (raven_call)

# %%
# Notebook cell 30
eval(raven_call)

# %%
# Notebook cell 31
get_ipython().system('rm extracted.db')
initialize_db()

# %%
# Notebook cell 32
from tqdm import tqdm

for i in tqdm(range(0, 10)):
    data = dialogue_data[i]
    dialogue_string = data["conversation"].replace("\n\n", "\n")

    # Ask Raven to extract the information we want out of this dialogue. 
    prompt = "\n" + dialogue_string
    signature = inspect.signature(update_knowledge)
    docstring = update_knowledge.__doc__
    raven_prompt = f'''{dataclass_schema_representation}\nFunction:\n{update_knowledge.__name__}{signature}\n    """{docstring}"""\n\n\nUser Query:{prompt}<human_end>'''
    raven_call = query_raven(raven_prompt)
    print (raven_call)
    exec(raven_call)

# %%
# Notebook cell 33
signature = inspect.signature(execute_sql)

docstring = execute_sql.__doc__

schema_representation = \
"""
CREATE TABLE customer_information (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT,
    customer_email TEXT,
    customer_order TEXT,
    customer_phone TEXT,
    customer_sentiment TEXT
);
"""

raven_prompt = f'''{schema_representation}\nFunction:\n{execute_sql.__name__}{signature}\n    """{docstring}"""\n\n\n'''
raven_prompt = raven_prompt + "User Query: How many happy customers?<human_end>"
print (raven_prompt)
raven_call = query_raven(raven_prompt)

print (raven_call)
eval(raven_call)

# %%
# Notebook cell 34
raven_prompt = f'''{schema_representation}\nFunction:\n{execute_sql.__name__}{signature}\n    """{docstring}"""\n\n\n'''
raven_prompt = raven_prompt + \
"User Query: Give me the names and phone numbers of the ones"\
"who are frustrated and the order numbers?<human_end>"

print (raven_prompt)
raven_call = query_raven(raven_prompt)

print (raven_call)
eval(raven_call)

# %%
# Notebook cell 35

