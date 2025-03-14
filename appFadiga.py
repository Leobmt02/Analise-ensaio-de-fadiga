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
    
    # Verificar se há dados suficientes para plotar
    if not df.empty:
        # Calcular e exibir o valor máximo de ciclos
        max_value_cycles = df['CycleCount'].max()
        st.write(f"Cycles: {max_value_cycles} Ciclos")
        
        # Calcular e exibir os valores mínimos e máximos de kN e mm
        st.write(f"kN Minimo: {df['kN'].min():.2f} kN | kN Maximo: {df['kN'].max():.2f} kN")
        st.write(f"mm Minimo: {df['mm'].min():.2f} mm | mm Maximo: {df['mm'].max():.2f} mm")

        # Criar o primeiro gráfico (kN x CycleCount)
        fig1, ax1 = plt.subplots()
        df.plot(kind='line', x='CycleCount', y='kN', ax=ax1)
        plt.xlabel("CycleCount")
        plt.ylabel("kN")
        plt.title("Força (kN) vs. Ciclos")

        # Ajustar dinamicamente os limites de y para kN
        min_kN = df['kN'].min()
        max_kN = df['kN'].max()
        plt.ylim(min_kN - 0.1 * (max_kN - min_kN), max_kN + 0.1 * (max_kN - min_kN))

        # Ajustar o limite de x para CycleCount
        plt.xlim(0, df['CycleCount'].max())
        st.pyplot(fig1)

        # Criar o segundo gráfico (mm x CycleCount)
        fig2, ax2 = plt.subplots()
        df.plot(kind='line', x='CycleCount', y='mm', ax=ax2, color='orange')
        plt.xlabel("CycleCount")
        plt.ylabel("mm")
        plt.title("Deslocamento (mm) vs. Ciclos")

        # Ajustar dinamicamente os limites de y para mm
        min_mm = df['mm'].min()
        max_mm = df['mm'].max()
        plt.ylim(min_mm - 0.1 * (max_mm - min_mm), max_mm + 0.1 * (max_mm - min_mm))

        # Ajustar o limite de x para CycleCount
        plt.xlim(0, df['CycleCount'].max())
        st.pyplot(fig2)
    else:
        st.write("O DataFrame está vazio. Verifique os dados do arquivo CSV.")
