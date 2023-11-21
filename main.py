import streamlit as st
import os
import pandas as pd
import pysftp
from io import StringIO
import matplotlib.pyplot as plt
import plotly.express as px


myHostname = st.secrets['hostname']
port = st.secrets['portnumber']
myUsername = st.secrets['username']
myPassword = st.secrets['password']

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
sftp = pysftp.Connection(host=myHostname, port=port, username=myUsername, password=myPassword, cnopts=cnopts)


# Produtos
with sftp.open('/dados/BF/produtos.csv', 'r') as remote_file:
    contents_bytes = remote_file.read()

contents_str = contents_bytes.decode('utf-8')  # Converter bytes para string
dfp = pd.read_csv(StringIO(contents_str), sep=';')
dfp['EXCEDENTE'] = dfp['EXCEDENTE'].str.replace(',', '.').astype(float)
dfp['ESTOQUE'] = dfp['ESTOQUE'].str.replace(',', '.').astype(float)
dfp = dfp.sort_values('EXCEDENTE')
dfp['SEQPRODUTO'] = dfp['SEQPRODUTO'].astype(str)

df = dfp[['EMPRESA','SEQPRODUTO','DESCCOMPLETA','EXCEDENTE']].head(20)


# STREAMLIT
# Gráfico interativo usando Plotly Express
fig = px.bar(df, x='SEQPRODUTO', y='EXCEDENTE', title='Excedente por SKU',
             labels={'EXCEDENTE': 'Quantidade excedente', 'SEQPRODUTO': 'SKU'})

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)
