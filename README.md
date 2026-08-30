# Pipeline de Dados Contábeis, arquitetura Data Lake simulada localmente

**Stack:** Python, PySpark, DuckDB, MinIO (S3 local), SICONFI API, Power BI

Esse projeto simula uma arquitetura completa de Data Lake usando os dados públicos e reais do SICONFI, o sistema de informações contábeis do Tesouro Nacional. A ideia original era montar isso direto na AWS, usando S3, Glue e Athena, mas como não queria correr risco de gastar dinheiro à toa enquanto estava aprendendo, resolvi simular tudo localmente com ferramentas open source que fazem praticamente a mesma coisa.

## Como funciona, do começo ao fim

```
API do SICONFI, dados de Manaus  →  Extração em Python  →  Camada Raw (MinIO)  →  Transformação com PySpark  →  Camada Processed em Parquet (MinIO)  →  Consulta com SQL (DuckDB)  →  Power BI
```

1. Busco os dados do RREO (Relatório Resumido da Execução Orçamentária) de Manaus direto na API pública do Tesouro Nacional, sem precisar de cadastro nem chave de acesso.
2. Salvo esse retorno bruto num bucket chamado `siconfi-raw`, que fica dentro do MinIO, um programa que roda no meu próprio computador e imita o comportamento do Amazon S3.
3. Uso o PySpark para ler esse arquivo, escolher só as colunas que interessam e converter o valor de texto para número de verdade.
4. Salvo o resultado tratado no formato Parquet e mando para outro bucket, o `siconfi-processed`.
5. Consulto esses dados com SQL usando o DuckDB, que consegue ler os arquivos Parquet direto do MinIO, do mesmo jeito que o Amazon Athena faria com o S3 de verdade.
6. Por fim, conecto o Power BI direto nos arquivos Parquet para montar as visualizações.

## Por que fiz do jeito local em vez de usar a AWS de verdade

Confesso que pensei bastante nisso. A AWS até dá um crédito bom pra quem cria conta nova, mas queria ter certeza absoluta de não gastar nada enquanto ainda estou testando e aprendendo. Então troquei os serviços pagos por equivalentes gratuitos que fazem exatamente o mesmo papel na arquitetura:

- No lugar do Amazon S3, uso o MinIO, que roda local e fala a mesma língua do S3.
- No lugar do AWS Glue, uso o PySpark instalado direto no meu computador, sem custo de processamento na nuvem.
- No lugar do Amazon Athena, uso o DuckDB, que consulta os arquivos Parquet com SQL puro, rápido e sem custo por consulta.

O legal disso é que a lógica e as ferramentas de código são praticamente as mesmas que eu usaria numa empresa de verdade. Se um dia eu quiser migrar isso pra AWS de verdade, é basicamente trocar os endereços de conexão, o resto do código continua igual.

## Um perrengue no meio do caminho

O PySpark no Windows depende de um arquivo chamado winutils.exe pra funcionar direito, mesmo processando só arquivos locais, sem nuvem nenhuma envolvida. Sem isso, ele quebra com um erro bem confuso de Java. Descobri isso na prática, tomando um erro depois de já ter processado os dados uma vez com sucesso (só que numa sessão diferente do terminal, onde a configuração não persistiu). Resolvi configurando a variável HADOOP_HOME de forma permanente no Windows, apontando pra pasta com o winutils, e depois disso nunca mais deu problema.

## O que o projeto já entrega

- Extração automática de dados reais e públicos de finanças municipais.
- Um Data Lake simulado com camada bruta e camada tratada, separadas em buckets diferentes.
- Transformação de dados usando processamento distribuído de verdade (PySpark), não só pandas simples.
- Consulta SQL direto em cima de arquivos Parquet guardados como se fossem num S3.
- Um dashboard no Power BI mostrando receitas e despesas do município de Manaus.

## Como rodar na sua máquina

Você vai precisar ter instalado antes: Python, Java (17 ou mais recente) e o Power BI Desktop, se quiser montar o dashboard.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Depois é baixar o executável do MinIO (o link direto está nos comentários do script `testar_minio.py`) e subir o servidor local com:

```bash
.\minio\minio.exe server .\minio_data --console-address ":9001"
```

Com o MinIO no ar, é só rodar os scripts na ordem: `extrair_dados.py`, depois `transformar_dados.py`, e por fim `consultar_dados.py` pra ver a consulta SQL funcionando.

## O que eu penso em melhorar futuramente

- Trazer mais de um período e mais de um município, pra dar pra comparar dados ao longo do tempo.
- Automatizar isso pra rodar sozinho sem eu precisar disparar cada script na mão.
- Um dia, testar migrar essa mesma lógica pra AWS de verdade, usando o crédito gratuito que eles dão pra conta nova.
- Melhorar o dashboard do Power BI, hoje ainda é bem simples, só uma tabela de teste.
