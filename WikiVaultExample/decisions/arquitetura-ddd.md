# Arquitetura DDD e Separação de Camadas

## Problema
Como organizar a estrutura de pastas e a lógica do código em um projeto primariamente focado em visualização de notas.

## Solução escolhida
Adoção do padrão arquitetural **Domain-Driven Design (DDD)** simplificado, com pastas explícitas para `domain`, `infrastructure` e `presentation`.

## Justificativa
Ainda que o projeto inicial seja de escopo pessoal/reduzido, a adoção do DDD atende a dois propósitos principais:
1. **Aprendizado e Boas Práticas**: Garantir que o código permaneça organizado e escopo bem delimitado.
2. **Facilitar a migração**: Conforme descrito em `migracao-django.md`, manter o núcleo do negócio (parse de Markdown, geração do grafo) agnóstico em relação à web e framework (Flask) permite que no futuro outro framework seja plugado (ex: Django) trocando apenas a camada `infrastructure/web`, preservando intacto todo o `domain`.

## Benefícios
- O `domain` é puro Python, sem saber que a internet existe.
- Alta testabilidade da lógica de negócios.
- Permite que a wiki cresça de forma sustentável sem virar um "monólito espaguete" de rotas web chamando lógica diretamente.
