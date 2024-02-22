from utils import format_nis, remove_pontuacao, load_data, pd, st
from utils import carregar_estados
from threading import Thread

maxMessageSize = 5000
st.set_page_config(
    page_title='BUSCAR RF',
    layout='wide',
    page_icon=':copyright:',
    initial_sidebar_state='collapsed'
)

html_temp = '''
    <div style="background-color:tomato;padding:15px; text-align:center">
    <h1>BUSCAR RF</h1>

    </div>
    <br>
    <style>
    
    </style>
    '''
st.markdown(html_temp, unsafe_allow_html=True)

# carregar dicionario json
estados = carregar_estados()

class BuscaThread(Thread):
    def __init__(self, nome_nis):
        super().__init__()
        self.nome_nis = nome_nis
        self.df_busca = None

    def run(self):
        self.df_busca = buscar_dados(self.nome_nis)

    def get_result(self):
        return self.df_busca

# Obter as chaves do dicionário
chaves = list(estados.keys())

# Criar a rádio
estado = st.radio('Selecione um estado:', chaves, index=4, horizontal=True)

# Exibir o estado selecionado
estado_selecionado = estados[estado]

municipio = st.selectbox('Selecione um município:', estado_selecionado)
caminho_arquivo = f'dados_bolsa_familia/{estado}/{municipio}.csv'
    # Abrir o arquivo da cidade
df_cidade = load_data(caminho_arquivo)


def buscar_dados(nome_nis):
   return df_cidade.loc[(df_cidade['nome'].str.contains(remove_pontuacao(nome_nis))) | (df_cidade['nis'].str.contains(format_nis(nome_nis)))]


if municipio:
    # Adicionar um campo de texto para o nome ou número do NIS
    nome_nis = st.text_input("Nome ou número do NIS:").upper()

    # Cria um objeto BuscaThread
    thread = BuscaThread(nome_nis)

    # Inicia o thread
    thread.start()

    # Espera o thread terminar
    thread.join()

    # Obtém o resultado da busca
    df_busca = thread.get_result()
  
    st.dataframe(
        df_busca,
                  use_container_width=True, hide_index=True,
                 )