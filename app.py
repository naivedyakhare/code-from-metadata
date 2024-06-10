import streamlit as st
from openai import OpenAI
import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

st.set_page_config(layout="wide")
st.title('Code Creator')

supported_languages = ['SAS', 'R', 'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'Go', 'PHP']

# Sidebar for file upload
with st.sidebar:
    st.header('Upload excel File containing metadata')
    sas_file = st.file_uploader('Upload a file', type=['csv', 'xlsx'])

    # Select the source and target languages
    target_language = st.selectbox('Target Language:', ['SAS', 'R', 'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'Go', 'PHP'])

    random_btn = st.button("Send Prompt")

columns = ""
metadata = " "

default_prompt = '''I am SAS programmer, and I want to create CDISC dm (demographic) data using SAS. Use below table under # Metadata, delimited by comma to create the code. Also, refer to SAS codes under # Reference Code. Just keep SAS code and remove everything else. I want raw SAS Code.

# Metadata


# Reference code

'''

# Input for the source code
if sas_file is not None:
    if sas_file.name.endswith(".csv"):
        df = pd.read_csv(sas_file)
    elif sas_file.name.endswith(".xlsx"):
        df = pd.read_excel(sas_file)
    else:
        st.error("You can only give CSV (comma separated value) or XLSX (Excel) files as input")
    
    columns = ", ".join(df.columns)
    metadata = []

    n_rows = len(df)
    for i in range(n_rows):
        row = ""
        for item in df.iloc[i,:]:
            row += str(item) + ", "
        row = row.rstrip(",")
        metadata.append(row)

    metadata = list(map(lambda x: x.rstrip(", "), metadata))
    

input_column, output_column = st.columns(2)

with output_column:
    st.write("Your output will be generated here: ")

# Use the code editor component
with input_column:
    input_prompt = st.text_area(height=200,value=default_prompt, label="Enter the metadata inside #Metadata and enter reference code (if required) inside #Reference code and send it using send prompt. You can change the prompt as per your requirement but it is mandatory to put your metadata table and reference code inside the dedicated string #Metadata and #Reference Code")
    input_metadata = st.text_area(height=300,value=columns + "\n" + "\n".join(metadata), label="Enter your metadata here or upload a file from sidebar, edit it if required and copy paste it under # Metadata in the above text area 👆")

# Function to call OpenAI API
def create_code(columns=None, metadata=None, target_language="SAS"):
    global default_prompt

    if metadata == None:
        prompt = input_prompt
    else:
        prompt = f'''{columns}\n{metadata}\n
            You have been given the metadata. Create a code in the {target_language} based on the given metadata.

            {input_prompt}

        '''
    print(prompt)

    client = OpenAI(api_key = os.environ.get("NAIVEDYA_OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
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

if random_btn:
    if input_prompt:
        with st.spinner('Converting...'):
            created_code = create_code(None, None, target_language)

            with output_column:
                st.code(f"{created_code}", language=target_language.lower())
    else:
        with output_column:
            st.error('Please enter the source code or upload a file.')