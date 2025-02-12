import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Definir o tamanho dos chunks para renderização
plt.rcParams['agg.path.chunksize'] = 100000

# Título do aplicativo
st.title("📊 Ensaios de Teste de Fadiga")

# Configurar tamanho máximo do upload
st.write("**Aviso:** O aplicativo suporta arquivos de até 20GB usando carregamento em chunks.")

# Carregar o arquivo CSV
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=["csv"])

if uploaded_file is not None:
    # Opção para o usuário escolher o delimitador
    delimiter = st.selectbox("Escolha o delimitador do arquivo CSV", [',', ';', '\t', '|'])
    
    try:
        # Criar um gerador para processar grandes arquivos
        chunk_size = 1000000  # 1 milhão de linhas por vez
        df_chunks = pd.read_csv(uploaded_file, delimiter=delimiter, encoding='utf-8', skiprows=2, usecols=['CycleCount', 'mm', 'kN'], chunksize=chunk_size)
        
        # Ler apenas a primeira parte do arquivo para pré-visualização
        df = next(df_chunks)
        
        # Exibir as primeiras linhas do DataFrame
        st.write("### Visualização Inicial dos Dados:")
        st.write(df.head())
        
        # Selecionar colunas para os eixos X e Y
        x_column = st.selectbox("Escolha a coluna para o eixo X", ['CycleCount'])
        y_column = st.selectbox("Escolha a coluna para o eixo Y", ['mm', 'kN'])
        
        # Exibir Estatísticas
        st.write("### Estatísticas dos Dados:")
        st.write(f"**Cycles Máximo:** {df['CycleCount'].max()}")
        st.write(f"**kN Mínimo:** {df['kN'].min()} - kN Máximo: {df['kN'].max()}")
        st.write(f"**mm Mínimo:** {df['mm'].min()} - mm Máximo: {df['mm'].max()}")
        
        # Gráfico
        st.write("### Gráfico de Dados:")
        fig, ax = plt.subplots()
        df.plot(kind='line', x=x_column, y=y_column, ax=ax)
        plt.ylim(-1.8, 1.8)
        plt.xlim(0, df[x_column].max())
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(f'{y_column} x {x_column}')
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
else:
    st.info("Por favor, faça o upload de um arquivo CSV.")
