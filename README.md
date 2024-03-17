# ETL-in-Python-and-Duckdb2

![Ilustração e anotações sobre ETL do projeto](./etl_project.png)

## Processos e Requisitos de Desenvolvimento do ETL

1. **Baixar arquivos do Google Drive**
2. **Listar arquivos no diretório**
3. **Checar tipo do arquivo**
    - **CSV:** Ler arquivo CSV
    - **JSON:** Ler arquivo JSON
    - **Parquet:** Ler arquivo Parquet
4. **Transformar em DataFrame**
5. **Checar se o arquivo foi processado**
    - Se sim, Fim do processamento do arquivo
    - Se não:
        - Salvar no PostgreSQL
        - Registrar arquivo como processado
        - Fim do processamento do arquivo

---

## Descrição das Bibliotecas Utilizadas

- **gdown:** Biblioteca para download de arquivos do Google Drive. É importante notar que podem ocorrer erros de solicitação ao se conectar ao Google devido ao bloqueio de algumas requisições. Para uma melhor performance e para códigos de produção, recomenda-se utilizar a API oficial do Google.

