import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# Configurar a API do Gemini
genai.configure(api_key="AIzaSyCjvIcpaMQFXy7jSMdrJy3BJoG1Ax93WH0")

# Carregar o arquivo Excel
caminhoArquivo = 'COPAS.xlsx'
xl = pd.ExcelFile(caminhoArquivo)

# Obter os nomes das planilhas (anos)
planilhas = xl.sheet_names

# Criar uma barra lateral para selecionar o ano
anoSelecionado = st.sidebar.selectbox('Selecione o Ano', planilhas)

# Carregar os dados da planilha selecionada
df = xl.parse(anoSelecionado)

# Exibir um título
st.title(f'Dados da Copa do Mundo - {anoSelecionado}')

# Filtros interativos
equipesSelecionadas = st.sidebar.multiselect('Selecione a Equipe', df['Equipe'].unique())

# Função para criar sliders com verificação
def criarSlider(label, coluna):
    valorMinimo = int(df[coluna].min())
    valorMaximo = int(df[coluna].max())
    if valorMinimo == valorMaximo:
        return valorMinimo, valorMaximo + 1  # Adicionar 1 para evitar erro
    return st.sidebar.slider(label, valorMinimo, valorMaximo, (valorMinimo, valorMaximo))

# Filtros adicionais
pontosMinimo, pontosMaximo = criarSlider('Pontos', 'PtsPontos')
partidasJogadasMinimo, partidasJogadasMaximo = criarSlider('Partidas Jogadas', 'PJPartidas jogadas')
vitoriasMinimo, vitoriasMaximo = criarSlider('Vitórias', 'VITVitórias')
empatesMinimo, empatesMaximo = criarSlider('Empates', 'EEmpates')
derrotasMinimo, derrotasMaximo = criarSlider('Derrotas', 'DERDerrotas')
golsMarcadosMinimo, golsMarcadosMaximo = criarSlider('Gols Marcados', 'GMGols marcados')
golsContraMinimo, golsContraMaximo = criarSlider('Gols Contra', 'GCGols contra')
saldoGolsMinimo, saldoGolsMaximo = criarSlider('Saldo de Gols', 'SGSaldo de gols')

# Aplicar filtros
if equipesSelecionadas:
    df = df[df['Equipe'].isin(equipesSelecionadas)]
df = df[(df['PtsPontos'] >= pontosMinimo) & (df['PtsPontos'] <= pontosMaximo)]
df = df[(df['PJPartidas jogadas'] >= partidasJogadasMinimo) & (df['PJPartidas jogadas'] <= partidasJogadasMaximo)]
df = df[(df['VITVitórias'] >= vitoriasMinimo) & (df['VITVitórias'] <= vitoriasMaximo)]
df = df[(df['EEmpates'] >= empatesMinimo) & (df['EEmpates'] <= empatesMaximo)]
df = df[(df['DERDerrotas'] >= derrotasMinimo) & (df['DERDerrotas'] <= derrotasMaximo)]
df = df[(df['GMGols marcados'] >= golsMarcadosMinimo) & (df['GMGols marcados'] <= golsMarcadosMaximo)]
df = df[(df['GCGols contra'] >= golsContraMinimo) & (df['GCGols contra'] <= golsContraMaximo)]
df = df[(df['SGSaldo de gols'] >= saldoGolsMinimo) & (df['SGSaldo de gols'] <= saldoGolsMaximo)]

# Exibir a tabela filtrada
st.dataframe(df)

# Criar gráficos interativos com plotly
st.subheader('Estatísticas')

# Pontos por equipe
figPontos = px.bar(df, x='Equipe', y='PtsPontos', title='Pontos por Equipe')
st.plotly_chart(figPontos)

# Gols marcados por equipe
figGolsMarcados = px.bar(df, x='Equipe', y='GMGols marcados', title='Gols Marcados por Equipe')
st.plotly_chart(figGolsMarcados)

# Gols contra por equipe
figGolsContra = px.bar(df, x='Equipe', y='GCGols contra', title='Gols Contra por Equipe')
st.plotly_chart(figGolsContra)

# Saldo de gols por equipe
figSaldoGols = px.bar(df, x='Equipe', y='SGSaldo de gols', title='Saldo de Gols por Equipe')
st.plotly_chart(figSaldoGols)

# Adicionar um chatbox para interação com o Gemini
st.subheader('Interaja com o Gemini')

# Entrada de texto do usuário
user_input = st.text_input("Digite sua pergunta:")

if st.button('Enviar'):
    # Gerar resposta usando a API do Gemini
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(user_input)
    
    # Exibir a resposta
    st.write("Resposta do Gemini:")
    st.write(response.text)