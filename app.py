import streamlit as st
from openai import OpenAI
import os
import pandas as pd

st.set_page_config(layout="wide")
st.title('Code Creator')

supported_languages = ['SAS', 'R', 'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'Go', 'PHP']

columns = ""
rows = ""
# Sidebar for file upload
with st.sidebar:
    st.header('Upload excel File containing metadata')
    sas_file = st.file_uploader('Upload a file', type=['csv', 'xlsx'])

    # Select the source and target languages
    target_language = st.selectbox('Target Language:', ['R', 'SAS', 'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'Go', 'PHP'])

    create_btn = st.button("Create")



# Input for the source code
if sas_file is not None:
    
    df = pd.read_excel(sas_file)
    print("HERES THE DEAD /////// ", df.head())
    columns = sas_file.readline()
    # columns = sas_file.readline().decode('utf-8')
    metadata = []

    rows = sas_file.read().decode("utf-8")
    # print("HERES THE PRINT, ", columns, rows)
    # rows = sas_file.read().decode('utf-8')
    for line in rows.split("\n"):
        metadata.append(line)

input_column, output_column = st.columns(2)

with output_column:
    st.write("Your output will be generated here: ")

# Use the code editor component
with input_column:
    st.text_area(height=300,value=columns+rows, label="Enter your metadata here or upload a file from sidebar")

# Function to call OpenAI API
def create_code(columns, metadata, target_language):
    prompt = f'''
        {columns}\n{metadata}\n You have been given the metadata. Create a code in the {target_language} based on the given metadata.

        The response should follow these rules:
        1. No explanation
        2. No backticks for code
        3. No need to tell the response language
        4. Only give raw code and nothing else
        5. The example column is just a scenario. It's not suuposed to be used for any purpose.
    
    '''
    # return prompt

    client = OpenAI(api_key = os.environ.get("KEVIN_OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You create code from the given metadata."},
            {"role": "user", "content": prompt}
        ],
        stream=True,
    )
    
    output = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            output += chunk.choices[0].delta.content
    
    return output

if create_btn:
    if metadata:
        with st.spinner('Converting...'):
            created_code = ""
            for data in metadata:
                created_code = created_code + "\n\n" + create_code(columns, data, target_language)

            with output_column:
                st.code(f"{created_code}", language=target_language.lower())
    else:
        with output_column:
            st.error('Please enter the source code or upload a file.')