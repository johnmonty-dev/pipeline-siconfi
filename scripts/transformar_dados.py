import boto3
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os
from dotenv import load_dotenv

load_dotenv()

cliente = boto3.client(
    's3',
    endpoint_url='http://127.0.0.1:9000',
    aws_access_key_id=os.getenv('MINIO_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('MINIO_SECRET_KEY')
)

nome_arquivo = 'rreo_manaus_2023_periodo6.json'
caminho_raw = 'raw/' + nome_arquivo

cliente.download_file('siconfi-raw', nome_arquivo, caminho_raw)

print('Arquivo baixado da camada raw:', caminho_raw)

spark = SparkSession.builder.appName('TransformaSiconfi').getOrCreate()

df = spark.read.json(caminho_raw, multiLine=True)

print('')
print('Esquema dos dados:')
df.printSchema()

print('Primeiras linhas:')
df.show(5)

df_transformado = df.select(
    col('exercicio'),
    col('periodo'),
    col('instituicao'),
    col('cod_ibge'),
    col('uf'),
    col('rotulo'),
    col('coluna'),
    col('conta'),
    col('valor').cast('double')
)

print('')
print('Dados transformados:')
df_transformado.show(10, truncate=False)

pasta_local_parquet = 'processed/rreo_manaus_2023_periodo6'

df_transformado.write.mode('overwrite').parquet(pasta_local_parquet)

print('')
print('Parquet salvo localmente em:', pasta_local_parquet)

for raiz, pastas, arquivos in os.walk(pasta_local_parquet):
    for arquivo in arquivos:
        caminho_completo = os.path.join(raiz, arquivo)
        caminho_relativo = os.path.relpath(caminho_completo, 'processed')
        chave_s3 = caminho_relativo.replace('\\', '/')
        cliente.upload_file(caminho_completo, 'siconfi-processed', chave_s3)
        print('Enviado para o bucket:', chave_s3)
