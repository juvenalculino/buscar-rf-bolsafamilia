from utils import format_nis, remove_pontuacao, load_data, pd, st
from utils import carregar_estados, carregar_unipessoal
from threading import Thread
from streamlit_option_menu import option_menu


selected = option_menu(
    menu_title = "MENU",
    options=["BENÉFICIOS", "UNIPESSOAL"],
    icons=['house', 'book'],
    menu_icon='cast',
    default_index=1,
    orientation='horizontal',
    styles={
    "container": {"margin": "0px !important", "padding": "0!important", "align-items": "stretch", "background-color": "#fafafa"},
    "icon": {"color": "black", "font-size": "20px"}, 
    "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
    "nav-link-selected": {"background-color": "green", "font-size": "20px", "font-weight": "bold", "color": "black", },


    }
)


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
    

if selected == 'BENÉFICIOS':
    # Obter as chaves do dicionário
    chaves = list(estados.keys())

    # Criar a rádio
    estado = st.selectbox('Selecione um estado:', chaves, index=4)

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
                    use_container_width=True,
                    )



if selected == 'UNIPESSOAL':
    caminho_arquivo = carregar_unipessoal(f'unipessoal/unipessoal.csv')
    caminho_arquivo['cod_familiar'] = caminho_arquivo["cod_familiar"].astype('str')
    nome_cpf = st.text_input("Nome, cpf ou endereço: ").upper()



    def buscar_por_nome_cpf_endereco(df, valor):
        return df.loc[(df['nome'].str.contains(remove_pontuacao(valor))) |
                    (df['cpf'].str.contains(remove_pontuacao(valor))) |
                    (df['endereco'].str.contains(remove_pontuacao(valor)))]
    # Realizar a busca
    df_busca = buscar_por_nome_cpf_endereco(caminho_arquivo.copy(), nome_cpf)
   
    st.dataframe(df_busca)
