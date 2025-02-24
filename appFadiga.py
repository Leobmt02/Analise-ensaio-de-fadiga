import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Definir o tamanho dos chunks
plt.rcParams['agg.path.chunksize'] = 100000

# Título do aplicativo
st.title("📊 Ensaios de Teste de Fadiga")

# Carregar o arquivo CSV
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    # Opção para o usuário escolher o delimitador
    delimiter = st.selectbox("Escolha o delimitador do arquivo CSV", [',', ';', '\t', '|'])
    
    # Carregar o arquivo CSV com ajuste no delimitador e na codificação
    df = pd.read_csv(uploaded_file, delimiter=delimiter, encoding='utf-8', skiprows=2, usecols=['CycleCount', 'mm', 'kN'])
    
    # Exibir as primeiras linhas do DataFrame
    #st.write(df.head())
    
    # Selecionar as colunas desejadas para os eixos X e Y
    x_column = st.selectbox("Escolha a coluna para o eixo X", ['CycleCount'])
    y_column = st.selectbox("Escolha a coluna para o eixo Y", ['mm', 'kN'])
    
    # Filtrar o DataFrame com as colunas selecionadas
    df_filtered = df[[x_column, y_column]]
    
    # Exibir o DataFrame filtrado
    #st.write(df_filtered)
    
    # Verificar se há dados suficientes para plotar
    if not df_filtered.empty:
        # Calcular e exibir o valor máximo de ciclos
        max_value_cycles = df['CycleCount'].max()
        st.write(f"Cycles: {max_value_cycles} Ciclos")
        
        # Calcular e exibir os valores mínimos e máximos de kN e mm
        min_value_kn = df['kN'].min()
        max_value_kn = df['kN'].max()
        st.write(f"kN Minimo: {min_value_kn:.2f} kN")
        st.write(f"kN Maximo: {max_value_kn:.2f} kN")
        
        min_value_mm = df['mm'].min()
        max_value_mm = df['mm'].max()
        st.write(f"mm Minimo: {min_value_mm:.2f} mm")
        st.write(f"mm Maximo: {max_value_mm:.2f} mm")
        
        # Gráfico
        fig, ax = plt.subplots()
        df_filtered.plot(kind='line', x=x_column, y=y_column, ax=ax)
        
        plt.ylim(-1.8, 1.8)
        plt.xlim(0, df_filtered[x_column].max())
        
        # Nome dos campos
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(f'{y_column} x {x_column}')
        
        st.pyplot(fig)
    else:
        st.write("O DataFrame filtrado está vazio. Verifique se as colunas selecionadas contêm dados.")
