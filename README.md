# fipe-api

Sistema para consulta de modelos de veículos de carros presentes na tabela FIPE.
Para os usuários as principais funcionalidades são:
1. Disparar a carga inicial ou atualização dos dados;
2. Listar as marcas de todos os veículos;
3. Listar todos oos modelos de veículos de uma marca específica;
4. Adicionar/editar os campos `modelo e observações` de um veículo.

#### *Observação*
```
Quando a pessoa responsável pela avaliação for testar a aplicação, o banco de dados estará limpo e será
necessário disparar a carga inicial dos dados para popular o banco. Detalhes mais abaixo.
```


## Execução utilizando a aplicação em produção hospedada no GCP

 - API-1: `https://api-1-6cu7fqvgrq-rj.a.run.app/docs/`
 - API-2: `https://api-2-6cu7fqvgrq-rj.a.run.app/docs/` 

O deploy da aplicação em produção foi feita usando os serviços do Cloud Build e Cloud Run. 

De forma bem resumida, o Cloud Build foi configurado para ser executado sempre que houver uma modificação na branch `master` do
repositório no github. Como esta descrito no arquivo `cloudbuild.yaml` na raiz do projeto, é criada um
imagem docker para API-1 e outra para API-2 e são armazenadas no serviço `Artifact Registry`. 
Após criar as imagens o Cloud Build realiza o deploy de cada API no serviço do Cloud Run passando as configurações correspondentes.
Dessa forma, temos a API-1 e API-2 sendo executas em instâncias do google e disponíveis para acesso por qualquer pessoa. 

Para realiza a comunicação entre as 2 API's foi utilizado o serviço Cloud Tasks, onde a API-1 cria tasks do tipo `http_request`
com destino para API-2 e essas requests são disparadas de forma assíncrona. 

E na API-2 quando recebe essas requests feitas pelo Cloud Tasks, realiza todo o processamento e salva os dados no `Firestore`, que
é um banco de dados NoSQL do google. 

Sendo assim, toda aplicação incluindo a hospedagem das 2 API's, sistema de filas e banco de dados estão rodando no GCP.


## Pré-requisitos para execução local

Certifique-se de ter instalado os seguintes requisitos antes de executar o projeto:

- Docker
- Docker Compose
- Make


## Instalação

1. Clone o repositório:

   ```bash
   git clone git@github.com:Augusto94/fipe-api.git
   ```

2. Acesse o diretório do projeto:

    ```bash
    cd fipe-api
    ```

3. Execute o comando do Docker Compose para construir e iniciar o projeto:

    ```bash
    docker-compose up
    ```
    ou
    ```bash
    make start
    ```

Nesse momento as API's estarão disponíveis em `http://localhost:8000/` e `http://localhost:8001/`.

Localmente são utilizadas outras ferramentas para armazenamento dos dados e o sistema de filas e comunicação entre as API's. 

Em produção o banco de dados utilizado é o `Firestore`. Já no ambiente de desenvolvimento o banco escolhido foi o `MongoDB`. 
Já o sistema de filas adotado foi o `Redis` ao invés do `Cloud Tasks`. Onde a API-1 envia mensagens contendo as informações das marcas para uma fila no redis e
um serviço terceiro, chamado de `consumer` fica monitorando essa fila e a cada nova mensagem realiza a chamada para a API-2 realizar a
criação dos veículos. 

Em resumo o funcionamento da aplicação é o mesmo mas as ferramentas de banco de dados e fila são diferentes dependendo do ambiente (local ou prod.)


## Explicação das API's
Por definição do desafio teste, 2 API's foram criadas para manipular os dados.
As API's foram criadas utilizando o framework FastAPI.
1. API-1: Possui os endpoints para realizar a carga inicial dos dados e ler as marcas e os dados dos veículos;
2. API-2: Possui os endpoints para criação e atualização dos dados. 


De forma simples, a API-1 é utilizada para leitura dos dados e a API-2 para criação e edição. 

A fonte dos dados utilizadas para popular a nossa base de dados se encontra em: `https://deividfortuna.github.io/fipe/`.
Basicamente, ao chamado o endpoint  GET `/atualizar-dados` a API-1 realiza uma request na api externa para buscar a lista das marcas dos veículos na tabela FIPE.
Os veículos podem ser `carros, motos ou caminhoes`. A API-1 consulta as marcas nessas 2 categorias. 

Em posse dos resultados, para cada marca, a API-1 envia as informações de `codigo, nome e categoria` para uma fila e
de forma assíncrona as mensagens que chegam na fila realizam uma request para o endpoint de criação de veículo na API-2. 

