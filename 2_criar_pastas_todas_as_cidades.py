import pandas as pd
import os
import re

# Define as colunas do DataFrame
colunas = [
    'MÊS COMPETÊNCIA', 'MÊS REFERÊNCIA', 'UF', 'CÓDIGO MUNICÍPIO SIAFI',
    'NOME MUNICÍPIO', 'CPF FAVORECIDO', 'NIS FAVORECIDO', 'NOME FAVORECIDO',
    'VALOR PARCELA'
]

# Função para formatar o NIS
def format_nis(nis):
  return re.sub(r'(\d{1})(\d{3})(\d{3})(\d{3})(\d{1})', r'\1.\2.\3.\4-\5', nis)

# Função para remover ponto e zero do NIS
def remove_ponto_e_zero(nis):
    return nis[:-2]

# Lê o arquivo CSV com os dados do Bolsa Família
df = pd.read_csv('202312_NovoBolsaFamilia.csv', sep=';', encoding='latin-1', usecols=colunas)

# Renomeia as colunas
df = df.rename(columns={
    'MÊS REFERÊNCIA': 'mes',
    'UF': 'uf',
    'NOME MUNICÍPIO': 'municipio',
    'CPF FAVORECIDO': 'cpf',
    'NIS FAVORECIDO': 'nis',
    'NOME FAVORECIDO': 'nome',
    'VALOR PARCELA': 'val_parcela',
    
    })

# Converte a coluna NIS para string
df['nis'] = df['nis'].astype('str')

# Formata o NIS
df['nis'] = df['nis'].apply(format_nis)

# Remove ponto e zero do NIS
df['nis'] = df['nis'].apply(remove_ponto_e_zero)

# Remove colunas desnecessárias
df.drop(columns='MÊS COMPETÊNCIA', inplace=True)
df.drop(columns='CÓDIGO MUNICÍPIO SIAFI', inplace=True)
df.drop(columns='mes', inplace=True)

# Preenche valores nulos do CPF e NIS
df['cpf'].fillna('000.000.000-00', inplace=True)
df['nis'].fillna('0.000.000.000-0', inplace=True)

# Obtém a lista de estados
lista_de_estados = df['uf'].unique()

# Cria a pasta "dados_bolsa_familia" se ela não existir
os.makedirs('dados_bolsa_familia', exist_ok=True)

# Percorre a lista de estados
for estado in lista_de_estados:
    print(estado)
    # Cria a pasta do estado se ela não existir
    os.makedirs(f'dados_bolsa_familia/{estado}', exist_ok=True)

    # Filtra os dados do estado
    df_estado = df[df['uf'] == estado]

    # Obtém a lista de cidades
    lista_de_cidades = df_estado['municipio'].unique()

    # Salva a lista de cidades em um arquivo TXT
    with open('cidade_list.txt', 'a') as f:
        f.write(f'{lista_de_cidades,","}|')

    # Percorre a lista de cidades
    for cidade in lista_de_cidades:
        # Filtra os dados da cidade
        df_cidade = df_estado[df_estado['municipio'] == cidade]

        # Salva os dados da cidade em um arquivo CSV
        df_cidade.to_csv(f'dados_bolsa_familia/{estado}/{cidade}.csv', index=False)

# Exibe a mensagem de sucesso
print('Processamento concluído com sucesso!')
