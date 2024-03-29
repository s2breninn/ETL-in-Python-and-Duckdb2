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
# DuckDB e Python para ETL

DuckDB é uma biblioteca leve e eficiente para processamento de dados em memória que suporta consultas SQL. Esta biblioteca tem ganhado popularidade no ecossistema de análise de dados em Python devido à sua rapidez e facilidade de uso.

## Por que usar DuckDB para ETL?

- **Desempenho excepcional**: DuckDB é otimizado para consultas analíticas e operações de ETL, oferecendo um desempenho excepcional mesmo com grandes volumes de dados.

- **Integração perfeita com Python**: Com uma interface Pythonic, DuckDB pode ser facilmente integrado em fluxos de trabalho existentes em Python, permitindo que os desenvolvedores usem suas habilidades em Python para processar e transformar dados.

- **Flexibilidade na manipulação de dados**: DuckDB suporta uma ampla gama de recursos SQL para manipulação de dados, tornando-o altamente flexível para realizar uma variedade de transformações durante o processo de ETL.

- **Portabilidade e facilidade de implantação**: DuckDB é uma biblioteca em memória e não requer uma configuração complexa de banco de dados, facilitando sua implantação e uso em diferentes ambientes.

- **Compatibilidade com outras ferramentas**: DuckDB é compatível com diversas ferramentas e bibliotecas de análise de dados em Python, como pandas e SQLAlchemy, tornando-o uma escolha versátil para integração em fluxos de trabalho existentes.  
---

## Descrição das Bibliotecas Utilizadas

- **gdown**: Esta biblioteca facilita o download de arquivos do Google Drive. Ela é útil quando você precisa baixar arquivos armazenados no Google Drive para o seu ambiente local.

- **duckdb**: DuckDB é um banco de dados em memória que suporta consultas SQL. Ele é conhecido por ser leve e rápido, tornando-o uma opção interessante para análise de dados em Python.

- **pandas**: pandas é uma biblioteca amplamente utilizada para análise de dados em Python. Ela oferece estruturas de dados flexíveis e eficientes para manipulação e análise de dados tabulares.

- **SQLAlchemy**: Esta biblioteca é uma abstração de banco de dados em Python que simplifica a interação com bancos de dados relacionais. Ela permite que você trabalhe com bancos de dados SQL usando uma interface Pythonic, facilitando tarefas como consultas, inserções e atualizações de dados.

- **dotenv**: dotenv é uma biblioteca que permite carregar variáveis de ambiente de um arquivo `.env` para o ambiente de execução do seu script Python. Isso é útil para configurar variáveis sensíveis, como credenciais de banco de dados, de forma segura e sem expô-las diretamente no código.

- **datetime**: datetime é um módulo padrão do Python que fornece classes para manipulação de datas e horas. Ele permite que você trabalhe com datas e horas de forma conveniente e eficaz em suas aplicações Python.

- **streamlit**: Streamlit é uma biblioteca para criação de aplicativos da web de maneira rápida e fácil com Python. É muito útil para criar painéis interativos e visualizações de dados diretamente a partir de scripts Python, sem a necessidade de conhecimento prévio em desenvolvimento web.


