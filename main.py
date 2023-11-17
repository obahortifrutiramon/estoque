import streamlit as st
import os
import cx_Oracle
import pandas as pd
import matplotlib.pyplot as plt

df_skus = pd.read_excel('products.xlsx')

skusList = []
skusList = list(df_skus['SEQPRODUTO'].drop_duplicates())



hostName = st.secrets["host_Name"]
portNumber = st.secrets["port_Number"]
serviceName = st.secrets["service_Name"]
userName = st.secrets["user_Name"]
personalPassword = st.secrets["personal_Password"]

#dsn_tns = cx_Oracle.makedsn(hostName, portNumber, service_name=serviceName)
#conn = cx_Oracle.connect(user=userName, password=personalPassword, dsn=dsn_tns)

#c = conn.cursor()

#query1 = '''
#    select nroempresa, seqproduto, estqloja, qtdreservadavda from consinco.mrl_produtoempresa 
#    where seqproduto in (''' + str(skusList).replace('[','').replace(']','') + ''') 
#    '''
#df_estoque = pd.read_sql_query(query1, conn)



df = df_skus.merge(df_estoque, how='left', on=['SEQPRODUTO'])
df['ESTOQUE'] = df['ESTQLOJA'] - df['QTDRESERVADAVDA']
df['EXCEDENTE'] = df['ESTOQUE'] - df['QUANTIDADE']
df = df.sort_values(['PRODUTO','NROEMPRESA','EXCEDENTE'])
df['EXCMIN'] = df.groupby(['PRODUTO','NROEMPRESA'])['EXCEDENTE'].transform('first')

df_kits = df[['SKU VTEX','PRODUTO','NROEMPRESA','EXCMIN']].drop_duplicates()
df_prod = df[['SEQPRODUTO','PRODUTO','NROEMPRESA','EXCEDENTE']].drop_duplicates()

# def plot_grafico(dataframe):
#     fig, ax = plt.subplots()
#     ax.bar(x='PRODUTO', height='EXCEDENTE', width=0.8, data=dataframe)
#     return fig


    
if __name__ == "__main__":
    # Titulo da pagina
    st.set_page_config(page_title="Acompanhamento de Estoque")
    st.title("Acompanhamento de Estoque\n")
    
    df_kitsalerta = df_kits[df_kits['EXCMIN'] < 5]
    st.bar_chart(data=df_kitsalerta, x='PRODUTO', y=['EXCMIN'], color=None, width=0, height=0)
    
#     figura = plot_grafico(df.head(5))
#     st.pyplot(figura)
    
    
    
