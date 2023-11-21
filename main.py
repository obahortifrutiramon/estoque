import streamlit as st
import os
import pandas as pd
import pysftp
from io import StringIO
import matplotlib.pyplot as plt
import plotly.express as px


myHostname = st.secrets[hostname]
port = st.secrets[portnumber]
myUsername = st.secrets[username]
myPassword = st.secrets[password]

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
sftp = pysftp.Connection(host=myHostname, port=port, username=myUsername, password=myPassword, cnopts=cnopts)


# Kits
with sftp.open('/dados/BF/kits.csv', 'r') as remote_file:
    contents_bytes = remote_file.read()

contents_str = contents_bytes.decode('utf-8')  # Converter bytes para string
dfk = pd.read_csv(StringIO(contents_str), sep=';')
dfk = dfk[(dfk['SKU VTEX'] != 'SKU') & (dfk['NROEMPRESA'] == 1)]



# Produtos
with sftp.open('/dados/BF/produtos.csv', 'r') as remote_file:
    contents_bytes = remote_file.read()

contents_str = contents_bytes.decode('utf-8')  # Converter bytes para string
dfp = pd.read_csv(StringIO(contents_str), sep=';')





# STREAMLIT
# Gráfico interativo usando Plotly Express
fig = px.bar(dfk, x='SKU VTEX', y='EXCEDENTE', title='Excedente por KIT',
             labels={'EXCEDENTE': 'Quantidade excedente', 'SKU VTEX': 'ID do kits na vtex'})

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)
