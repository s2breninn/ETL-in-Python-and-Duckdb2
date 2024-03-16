import os
import gdown # Download de arquivos no Gloogle Drive
import duckdb
import pandas as pd
from sqlalchemy import create_engine # Salvar no postgres
from dotenv import load_dotenv # Variáveis de ambientes
load_dotenv() # Carregando variáveis de ambientes

def baixar_arquivos_gloogle_drive(url, diretorio_local):
    os.makedirs(diretorio_local, exist_ok=True)
    gdown.download_folder(url, output=diretorio_local, quiet=False, use_cookies=False)

# Função para listar arquivos CSV no diretório especificado
def listar_arquivos_csv(diretorio):
    arquivos_csv = []
    todos_arquivos = os.listdir(diretorio)
    for arquivo in todos_arquivos:
        if arquivo.endswith('.csv'):
            caminho_completo = os.path.join(diretorio, arquivo)
            arquivos_csv.append(caminho_completo)
    return arquivos_csv

# Funcão para ler arquivos CSV e retornar um DataFrame do duckdb
def ler_arquivos_csv(caminho_arquivo):
    return duckdb.read_csv(caminho_arquivo)

# Função para adicionar uma coluna de total de vendas 
def transformar(df):
    # Executa a consulta SQL que inclui a nova coluna, aperando sobre a tabela virtual
    df_transformado = duckdb.sql("SELECT *, quantidade * valor AS total_vendas FROM df").df()
    # Remove registro da tabela virtual para limpeza
    return df_transformado

def salvar_no_postgres(df_pandas_transformado, tabela):
    DATABASE_URL = os.getenv('DATABASE_URL') #  Url do database
    engine = create_engine(DATABASE_URL)
    # Salvar o DataFrame no PostgresSQL
    df_pandas_transformado.to_sql(tabela, con=engine, if_exists='append', index=False)

if __name__ == '__main__':
    try:
        url = 'https://drive.google.com/drive/folders/1WhdNw56xWZ8lCk5DSXoYh3R5uL1ZiGkR'
        diretorio_local = './folder_gdown'
        #baixar_arquivos_gloogle_drive(url, diretorio_local)
        lista_de_arquivos = listar_arquivos_csv(diretorio_local)
        for caminho_arquivo in lista_de_arquivos:
            df_duckdb = ler_arquivos_csv(caminho_arquivo)
            df_pandas_transformado = transformar(df_duckdb) # Df em Duckdb transformado em Pandas
            salvar_no_postgres(df_pandas_transformado, 'vendas_calculado')
    except Exception as e:
        print(f'{e}: Erro de conexão')