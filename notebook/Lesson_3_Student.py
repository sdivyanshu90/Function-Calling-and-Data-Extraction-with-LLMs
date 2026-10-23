# %% [markdown]
# Source notebook: Lesson_3_Student.ipynb
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
# ### How Do We Interface With External Resources?

# %%
# Notebook cell 2
import requests

url = "https://v2.jokeapi.dev/joke/Any?safe-mode&type=twopart"

response = requests.get(url)

print(response.json()["setup"])
print(response.json()["delivery"])

# %%
# Notebook cell 3
response.json()

# %%
# Notebook cell 4
import requests
def give_joke(category : str):
    """
    Joke categories. Supports: Any, Misc, Programming, Pun, Spooky, Christmas.
    """

    url = f"https://v2.jokeapi.dev/joke/{category}?safe-mode&type=twopart"
    response = requests.get(url)
    print(response.json()["setup"])
    print(response.json()["delivery"])

# %%
# Notebook cell 5
USER_QUERY = "Hey! Can you get me a joke for this december?"

# %%
# Notebook cell 6
from utils import query_raven

raven_functions = \
f'''
def give_joke(category : str):
    """
    Joke categories. Supports: Any, Misc, Programming, Dark, Pun, Spooky, Christmas.
    """

User Query: {USER_QUERY}<human_end>
'''
call = query_raven(raven_functions)

# %%
# Notebook cell 7
exec(call)

# %% [markdown]
# #### Writing A Tool That Uses OpenAPI APIs

# %%
# Notebook cell 9
#!wget https://raw.githubusercontent.com/open-meteo/open-meteo/main/openapi.yml

# %%
# Notebook cell 10
import yaml
import json

# Read the content of the file
with open('openapi.yml', 'r') as file:
    file_content = file.read()
file_content = file_content.replace("int\n", "number\n")
file_content = file_content.replace("float\n", "number\n")
data = yaml.safe_load(file_content)

data["servers"] = [{"url":"https://api.open-meteo.com"}]

with open('openapi.json', 'w') as file:
    json_content = json.dump(data, file)

# %%
# Notebook cell 11
get_ipython().system('openapi-python-generator openapi.json ./api_specification_main/')

# %%
# Notebook cell 12
from api_specification_main.services.WeatherForecastAPIs_service\
    import get_v1forecast

# %%
# Notebook cell 13
user_query = "Hey how is the current weather and windspeed in New York?"

# %%
# Notebook cell 14
import inspect
signature = inspect.signature(get_v1forecast)
docstring = \
'''
Requires the latitude and longitude.
Set current_weather to True to get the weather.
Set hourly or daily based on preference.
'''

raven_prompt = \
f'''
Function:
{get_v1forecast.__name__}{signature}
"""{docstring}"""

User Query: {user_query}<human_end>'''

print (raven_prompt)

# %%
# Notebook cell 15
from utils import query_raven
call = query_raven(raven_prompt)
print (call)

# %%
# Notebook cell 16
eval(call)

# %%
# Notebook cell 17

