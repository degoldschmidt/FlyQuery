import flyquery
from flyquery.gsheets import GoogleClient
from flyquery.query import fill_in, get_genotype
from google.oauth2.credentials import Credentials
import streamlit as st
import json
import pandas as pd

### Upload service account details
st.header('Welcome to Stock List Magic!')
st.subheader('Upload your data using the sidebar.')

uploaded_file = st.sidebar.file_uploader('Upload your stock list.', type='csv')
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)

    options = st.sidebar.multiselect('What information do you want to add to your stock list?', ['genotype', 'shortname'])
    id_col = st.sidebar.selectbox('Select column with BDSC IDs.', [col for col in df.columns])

    if st.sidebar.button('Fill in information'):
        ### Fill in genotype data from given stock IDs
        new_df = fill_in(df, id_col=id_col, add_columns=options)
        st.write(new_df)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
