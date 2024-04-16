import streamlit as st
import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=st.secrets["OPENAI_KEY"],
)

def generate_response(context, query_text): 

    ## Use a shorter template to reduce the number of tokens in the prompt
    prompt = f"""
    Answer the given questions using the provided context as a source. 
    ALWAYS include the original text as a citation in your answer citing only the minimal set of sources needed to answer the question. 
    If you are unable to answer the question, simply state that you do not have enough information to answer the question. 
    Use only the provided context and do not attempt to fabricate an answer.

    QUESTION: {query_text}

    CONTEXT:
    =========

    {context}
    """   

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-4",
    )
        
    return chat_completion.choices[0].message.content

# Open the file in read mode
with open('files/lundin_mining_candelaria_202.txt', 'r') as file:
    # Read the text from the file
    context = file.read()

# needs to be called first
st.set_page_config(
    page_title="Woven Mining",
    page_icon=":pick:",
    layout="wide",
)

st.markdown("""
# Ask Questions about the Candelaria Copper Mining Complex
### Candelaria Copper Mining Complex,
### Atacama Region, Chile
            
Sample includes sections on:
             
- Geology, Mineralization, and Deposit Types 
- Regional, Local, and Property Geology 
- Deposit Types
- Exploration 
- Drilling            
- Recovery Methods                       
""")

# Query text
query_text = st.text_input('Enter your question:')

# Form input and query
result = []

with st.form('myform', clear_on_submit=True):
    submitted = st.form_submit_button('Submit')
    with st.spinner('Calculating...'):
        if query_text:
            response = generate_response(context, query_text)
            result.append(response)

if len(result):
    st.info(response)

#st.text(context)
