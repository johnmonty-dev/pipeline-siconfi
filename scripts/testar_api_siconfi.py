import requests

url = 'https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo'

parametros = {
    'an_exercicio': 2023,
    'nr_periodo': 6,
    'co_tipo_demonstrativo': 'RREO',
    'no_anexo': 'RREO-Anexo 01',
    'id_ente': 1302603
}

resposta = requests.get(url, params=parametros)

print('Status da requisicao:', resposta.status_code)

dados = resposta.json()

print('Chaves do JSON retornado:', dados.keys())
print('Quantidade de itens:', len(dados['items']))
print('')
print('Primeiro item:')
print(dados['items'][0])
