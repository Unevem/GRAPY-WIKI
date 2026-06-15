# grapy-wiki vs Obsidian Publish

## Problema
Por que criar uma engine própria para a wiki se o Obsidian já possui o Obsidian Publish nativo com suporte a Graph View?

## Solução escolhida
Desenvolver a engine própria open-source (`grapy-wiki`).

## Justificativa
Os motivos centrais são **Controle** e **Custo**:
1. **Controle Absoluto**: Tendo acesso total ao código fonte (Python, JS), podemos customizar integrações (como o RBAC baseado em pastas locais, Single Sign-On empresarial e scripts de deploy customizados via Webhooks), algo impossível em uma solução fechada de mercado.
2. **Open Source e Livre**: O Obsidian Publish é um excelente serviço, mas é pago de forma recorrente por site. O grapy-wiki é e sempre será gratuito, self-hosted, rodando em qualquer infraestrutura (on-premise ou cloud) que suporte Python básico.

## Benefícios
- Extensibilidade total de backend e frontend.
- Controle de acesso granular e customizado por pastas.
- Autonomia e hospedagem livre (independência de vendors).
