# Create Code from metadata
The Original purpose for this was to create code from metadata provided inside the Clinical Data Spec that usually is done in SAS.
The program takes a prompt that contains the metadata provided by the user and converts that into code in user provided language using OpenAI API.

- To install the required modules, open the terminal and run `pip install -r requirements.txt`
- To run the code, type the command in the Terminal below `streamlit run app3.py`

### Inside the UI
- You can upload the metadata dataset (.csv or .xlsx) and it will get displayed on the bottom right text area in a comma separated manner.
- Copy that dataset from text area and paste it on the top text area under #Metadata heading then press the Send Prompt to run the command and it will return the response on the right.

This code is free to use/distribute for any purpose, under legal terms.
