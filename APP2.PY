import streamlit as st
from openai import OpenAI
import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
load_dotenv(r"C:\Users\rohit\OneDrive\Desktop\Awesome LLM Apps\.env")

st.set_page_config(layout="wide")
st.title('Code Creator')

supported_languages = ['SAS', 'R', 'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'Go', 'PHP']

columns = ""
metadata = " "
# Sidebar for file upload
with st.sidebar:
    st.header('Upload excel File containing metadata')
    sas_file = st.file_uploader('Upload a file', type=['csv', 'xlsx'])

    # Select the source and target languages
    target_language = st.selectbox('Target Language:', ['SAS', 'R', 'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'Go', 'PHP'])

    create_btn = st.button("Create")
    random_btn = st.button("OTHER BUTTON")



# Input for the source code
if sas_file is not None:
    if sas_file.name.endswith(".csv"):
        df = pd.read_csv(sas_file)
    elif sas_file.name.endswith(".xlsx"):
        df = pd.read_excel(sas_file)
    else:
        st.error("You can only give CSV (comma separated value) or XLSX (Excel) files as input")
    
    columns = " || ".join(df.columns)
    metadata = []

    n_rows = len(df)
    for i in range(n_rows):
        row = ""
        for item in df.iloc[i,:]:
            row += str(item) + " || "
        row = row.rstrip("||")
        metadata.append(row)

    metadata = list(map(lambda x: x.rstrip(" || "), metadata))
    

input_column, output_column = st.columns(2)

with output_column:
    st.write("Your output will be generated here: ")

# Use the code editor component
with input_column:
    f = st.text_area(height=300,value=columns + "\n" + "\n".join(metadata), label="Enter your metadata here or upload a file from sidebar")

# Function to call OpenAI API
def create_code(columns, metadata, target_language):
    prompt = f'''
        {columns}\n{metadata}\n
        You have been given the metadata. Create a code in the {target_language} based on the given metadata. Return a complete dataset!
        Each value in a row is separated by the special character double pipe (||).
        Info about Input:
        1. The Variable_Name is the target variable to be created.
        2. The Variable_Label column is the description about the variable to be created (Not to be used in Code).
        3. The Type columns consists of datatype of the variable to be created (Not to be used in Code).
        4. The Deriviation column tells us how the data is mapped into the Variable_Name
        5. The Example column is just an example. (Not to be used in Code)
        6. The output of the mapping is inside the dm dataset


        The response should follow these rules:

        1. No explanation
        2. No backticks for code
        3. No need to tell the response language
        4. Only give raw code and nothing else
    
    '''
    print(prompt)
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
            # print(input_metadata)
            columns = input_metadata.split("\n")[0].lstrip("\n")
            metadata = input_metadata.split("\n")[1:]

            for data in metadata:
                # print(columns, "\n", data)
                created_code = created_code + "\n\n" + create_code(columns, data, target_language)

            with output_column:
                st.code(f"{created_code}", language=target_language.lower())
    else:
        with output_column:
            st.error('Please enter the source code or upload a file.')












