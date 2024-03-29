import os
import gdown # Download de arquivos no Gloogle Drive
import duckdb
import pandas as pd
from sqlalchemy import create_engine # Salvar no postgres
from dotenv import load_dotenv # Variáveis de ambientes
from datetime import datetime
load_dotenv() # Carregando variáveis de ambientes

def conectar_banco():
    """Conecta ao banco de dados DuckDB, cria o banco se não existir"""
    return duckdb.connect(database='duckdb.db', read_only=False)

def inicializar_tabela(con):
    # Cria a tabela se ela não existir
    con.execute("""
                CREATE TABLE IF NOT EXISTS historico_arquivos(
                    nome_arquivo VARCHAR,
                    horario_processamento TIMESTAMP
                )
    """)

def registrar_arquivo(con, nome_arquivo):
    # Registrar um novo arquivo no bando de dados com o horário atual
    con.execute("""
                INSERT INTO historico_arquivos (nome_arquivo, horario_processamento)
                VALUES (?, ?)
    """, (nome_arquivo, datetime.now()))

def arquivos_processados(con):
    # Retornar um set  com os nomes de todos os arquivos já processados
    return set(row[0] for row in con.execute('SELECT nome_arquivo FROM historico_arquivos').fetchall())

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
    url = 'https://drive.google.com/drive/folders/1WhdNw56xWZ8lCk5DSXoYh3R5uL1ZiGkR'
    diretorio_local = './folder_gdown'
    #baixar_arquivos_gloogle_drive(url, diretorio_local)
    lista_de_arquivos = listar_arquivos_csv(diretorio_local)
    con = conectar_banco()
    inicializar_tabela(con)
    processados = arquivos_processados(con)

    for caminho_arquivo in lista_de_arquivos:
        nome_arquivo = os.path.basename(caminho_arquivo)
        if nome_arquivo not in processados:
            df_duckdb = ler_arquivos_csv(caminho_arquivo)
            df_pandas_transformado = transformar(df_duckdb) # Df em Duckdb transformado em Pandas
            salvar_no_postgres(df_pandas_transformado, 'vendas_calculado')
            registrar_arquivo(con, nome_arquivo)
            print(f'Arquivo {nome_arquivo} processado e salvo.')
        else:
            print(f'Arquivo {nome_arquivo} já foi processado anteriomente')