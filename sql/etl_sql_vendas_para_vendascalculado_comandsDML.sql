-- ETL em SQL:
INSERT INTO vendas_calculado (data_venda, valor, quantidade, cliente_id, categoria, total_vendas)
SELECT data_venda, valor, quantidade, cliente_id , categoria , (valor * quantidade) as total_vendas 
FROM vendas;