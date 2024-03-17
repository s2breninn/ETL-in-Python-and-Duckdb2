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
def listar_arquivos_e_tipos(diretorio):
    # Listar arquivos e identifica se são CSV, JSON ou Parquet
    """Lista arquivos e identifica se são CSV, JSON ou Parquet."""
    arquivos_e_tipos = []
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".csv") or arquivo.endswith(".json") or arquivo.endswith(".parquet"):
            caminho_completo = os.path.join(diretorio, arquivo)
            tipo = arquivo.split(".")[-1]
            arquivos_e_tipos.append((caminho_completo, tipo))
    return arquivos_e_tipos

# Funcão para ler e checar os tipos de arquivos
def ler_arquivos(caminho_arquivo, tipo):
    # Ler arquivo com o seu tipo e retorna em DataFrame
    if tipo == 'csv':
        return duckdb.read_csv(caminho_arquivo)
    elif tipo == 'json':
        return duckdb.read_json(caminho_arquivo)
    elif tipo == 'parquet':
        return duckdb.read_parquet(caminho_arquivo)
    else:
        raise ValueError(f'Tipo de arquivo não suportado: {tipo}')

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

def pipeline():
    url = 'https://drive.google.com/drive/folders/1WhdNw56xWZ8lCk5DSXoYh3R5uL1ZiGkR'
    diretorio_local = './folder_gdown'
    baixar_arquivos_gloogle_drive(url, diretorio_local)
    con = conectar_banco()
    inicializar_tabela(con)
    processados = arquivos_processados(con)
    arquivos_e_tipos = listar_arquivos_e_tipos(diretorio_local)

    logs = []
    for caminho_arquivo, tipo in arquivos_e_tipos:
        nome_arquivo = os.path.basename(caminho_arquivo)
        if nome_arquivo not in processados:
            df = ler_arquivos(caminho_arquivo, tipo)
            df_transformado = transformar(df) # Df em Duckdb transformado em Pandas
            salvar_no_postgres(df_transformado, 'vendas_calculado')
            registrar_arquivo(con, nome_arquivo)
            logs.append(f'Arquivo {nome_arquivo} processado e salvo.')
        else:
            logs.append(f'Arquivo {nome_arquivo} já foi processado anteriomente')
    
    return logs

if __name__ == '__main__':
    pipeline()