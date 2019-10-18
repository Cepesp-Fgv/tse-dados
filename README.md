# TSE Dados

Esse projeto contém os códigos e análises para criação do CEPESPData (cepesp.io). O CEPESPData é um repositório que permite o acesso, de forma fácil e confiável, aos resultados e dados eleitorais. O CEPESPData permite a consulta e fácil visualização de resultados e dados eleitorais para todos os cargos, a partir de diferentes agregações geográficas (Brasil, UF, município, micro-região, entre outras), de 1998 a 2014. 

Além de facilitar o acesso aos dados eleitorais, temos o objetivo de criar um repositório aberto e transparente. Dessa forma, nossos códigos, análises e testes de consistências dos dados estão disponíveis neste repositório. Estamos desenvolvendo também, um R API (https://github.com/Cepesp-Fgv/cepesp-r), Python API (https://github.com/Cepesp-Fgv/cepesp-python) e Rest API (https://github.com/Cepesp-Fgv/cepesp-rest) para auxiliar na consulta dos dados no nosso repositório a partir de liguagens de programação.

Sugestões, correções e demais contribuições são bem-vidas.

## Pré-requisitos
- Python 3.6 ou mais recente

## Instalação

Primeiro, você precisa instalar a ferramenta [virtualenv](https://virtualenv.pypa.io/en/latest/installation/)
```bash
pip install virtualenv
```

E então, criar um ambiente virtual.
```bash
cd /caminho/para/o/tse-dados
virtualenv .venv --python=python3
```

Para ativar o seu ambiente virtual recém criado:

- No Linux/MacOS:
    ```bash
    source .venv/bin/activate
    ```
- No Windows:
    ```bash
    ./.venv/Scripts/activate
    ```

Instale os módulos requeridos pelo sistema.
```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` e edite-o
```bash
cp .env.example .env
```

Pronto! Agora já pode iniciar a aplicação

## Running Web Server
```bash
FLASK_APP=web/application.py python -m flask run
```

## Running ETL
First, edit the `etl/config.py` with the necessary options
```bash
python -c "from etl.run import run; run()"
```

### Fonte Original dos Dados:

Muitos dos dados originais utilizados aqui podem ser encontrados em no Repositório de Dados do TSE: http://www.tse.jus.br/eleicoes/estatisticas/repositorio-de-dados-eleitorais

### Wiki

 - [Estrutura do Projeto](https://github.com/Cepesp-Fgv/tse-dados/wiki/Estrutura)
 - [Seletores de Colunas](https://github.com/Cepesp-Fgv/tse-dados/wiki/Colunas)
   - [Eleições por Cargo](https://github.com/Cepesp-Fgv/tse-dados/wiki/Colunas#reposit%C3%B3rio-elei%C3%A7%C3%B5es-por-cargo-libtsecolumnspy)
   - [Resultados da Eleição](https://github.com/Cepesp-Fgv/tse-dados/wiki/Colunas#reposit%C3%B3rio-resultados-da-elei%C3%A7%C3%A3o-libvotoscolumnspy)
   - [Candidatos](https://github.com/Cepesp-Fgv/tse-dados/wiki/Colunas#reposit%C3%B3rio-candidatos-libcandidatoscolumnspy)
   - [Legendas](https://github.com/Cepesp-Fgv/tse-dados/wiki/Colunas#reposit%C3%B3rio-legendas-liblegendascolumnspy)
 - [Leitores de Dados](https://github.com/Cepesp-Fgv/tse-dados/wiki/Leitores)
   - [Caching](https://github.com/Cepesp-Fgv/tse-dados/wiki/Leitores#caching)
 - [Correções em Pré-Processamento](https://github.com/Cepesp-Fgv/tse-dados/wiki/Corre%C3%A7%C3%B5es-em-Pr%C3%A9-Processamento)
   - [Adicionar Cargos Extras (2014)](https://github.com/Cepesp-Fgv/tse-dados/wiki/Corre%C3%A7%C3%B5es-em-Pr%C3%A9-Processamento#adicionar-cargos-extras-2014)
   - [Correção Descrição Eleição (2014)](https://github.com/Cepesp-Fgv/tse-dados/wiki/Corre%C3%A7%C3%B5es-em-Pr%C3%A9-Processamento#corre%C3%A7%C3%A3o-descri%C3%A7%C3%A3o-elei%C3%A7%C3%A3o-2014)
   - [Correção Descrição Eleição (2010)](https://github.com/Cepesp-Fgv/tse-dados/wiki/Corre%C3%A7%C3%B5es-em-Pr%C3%A9-Processamento#corre%C3%A7%C3%A3o-descri%C3%A7%C3%A3o-elei%C3%A7%C3%A3o-2010)
   - [Padronização do Código Situação Turno](https://github.com/Cepesp-Fgv/tse-dados/wiki/Corre%C3%A7%C3%B5es-em-Pr%C3%A9-Processamento#padroniza%C3%A7%C3%A3o-do-c%C3%B3digo-situa%C3%A7%C3%A3o-turno)
   - [Corrigir Sequencia Coligação (2014)](https://github.com/Cepesp-Fgv/tse-dados/wiki/Corre%C3%A7%C3%B5es-em-Pr%C3%A9-Processamento#corrigir-sequencia-coliga%C3%A7%C3%A3o-2014)
   - [Corrigir Sequencia Coligação (2010)](https://github.com/Cepesp-Fgv/tse-dados/wiki/Corre%C3%A7%C3%B5es-em-Pr%C3%A9-Processamento#corrigir-sequencia-coliga%C3%A7%C3%A3o-2010)
   - [Corrigir Código Cor Raça](https://github.com/Cepesp-Fgv/tse-dados/wiki/Corre%C3%A7%C3%B5es-em-Pr%C3%A9-Processamento#corrigir-c%C3%B3digo-cor-ra%C3%A7a)
   - [Corrigir Email Candidato](https://github.com/Cepesp-Fgv/tse-dados/wiki/Corre%C3%A7%C3%B5es-em-Pr%C3%A9-Processamento#corrigir-email-candidato)
