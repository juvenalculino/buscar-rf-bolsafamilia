import pandas as pd 
import re
import datetime
#colunas = ["cpf", "nome", "nascimento", "rua", "numero", "complemento", "bairro", "cep",  "municipio", "uf", "mae"]


carregar = pd.read_csv('202312_NovoBolsaFamilia.csv', sep=';', encoding='latin-1')

lista_de_estados = carregar['UF'].unique()

def format_nis(nis):
  return re.sub(r'(\d{1})(\d{3})(\d{3})(\d{3})(\d{1})', r'\1.\2.\3.\4-\5', nis)

def remove_ponto_e_zero(nis):
    return nis[:-2]

for estado in lista_de_estados:
    df_estado = carregar[carregar['UF'] == estado]
    df_estado = df_estado.rename(columns={
    'MÊS REFERÊNCIA': 'mes',
    'UF': 'uf',
    'NOME MUNICÍPIO': 'municipio',
    'CPF FAVORECIDO': 'cpf',
    'NIS FAVORECIDO': 'nis',
    'NOME FAVORECIDO': 'nome',
    'VALOR PARCELA': 'val_parcela',
    
    })   
    df_estado['nis'] = df_estado['nis'].astype('str')
    df_estado['nis'] = df_estado['nis'].apply(format_nis)
    df_estado['nis'] = df_estado['nis'].apply(remove_ponto_e_zero)
    df_estado.drop(columns='MÊS COMPETÊNCIA', inplace=True)
    df_estado.drop(columns='CÓDIGO MUNICÍPIO SIAFI', inplace=True)
    df_estado.drop(columns='mes', inplace=True)
    df_estado.drop(columns='val_parcela', inplace=True)
    df_estado['cpf'].fillna('000.000.000-00', inplace=True)
    df_estado['nis'].fillna('0.000.000.000-0', inplace=True)
    

    # Aplicar a função ao DataFrame
    
    print(df_estado)
    df_estado.to_csv(f'bolsa_familia_estado_{estado}.csv', index=False)
             
"""
alterar_dados = {
    'mes': carregar['MÊS REFERÊNCIA'],
    'uf': carregar['UF'],
    'cod_siafi': carregar['CÓDIGO MUNICÍPIO SIAFI'],
    'municipio': carregar['NOME MUNICÍPIO'],
    'cpf': carregar['CPF FAVORECIDO'].fillna('000.000.000-00'),
    'nis': carregar['NIS FAVORECIDO'].fillna("0000000000.0"),
    'nome': carregar['NOME FAVORECIDO'],
    'parcela': carregar['VALOR PARCELA'],
}

df = pd.DataFrame(alterar_dados)
print(df)

"""

'''
# Calcular a quantidade de nan em um dataframe - print(df.isna().sum())

carregar['MÊS REFERÊNCIA']
#carregar['MÊS COMPETÊNCIA']
carregar['UF']
carregar['CÓDIGO MUNICÍPIO SIAFI']
carregar['NOME MUNICÍPIO']
carregar['CPF FAVORECIDO']
carregar['NIS FAVORECIDO']
carregar['NOME FAVORECIDO']
carregar['VALOR PARCELA']


# Use ffill() instead of fillna() with method='ffill'
df = pd.DataFrame(dados_teste)

pegar_bahia = df[df['estado'] == 'BA']
#pegar_fatima = pegar_bahia[pegar_bahia['municipio'] == "FATIMA"]
#pegar_fatima.to_csv('fatima.csv', index=False)
pegar_bahia.to_csv('dados_sus_ba.csv', index=False)'''

