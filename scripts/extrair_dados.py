import requests
import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = 'https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo'

parametros = {
    'an_exercicio': 2023,
    'nr_periodo': 6,
    'co_tipo_demonstrativo': 'RREO',
    'no_anexo': 'RREO-Anexo 01',
    'id_ente': 1302603
}

resposta = requests.get(url, params=parametros)
dados = resposta.json()

print('Status:', resposta.status_code)
print('Itens recebidos:', len(dados['items']))

nome_arquivo = 'rreo_manaus_2023_periodo6.json'
with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
    json.dump(dados['items'], arquivo, ensure_ascii=False, indent=2)

print('Arquivo salvo localmente:', nome_arquivo)

cliente = boto3.client(
    's3',
    endpoint_url='http://127.0.0.1:9000',
    aws_access_key_id=os.getenv('MINIO_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('MINIO_SECRET_KEY')
)

cliente.upload_file(nome_arquivo, 'siconfi-raw', nome_arquivo)

print('Arquivo enviado para o bucket siconfi-raw com sucesso!')
