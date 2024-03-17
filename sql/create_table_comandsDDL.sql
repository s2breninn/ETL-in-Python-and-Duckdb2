create table vendas (
	venda_id SERIAL primary key,
	data_venda DATE not null,
	valor DECIMAL(10, 2) not null,
	quantidade INT not null,
	cliente_id INT not null,
	categoria VARCHAR(255) not NULL
);

create table vendas_calculado (
	venda_id SERIAL primary key,
	data_venda DATE not null,
	valor DECIMAL(10, 2) not null,
	quantidade INT not null,
	cliente_id INT not null,
	categoria VARCHAR(255) not null,
	total_vendas DECIMAL(10, 2) not NULL
);
