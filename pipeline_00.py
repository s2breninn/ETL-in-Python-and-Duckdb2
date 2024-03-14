import os
import gdown # Download de arquivos no Gloogle Drive
import pandas as pd
from sqlalchemy import create_engine # Salvar no postgres
from dotenv import load_dotenv # Variáveis de ambientes

def baixar_arquivos_gloogle_drive(url, diretorio_local):
    os.makedirs(diretorio_local, exist_ok=True)
    gdown.download_folder(url, output=diretorio_local, quiet=False, use_cookies=False)

if __name__ == '__main___':
    url = 'https://drive.google.com/drive/folders/1WhdNw56xWZ8lCk5DSXoYh3R5uL1ZiGkR'
    diretorio_local = './folder_gdown'
    baixar_arquivos_gloogle_drive(url, diretorio_local)