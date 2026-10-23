# %% [markdown]
# Source notebook: Lesson_5_Student.ipynb
# Cell order and explanatory text are preserved; saved outputs are omitted.
# See SOURCE_FILES.md at the repository root for runtime requirements.

# %% [markdown]
# ## Adding Web Search To Your LLM

# %%
# Notebook cell 2
from dotenv import load_dotenv
_ = load_dotenv()

# %% [markdown]
# #### Asking Your LLM For The Latest Information

# %%
# Notebook cell 4
from utils import query_raven
question = "Hey, can you tell me more about this R1 thing that was announced by Rabbit? "

no_function_calling_prompt = \
f"""
<s> [INST] {question} [/INST]
"""
query_raven(no_function_calling_prompt)

# %% [markdown]
# #### Providing Up To Date Information

# %%
# Notebook cell 6
import os

def do_web_search(full_user_prompt : str, num_results : int = 5):
    API_URL = f'{os.getenv("DLAI_TAVILY_BASE_URL", "https://api.tavily.com")}/search'
    payload = \
    {
      "api_key": os.environ["TAVILY_API_KEY"],
      "query": full_user_prompt,
      "search_depth": "basic",
      "include_answer": False,
      "include_images": False,
      "include_raw_content": False,
      "max_results": num_results,
      "include_domains": [],
      "exclude_domains": []
    }
    import requests
    response = requests.post(API_URL, json=payload)
    response = response.json()
    all_results = "\n\n".join(item["content"] for item in response["results"])
    return all_results

# %% [markdown]
# #### Calling Raven

# %%
# Notebook cell 8
function_calling_prompt = \
"""
Function:
def do_web_search(full_user_prompt : str, num_results : int = 5):
    '''
    Searches the web for the user question.
    '''

Example:
User Query: What is the oldest capital in the world?
Call: do_web_search(full_user_prompt="oldest capital")

User Query: {query}<human_end>
"""
fc_result = query_raven(function_calling_prompt.format(query=question))
print (fc_result)

# %%
# Notebook cell 9
result = eval(fc_result)

# %%
# Notebook cell 10
full_prompt = \
f"""
<s> [INST]
{result}

Use the information above to answer the following question concisely.

Question:
{question} [/INST]
"""

# %%
# Notebook cell 11
grounded_response = query_raven(full_prompt.format(question = question))

# %%
# Notebook cell 12
print (grounded_response)

# %% [markdown]
# ## Chatting With Your SQL Database
# > Note below: The database values are randomly generated so your values may differ from those in the video.

# %%
# Notebook cell 14
from utils import create_random_database
create_random_database()

# %%
# Notebook cell 15
question = "What is the most expensive item we currently sell?"

# %%
# Notebook cell 16
from utils import execute_sql, query_raven

schema = \
"""
CREATE TABLE IF NOT EXISTS toys (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL
);
"""

raven_prompt = \
f'''
Function:
def execute_sql(sql_code : str):
  """
  Runs sql code for a company internal database
  """

Schema: {schema}
User Query: {question}
'''

output = query_raven(raven_prompt)
print (f"LLM's function call: {output}")
database_result = eval(output)

# %%
# Notebook cell 17
full_prompt = \
f"""
<s> [INST]
{database_result}

Use the information above to answer the following question concisely.

Question:
{question} [/INST]
"""
grounded_response = query_raven(full_prompt)
print (grounded_response)

# %% [markdown]
# ### Safer Interactions With Databases

# %%
# Notebook cell 19
import sqlite3
import random

# Internal database name setting
DB_NAME = 'toy_database.db'

# Connect to the database
def connect_db():
    return sqlite3.connect(DB_NAME)

# %%
# Notebook cell 20
# List all toys
def list_all_toys():
    with connect_db() as conn:
        cursor = conn.execute('SELECT * FROM toys')
        return cursor.fetchall()

# %%
# Notebook cell 21
# Find toy by name prefix
def find_toy_by_prefix(prefix):
    with connect_db() as conn:
        query = 'SELECT * FROM toys WHERE name LIKE ?'
        cursor = conn.execute(query, (prefix + '%',))
        return cursor.fetchall()

# %%
# Notebook cell 22
# Find toys in a price range
def find_toys_in_price_range(low_price, high_price):
    with connect_db() as conn:
        query = 'SELECT * FROM toys WHERE price BETWEEN ? AND ?'
        cursor = conn.execute(query, (low_price, high_price))
        return cursor.fetchall()

# %%
# Notebook cell 23
# Get a random selection of toys
def get_random_toys(count=5):
    with connect_db() as conn:
        cursor = conn.execute('SELECT * FROM toys')
        all_toys = cursor.fetchall()
        return random.sample(all_toys, min(count, len(all_toys)))

# %%
# Notebook cell 24
# Function to get the most expensive toy
def get_most_expensive_toy(count=1):
    with connect_db() as conn:
        cursor = conn.execute(f'SELECT * FROM toys ORDER BY price DESC LIMIT {count}')
        return cursor.fetchone()

# %%
# Notebook cell 25
# Function to get the cheapest toy
def get_cheapest_toy(count=1):
    with connect_db() as conn:
        cursor = conn.execute('SELECT * FROM toys ORDER BY price ASC LIMIT {count}')
        return cursor.fetchone()

# %%
# Notebook cell 26
raven_prompt = \
f'''
Function:
def list_all_toys():
    """
    Retrieves a list of all toys from the database. This function does not take any parameters.
    Returns: A list of tuples, where each tuple represents a toy with all its attributes (id, name, price).
    """

Function:
def find_toy_by_prefix(prefix):
    """
    Searches for and retrieves toys whose names start with a specified prefix.
    Parameters:
    - prefix (str): The prefix to search for in toy names.
    Returns: A list of tuples, where each tuple represents a toy that matches the prefix criteria.
    """

Function:
def find_toys_in_price_range(low_price, high_price):
    """
    Finds and returns toys within a specified price range.
    Parameters:
    - low_price (float): The lower bound of the price range.
    - high_price (float): The upper bound of the price range.
    Returns: A list of tuples, each representing a toy whose price falls within the specified range.
    """

Function:
def get_random_toys():
    """
    Selects and returns a random set of toys from the database, simulating a "featured toys" list.

    Returns: A list of tuples, each representing a randomly selected toy. The number of toys returned is up to the specified count.
    """

Function:
def get_most_expensive_toy(count : int):
    """
    Retrieves the most expensive toy from the database.
    This function does not take any parameters.

    Returns: A tuple representing the most expensive toy, including its id, name, and price.
    """

Function:
def get_cheapest_toy(count : int):
    """
    Finds and retrieves the cheapest toy in the database.
    This function does not take any parameters.

    Returns: A tuple representing the cheapest toy, including its id, name, and price.
    """

User Query: {question}<human_end>

'''

output = query_raven(raven_prompt)
print (output)
results = eval(output)

# %%
# Notebook cell 27
full_prompt = \
f"""
<s> [INST]
{database_result}

Use the information above to answer the following question in a single sentence.

Question:
{question} [/INST]
"""
grounded_response = query_raven(full_prompt)
print (grounded_response)

# %%
# Notebook cell 28

