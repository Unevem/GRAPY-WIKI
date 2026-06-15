# Flask sobre FastAPI

## Problema

Escolher o framework web Python mais adequado para o motor SSR do grapy-wiki.

## Alternativas consideradas

- **FastAPI** — moderno, rápido, com Swagger/OpenAPI automático, validação Pydantic e suporte nativo a async
- **Flask** — minimalista, maduro, SSR nativo via Jinja2, sem overhead de tipagem estrita

## Solução escolhida

Flask.

## Justificativa

O grapy-wiki atua primariamente como um motor de **Server-Side Rendering (SSR)**: lê arquivos Markdown do disco e renderiza HTML via Jinja2.

Não é uma API RESTful de consumo externo.

Os principais benefícios do FastAPI configuram complexidade desnecessária para este escopo:

- Swagger/OpenAPI automático → sem clientes externos consumindo a API
- Validação Pydantic estrita → os dados vêm do sistema de arquivos local, não de payloads externos
- Roteamento assíncrono → o I/O é local e síncrono; ganhos de performance seriam imperceptíveis

O Flask é nativamente otimizado para SSR com Jinja2, que é exatamente o padrão de uso aqui.

## Benefícios

- Sem overhead de configuração de tipos e schemas
- Jinja2 integrado sem configuração adicional
- Menor curva de aprendizado para contribuidores
- Blueprints nativos para organização por feature

## Desvantagens aceitas

- Sem documentação de API gerada automaticamente
- Validação de entrada manual (mitigado com `bleach` e validações explícitas nas rotas)

## Consequências

A camada `domain/` permanece 100% agnóstica ao framework.

Caso o escopo do projeto cresça para incluir uma API RESTful de consumo externo, a migração para FastAPI seria cirúrgica: apenas `infrastructure/web/` precisaria ser reescrito.