Agora na API-2, o endpoint de criação de veículos recebe as informações que foram enviadas para fila pela API-1 e em posse
dessas informações das marcas, realiza uma request para a api externa para consultar os modelos de veículos daquela marca
espefícificada. 

Ao receber o retorno da API externa prepara os dados e salva em um banco de dados NoSQL. Nesse momento já teremos no
nosso banco os dados de veículos prontos para serem consultados. Um exemplo de veículo salvo no banco de dados, pela API-2, é:
```json
{
    "observacoes": "",
    "modelo": "Q3 Prestige 2.0 TFSI Tiptr.Quatro ",
    "codigo": "10111",
    "categoria": "carros",
    "marca": "Audi"
}
```

No endpoint GET `/marcas` da API-1 é possível obter a lista das marcas dos veículos, de forma ordenada, que existem na nossa base. 
Um exemplo de response JSON é:
```json
[
  "AM Gen",
  "ASTON MARTIN",
  "Acura",
  "Agrale",
  "Alfa Romeo",
  "Asia Motors",
  "Audi",
  "BMW",
  "BRM",
  "BYD"
]
```
E no endpoint GET `/veiculos/{marca}` da API-1 é possível obter a lista de veículos de uma marca específica.
Um exemplo de response JSON é:
```json
[
  {
    "codigo": "100",
    "modelo": "A6 2.4 30V Mec",
    "observacoes": "",
    "categoria": "carros",
    "marca": "Audi"
  },
  {
    "observacoes": "",
    "modelo": "Q5 Perf. Black 2.0 TFSIe S.Tr. Qt (Hib.)",
    "codigo": "10045",
    "categoria": "carros",
    "marca": "Audi"
  },
  {
    "observacoes": "",
    "modelo": "Q5 Performance 2.0 TFSIe S.Tr. Qt (Hib.)",
    "codigo": "10046",
    "categoria": "carros",
    "marca": "Audi"
  }
]
```

Agora, voltando na API-2, é possível realizar a atualização de 2 campos de um veículo: `modelo e observacoes`.
No endpoint PUT `/veiculo` da API-2 é possível realizar a atualização de um veículo.
Um exemplo do body de uma request para esse endpoint é:
```json
{
  "codigo": "100",
  "observacoes": "Esse veículo é maravilhoso!"
}
```

E um exemplo de response JSON para essa request é:
```json
{
    "codigo": "100",
    "modelo": "A6 2.4 30V Mec",
    "observacoes": "Esse veículo é maravilhoso!",
    "categoria": "carros",
    "marca": "Audi"
}
```

## Organização do projeto

Por se tratar de 2 API's FastAPI que compartilham de vários recursos, foi tomado um grande cuidado para evitar
repetições de código e/ou arquivos. 

Dockerfile, docker-compose.yml, dependências pelo poetry, cloudbuild.yaml, entre outros recursos, são os mesmos
para as 2 API's. Database, logger, constant, etc, foram inseridos em uma pasta chamada `common` e podem ser facilmente
acessada por ambas API's. 

Os projetos FastAPI foram organizados utilizando o padrão service-repository onde ficam bem definidas as responsabilidades
de lógica de negócio (service) e comunicação e manipulação no banco de dados (repository) possibilidando possa crescer 
de forma organizada. 

Foi feito uso do pre-commit para padronização e garantir uma qualidade no código. Também foi utilizado type hint e escrita de
docstrings no padrão do google nas funções, facilitando o entendimento do código. 

Também foram implementados testes unitários e de integração usando o pytest. 


# Testes

Para executar os testes automatizados, utilize o seguinte comando:
```bash
docker-compose run --rm app pytest --cov --cov-report term-missing --cov-fail-under 90 --disable-pytest-warnings
```
ou simplesmente:
```bash
make test
```

## Observações e análise do projeto

#### *Stask das principais tecnologias/serviços utilizados*
 - FastAPI
 - Cloud Build
 - Cloud Run
 - Cloud Tasks
 - Firestore/Firebase
 - MongoDB
 - Redis
 - Docker
 - Docker Compose
 - Pytest
 - Poetry
 - pre-commit

#### Possíveis melhorias

 - Melhorar os teste e adicionar sua execução como um step cloud build para subir para produção somente códigos que passam nos testes.
 - Fazer o deploy da aplicação usando kubernetes possibilidando uma maior gerenciamento, escalabilidade, resiliência e vários outros benefícios do kubernetes.
 - Adicionar algumas verificações nas API's para evitar respostas inesperadas. Melhorar os testes pode ajudar nesse ponto.
 - Utilizar a mesmas tecnologias e ferramentas independente do ambiente.


## Contato

`email`: **augustoarl@gmail.com** 

`redes sociais`: **@augustoarl**
