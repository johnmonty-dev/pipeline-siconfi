import duckdb
import os
from dotenv import load_dotenv

load_dotenv()

con = duckdb.connect()

con.execute("INSTALL httpfs")
con.execute("LOAD httpfs")

print('Extensao httpfs instalada e carregada com sucesso')

con.execute("SET s3_endpoint='" + os.getenv("MINIO_ENDPOINT") + "'")
con.execute("SET s3_access_key_id='" + os.getenv("MINIO_ACCESS_KEY") + "'")
con.execute("SET s3_secret_access_key='" + os.getenv("MINIO_SECRET_KEY") + "'")
con.execute("SET s3_use_ssl=false")
con.execute("SET s3_url_style='path'")

print('Conexao com o MinIO configurada')

resultado = con.execute(
    "SELECT * FROM read_parquet('s3://siconfi-processed/rreo_manaus_2023_periodo6/*.parquet') LIMIT 10"
).fetchdf()

print('')
print('Resultado da consulta:')
print(resultado)
