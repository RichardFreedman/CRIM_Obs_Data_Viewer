import streamlit as st
from pathlib import Path
import requests
import pandas as pd
from pandas.io.json import json_normalize

# sets up function to call Markdown File for "about"
def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

#main heading of the resource

st.header("CRIM Project Data")

st.subheader("These tools assemble metadata for about 5000 observations in Citations: The Renaissance Imitation Mass [https://crimproject.org]")

# st.cache speeds things up by holding data in cache

@st.cache(allow_output_mutation=True)

# get the data function 
def get_data():
    data = requests.get('http://crimproject.org/data/observations/').json()
    #df = pd.DataFrame(data)
    df = pd.json_normalize(data)
    return df 
df = get_data()

select_data = df[["id", "observer.name", "piece.piece_id", "musical_type"]]

# to show full datafram

if st.sidebar.checkbox('Show All Metadata Fields'):
    st.subheader('All CRIM Observations with All Metadata')
    st.write(df)

if st.sidebar.checkbox('Show Selected Metadata:  Observer, Piece, Type'):
    st.subheader('Selected Metadata:  Observer, Piece, Type')
    st.write(select_data)

if st.sidebar.checkbox('Show Total Observations per Analyst'):
    st.subheader('Total Observations per Analyst')
    st.write(df['observer.name'].value_counts())  

if st.sidebar.checkbox('Show Total Observations per Piece Title'):
    st.subheader('Total Observations per Analyst')
    st.write(df['piece.full_title'].value_counts()) 

if st.sidebar.checkbox('Show Total Observations per Piece ID'):
    st.subheader('Total Observations per Piece ID')
    st.write(df['piece.piece_id'].value_counts()) 

if st.sidebar.checkbox('Show Total Observations per Musical Type'):
    st.subheader('Total Observations per Musical Type')
    st.write(df['musical_type'].value_counts())    

st.header("Select Observations by Analyst")
obs_list = select_data['observer.name'].unique()
obs_selected = st.multiselect('', obs_list)

# # Mask to filter dataframe:  returns only those "selected" in previous step
masked_obs = select_data['observer.name'].isin(obs_selected)

select_data_1 = select_data[masked_obs]
st.write(select_data_1)

st.header("Select Observations by Piece")
piece_list = select_data['piece.piece_id'].unique()
pieces_selected = st.multiselect('', piece_list)

# # Mask to filter dataframe:  returns only those "selected" in previous step
masked_pieces = select_data['piece.piece_id'].isin(pieces_selected)

select_data_2 = select_data[masked_pieces]
st.write(select_data_2)

st.header("Select Observations by Musical Type")
type_list = select_data['musical_type'].unique()
types_selected = st.multiselect('', type_list)

# # Mask to filter dataframe:  returns only those "selected" in previous step
masked_types = select_data['musical_type'].isin(types_selected )

select_data_3 = select_data[masked_types]
st.write(select_data_3)








