# TSE Dados

Esse projeto contém os códigos e análises para criação do CEPESPData (cepesp.io). O CEPESPData é um repositório que permite o acesso, de forma fácil e confiável, aos resultados e dados eleitorais. O CEPESPData permite a consulta e fácil visualização de resultados e dados eleitorais para todos os cargos, a partir de diferentes agregações geográficas (Brasil, UF, município, micro-região, entre outras), de 1998 a 2014. 

Além de facilitar o acesso aos dados eleitorais, temos o objetivo de criar um repositório aberto e transparente. Dessa forma, nossos códigos, análises e testes de consistências dos dados estão disponíveis neste repositório. Estamos desenvolvendo também, um R API (https://github.com/Cepesp-Fgv/cepesp-r) e Python API (https://github.com/Cepesp-Fgv/cepesp-python) para auxiliar na consulta dos dados no nosso repositório a partir de liguagens de programação.

Sugestões, correções e demais contribuições são bem-vidas.

### Instalação:
Abra o Terminal(MacOS) ou o CMD (Windows)  e execute o seguinte codigo:

pip install -r requirements.txt

Caso não tenha o pip instalado, siga esse tuturial:
http://willemallan.com.br/2012/02/instalando-pip-no-windows/

### Fonte Original dos Dados:

Muitos dos dados originais utilizados aqui podem ser encontrados em no Repositório de Dados do TSE: http://www.tse.jus.br/eleicoes/estatisticas/repositorio-de-dados-eleitorais

### Wiki

 - [Estrutura do Projeto](Estrutura)
 - [Seletores de Colunas](Colunas)
   - [Eleições por Cargo](Colunas#reposit%C3%B3rio-elei%C3%A7%C3%B5es-por-cargo-libtsecolumnspy)
   - [Resultados da Eleição](Colunas#reposit%C3%B3rio-resultados-da-elei%C3%A7%C3%A3o-libvotoscolumnspy)
   - [Candidatos](Colunas#reposit%C3%B3rio-candidatos-libcandidatoscolumnspy)
   - [Legendas](Colunas#reposit%C3%B3rio-legendas-liblegendascolumnspy)
 - [Leitores de Dados](Leitores)
   - [Caching](Leitores#caching)
 - [Correções em Pré-Processamento](Correções-em-Pré-Processamento)
   - [Adicionar Cargos Extras (2014)](Correções-em-Pré-Processamento#adicionar-cargos-extras-2014)
   - [Correção Descrição Eleição (2014)](Correções-em-Pré-Processamento#correção-descrição-eleição-2014)
   - [Correção Descrição Eleição (2010)](Correções-em-Pré-Processamento#correção-descrição-eleição-2010)
   - [Padronização do Código Situação Turno](Correções-em-Pré-Processamento#padronização-do-código-situação-turno)
   - [Corrigir Sequencia Coligação (2014)](Correções-em-Pré-Processamento#corrigir-sequencia-coligação-2014)
   - [Corrigir Sequencia Coligação (2010)](Correções-em-Pré-Processamento#corrigir-sequencia-coligação-2010)
   - [Corrigir Código Cor Raça](Correções-em-Pré-Processamento#corrigir-código-cor-raça)
   - [Corrigir Email Candidato](Correções-em-Pré-Processamento#corrigir-email-candidato)
 - [Pós-Processamento](Pós-processamento)
 - [Pré-processamento](Pré-processamento)
