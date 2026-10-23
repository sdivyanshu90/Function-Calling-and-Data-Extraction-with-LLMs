# %% [markdown]
# Source notebook: Lesson_1_Student.ipynb
# Cell order and explanatory text are preserved; saved outputs are omitted.
# See SOURCE_FILES.md at the repository root for runtime requirements.

# %% [markdown]
# # Introduction To Function Calling!

# %% [markdown]
# ### Writing A Local Python Tool

# %%
# Notebook cell 3
from matplotlib import pyplot as plt

def plot_some_points(x : list, y : list):
  """
  Plots some points!
  """
  plt.plot(x, y)
  plt.show()

# %%
# Notebook cell 4
USER_QUERY = "Hey can you plot y=10x where x=1, 2, 3 for me?"

# %%
# Notebook cell 5
plot_some_points(x=[1, 2, 3], y=[10, 20, 30])

# %%
# Notebook cell 6
prompt = \
f'''
Function:
def plot_some_points(x : list, y : list):
  """
  Plots some points!
  """
  plt.plot(x, y)
  plt.show()

User Query: {USER_QUERY}<human_end>
'''

# %%
# Notebook cell 7
from utils import query_raven
function_call = query_raven(prompt)

# %%
# Notebook cell 8
print (function_call)

# %%
# Notebook cell 9
exec(function_call)

# %% [markdown]
# #### Try Your Own!

# %%
# Notebook cell 11
USER_QUERY = ""

# %%
# Notebook cell 12
prompt = \
f'''
Function:
def plot_some_points(x : list, y : list):
  """
  Plots some points!
  """
  plt.plot(x, y)
  plt.show()

User Query: {USER_QUERY}<human_end>
'''
from utils import query_raven
function_call = query_raven(prompt)

# %%
# Notebook cell 13


# %% [markdown]
# ### Let's Try Another Example!

# %% [markdown]
# #### Let's define a function

# %%
# Notebook cell 16
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_clown_face(face_color='yellow', eye_color='black', 
                    nose_color='red'):
    """
    Draws a customizable, simplified clown face using matplotlib.

    Parameters:
    - face_color (str): Color of the clown's face. Default is 'yellow'.
    - eye_color (str): Color of the clown's eyes. Default is 'black'.
    - nose_color (str): Color of the clown's nose. Default is 'red'.

    This function creates a plot displaying a simplified clown face, where essential facial features' size, position, and color can be customized. 
    """
    # Constants
    face_radius = 0.4
    nose_radius = 0.1
    nose_x, nose_y = 0.5, 0.5
    mouth_x, mouth_y = 0.5, 0.3
    mouth_color = 'black'
    eye_size = 0.05
    mouth_size = (0.3, 0.1)
    eye_offset=(0.15, 0.15)
    mouth_theta = (200, 340)

    fig, ax = plt.subplots()
    # Face
    face = patches.Circle((0.5, 0.5), face_radius, color=face_color, fill=True)
    ax.add_patch(face)
    # Eyes
    eye_left = patches.Circle((0.5-eye_offset[0], 0.5+eye_offset[1]), eye_size, color=eye_color, fill=True)
    eye_right = patches.Circle((0.5+eye_offset[0], 0.5+eye_offset[1]), eye_size, color=eye_color, fill=True)
    ax.add_patch(eye_left)
    ax.add_patch(eye_right)
    # Nose
    nose = patches.Circle((nose_x, nose_y), nose_radius, color=nose_color, fill=True)
    ax.add_patch(nose)
    # Mouth
    mouth = patches.Arc((mouth_x, mouth_y), mouth_size[0], mouth_size[1], angle=0, 
                        theta1=mouth_theta[0], theta2=mouth_theta[1], color=mouth_color, linewidth=2)
    ax.add_patch(mouth)
    # Setting aspect ratio to 'equal' to ensure the face is circular
    ax.set_aspect('equal')
    # Remove axes
    ax.axis('off')
    plt.show()

# %% [markdown]
# #### Let's Define A Prompt

# %%
# Notebook cell 18
USER_QUERY = \
"Hey can you draw a pink clown face with a red nose" 

raven_prompt = \
'''
Function:
def draw_clown_face(face_color='yellow', 
                    eye_color='black',
                    nose_color='red'):
    """
    Draws a customizable, simplified clown face using matplotlib.

    Parameters:
    - face_color (str): Color of the clown's face.
    - eye_color (str): Color of the clown's eyes.
    - nose_color (str): Color of the clown's nose.
    """

User Query: {query}<human_end>
'''
raven_prompt_with_query = raven_prompt.format(query=USER_QUERY)

# %%
# Notebook cell 19
print (raven_prompt_with_query)

# %%
# Notebook cell 20
from utils import query_raven
raven_call = query_raven(raven_prompt_with_query)
print (raven_call)

# %% [markdown]
# #### Let's Run The Call

# %%
# Notebook cell 22
exec(raven_call)

# %% [markdown]
# #### Make Your Own Clown!

# %%
# Notebook cell 24
USER_QUERY = ""
raven_prompt_with_query = raven_prompt.format(query=USER_QUERY)

from utils import query_raven
raven_call = query_raven(raven_prompt_with_query)
print (raven_call)
exec(raven_call)

# %% [markdown]
# #### Using OpenAI FC

# %%
# Notebook cell 26
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

_ = load_dotenv()

def query_openai(msg, functions=None):
  load_dotenv()
  GPT_MODEL = "gpt-3.5-turbo"

  openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
  openai_response = openai_client.chat.completions.create(
    model = GPT_MODEL,
    messages = [{'role': 'user', 'content': msg}],
    tools = functions)
  return openai_response

# %%
# Notebook cell 27
openai_function = {
  "type": "function",
  "function": {
    "name": "draw_clown_face",
    "description": "Draws a customizable, simplified clown face using matplotlib.",
    "parameters": {
      "type": "object",
      "properties": {
        "face_color": {
          "type": "string",
          "description": "Color of the clown's face."
        },
        "eye_color": {
          "type": "string",
          "description": "Color of the clown's eyes."
        },
        "nose_color": {
          "type": "string",
          "description": "Color of the clown's nose."
        }
        }
      }
    }
  }

openai_msg = \
"Hey can you draw a pink clown face with a red nose"

# %%
# Notebook cell 28
result = query_openai(openai_msg, functions=[openai_function])

# %%
# Notebook cell 29
print (result.choices[0].message.tool_calls[0].function)

# %%
# Notebook cell 30
tool_name = result.choices[0].message.tool_calls[0].function.name
tool_args = result.choices[0].message.tool_calls[0].function.arguments

# %%
# Notebook cell 31
function_call = f"{tool_name}(**{tool_args})"

# %%
# Notebook cell 32
print (function_call)

# %%
# Notebook cell 33
exec(function_call)

# %%
# Notebook cell 34

