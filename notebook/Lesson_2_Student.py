# %% [markdown]
# Source notebook: Lesson_2_Student.ipynb
# Cell order and explanatory text are preserved; saved outputs are omitted.
# See SOURCE_FILES.md at the repository root for runtime requirements.

# %% [markdown]
# # Function Calling

# %% [markdown]
# ### Housekeeping

# %%
# Notebook cell 3
def afunction(arg1:int = 0, arg2:str = "hello", **kwargs)->int:
    ''' this is a function definition
        arg1 (int): an exemplary yet modest argument
        arg2 (str): another nice argument
        **kwargs : the rest of the rabble 

        returns arg1 incremented by one
    '''
    return(arg + 1)

# %%
# Notebook cell 4
print(afunction.__name__)
print(afunction.__doc__)

# %%
# Notebook cell 5
import inspect
print(inspect.signature(afunction))

# %% [markdown]
# ##### Building User Query
# > Note, the video shows how to access utils.py in Jupyter Notebook V7.   
# > You may be in Jupyter Notebook V6. To access it in this version, on the menu, choose File->Open. 

# %%
# Notebook cell 7
import inspect
def build_raven_prompt(function_list, user_query):
    raven_prompt = ""
    for function in function_list:
        signature = inspect.signature(function)
        docstring = function.__doc__
        prompt = \
f'''
Function:
def {function.__name__}{signature}
    """
    {docstring.strip()}
    """

'''
        raven_prompt += prompt

    raven_prompt += f"User Query: {user_query}<human_end>"
    return raven_prompt

# %%
# Notebook cell 8
print( build_raven_prompt([afunction], "a query"))

# %% [markdown]
# ### Concrete Example For Parallel Calls

# %%
# Notebook cell 10
from utils import draw_clown_face

raven_msg = "Hey, can you build me two clowns." \
"The first clown should be red faced, with a blue nose" \
"and a mouth from 0 to 180 degrees. The mouth should be black." \
"The second clown should have a blue face and a green nose" \
"and a red mouth that's 180 to 360 degrees."

# %% [markdown]
# #### Building Raven Prompt

# %%
# Notebook cell 12
raven_prompt = build_raven_prompt([draw_clown_face], raven_msg)

print (raven_prompt)

# %%
# Notebook cell 13
from utils import query_raven
raven_call = query_raven(raven_prompt)
print (raven_call)
exec(raven_call)

# %% [markdown]
# ### Using Multiple Functions!

# %% [markdown]
# #### Building The Prompt

# %%
# Notebook cell 16
from utils import draw_clown_face, draw_tie
raven_msg = "Hey draw a tie?"
raven_prompt = build_raven_prompt\
    ([draw_clown_face, draw_tie], raven_msg)

# %%
# Notebook cell 17
print(raven_prompt)

# %% [markdown]
# #### Getting The Call

# %%
# Notebook cell 19
raven_call = query_raven(raven_prompt)
print (raven_call)

# %%
# Notebook cell 20
exec(raven_call)

# %% [markdown]
# ### Multiple Parallel Function Calling

# %% [markdown]
# #### Build The Prompt

# %%
# Notebook cell 23
raven_msg = "Draw a clown and a tie?"

# %%
# Notebook cell 24
raven_prompt = build_raven_prompt([draw_tie, draw_clown_face], raven_msg)
raven_call = query_raven(raven_prompt)

# %%
# Notebook cell 25
print (raven_call)

# %%
# Notebook cell 26
exec(raven_call)

# %% [markdown]
# ### What is the significance of the docstrings?

# %%
# Notebook cell 28
raven_msg = "Draw me a sad one with green head"
raven_prompt = build_raven_prompt([draw_clown_face], raven_msg)
raven_call = query_raven(raven_prompt)
print (raven_call)
exec(raven_call)

# %% [markdown]
# #### Fixing The Function Docstring

# %%
# Notebook cell 30
print (raven_prompt)

# %%
# Notebook cell 31
raven_prompt_targeted = \
'''
Function:
def draw_clown_face(face_color='yellow', eye_color='black', nose_color='red', eye_size=0.05, mouth_size=(0.3, 0.1), mouth_color='black', eye_offset=(0.15, 0.15), mouth_theta=(200, 340))
    """
    Draws a customizable, simplified clown face using matplotlib.

    Parameters:
    - face_color (str): Color of the clown's face. Default is 'yellow'.
    - eye_color (str): Color of the clown's eyes. Default is 'black'.
    - nose_color (str): Color of the clown's nose. Default is 'red'.
    - eye_size (float): Radius of the clown's eyes. Default is 0.05.
    - mouth_size (tuple): Width and height of the clown's mouth arc. Default is (0.3, 0.1).
    - eye_offset (tuple): Horizontal and vertical offset for the eyes from the center. Default is (0.15, 0.15).
    - mouth_theta (tuple): Controls the emotions of the clown. Starting and ending angles (in degrees) of the mouth arc. Default is (200, 340).

    This function creates a plot displaying a simplified clown face, where essential facial features' size, position, and color can be customized. 

    Example usage:
    draw_clown_face(face_color='lightblue', eye_color='green', nose_color='orange', 
                    eye_size=0.07, mouth_size=(0.4, 0.25), 
                    eye_offset=(0.2, 0.2), mouth_theta=(0, 180))

    # This will draw a simplified clown face with a light blue face, green eyes, an orange nose, and a smiling mouth.
    """

User Query: Draw me a sad one with green head<human_end>
'''

# %%
# Notebook cell 32
raven_call = query_raven(raven_prompt_targeted)
print (raven_call)
exec(raven_call)

# %% [markdown]
# ### Concrete Example For Nested APIs

# %%
# Notebook cell 34
raven_msg_nested = "Hey draw me a clown with "\
                    "a red face, blue eyes, green nose, "\
                    "and a black mouth open from 0 to 360 "\
                    "degrees?"

# %%
# Notebook cell 35
from utils import draw_head, draw_eyes, \
    draw_nose, draw_mouth, \
    draw_clown_face_parts
raven_function_nested = build_raven_prompt([draw_head, \
                                            draw_eyes, \
                                            draw_nose, \
                                            draw_mouth, \
                                            draw_clown_face_parts],\
                                            raven_msg_nested)
raven_call = query_raven(raven_function_nested)

# %%
# Notebook cell 36
print (raven_call)

# %%
# Notebook cell 37
exec(raven_call)

# %%
# Notebook cell 38

