# %% [markdown]
# Source notebook: Lesson_4_Student.ipynb
# Cell order and explanatory text are preserved; saved outputs are omitted.
# See SOURCE_FILES.md at the repository root for runtime requirements.

# %% [markdown]
# # Using Function Calling For Structure

# %% [markdown]
# ## Simple Example Of Address Extraction

# %%
# Notebook cell 3
text = \
"""
John Doe lives at 123 Elm Street, Springfield. Next to him is Jane Smith, residing at 456 Oak Avenue, Lakeview. Not far away, we find Dr. Emily Ryan at 789 Pine Road, Westwood. Meanwhile, in a different part of town, Mr. Alan Turing can be found at 101 Binary Blvd, Computerville. Nearby, Ms. Olivia Newton stays at 202 Music Lane, Harmony. Also, Prof. Charles Xavier is located at 505 Mutant Circle, X-Town.
"""
print (text)

# %%
# Notebook cell 4
raven_prompt = \
f'''
Function:
def address_name_pairs(names : list[str], addresses : list[str]):
"""
Give names and associated addresses.
"""

{text}<human_end>
'''

# %%
# Notebook cell 5
from utils import query_raven

def address_name_pairs(names : list[str], addresses : list[str]):
  """
  Give names and associated addresses.
  """
  for name, addr in zip(names, addresses):
    print (name, ": ", addr)

result = query_raven(raven_prompt)
eval(result)

# %% [markdown]
# ## Alternative Way of Doing Extraction

# %%
# Notebook cell 7
unbalanced_text = \
"""
Dr. Susan Hill has a practice at 120 Green Road, Evergreen City, and also consults at 450 Riverdale Drive, Brookside. Mark Twain, the renowned author, once lived at 300 Maple Street, Springfield, but now resides at 200 Writers Block, Literaryville. The famous artist, Emily Carter, showcases her work at 789 Artisan Alley, Paintown, and has a studio at 101 Palette Place, Creativeland. Meanwhile, the tech innovator, John Tech, has his main office at 555 Silicon Street, Techville, and a secondary office at 777 Data Drive, Computown, but he lives at 123 Digital Domain, Innovatown.
"""
print (unbalanced_text)

# %%
# Notebook cell 8
raven_prompt = \
f'''

@dataclass
class Record:
    name : str
    addresses : List[str]

Function:
def insert_into_database(names : List[Record]):
"""
Inserts the records into the database. 
"""

{unbalanced_text}<human_end>

'''

result = query_raven(raven_prompt)
print (result)

# %% [markdown]
# ## Generating Valid JSONs

# %% [markdown]
# ```
# {
#   "city_name" : "London"
#   "location" : {
#       "country" : "United Kingdom",
#       "continent" : {
#           "simple_name" : "Europe",
#           "other_name" : "Afro-Eur-Asia"
#       }
#   }
# }
# ```

# %%
# Notebook cell 11
def city_info(city_name : str, location : dict):
  """
  Gets the city info
  """
  return locals()
def construct_location_dict(country : str, continent : dict):
  """
  Provides the location dictionary
  """
  return locals()
def construct_continent_dict(simple_name : str, other_name : str):
  """
  Provides the continent dict
  """
  return locals()

# %%
# Notebook cell 12
print (city_info("London", {}))

# %%
# Notebook cell 13
raven_prompt = \
'''
Function:
def city_info(city_name : str, location : dict):
"""
Gets the city info
"""

Function:
def construct_location_dict(country : str, continent : dict):
"""
Provides the location dictionary
"""

def construct_continent_dict(simple_name : str, other_name : str):
"""
Provides the continent dict
"""

User Query: {question}<human_end>
'''

# %%
# Notebook cell 14
question = "I want the city info for London, "\
"which is in the United Kingdom, which is in Europe or Afro-Eur-Asia."

output = query_raven(raven_prompt.format(question = question))
json0 = eval(output)
print (json0)

# %%
# Notebook cell 15
import json
json.dumps(json0)

# %% [markdown]
# ### Try These yourself!

# %%
# Notebook cell 17
question = "I need details for the city of Tokyo, "\
"situated in Japan, a part of the Asian continent, "\
"which is sometimes referred to as Eurasia."

output = query_raven(raven_prompt.format(question = question))
json1 = eval(output)
print (json1)

# %%
# Notebook cell 18
import json
json.dumps(json0)

# %%
# Notebook cell 19

