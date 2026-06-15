# Motor de Física Customizado vs D3.js

## Problema
Como renderizar e calcular a física do grafo de nós de conhecimento.

## Alternativas consideradas
- **D3.js**: Padrão da indústria para visualização de dados e grafos force-directed.
- **Motor customizado Vanilla JS**: Implementação própria usando Canvas API e matemática básica.

## Solução escolhida
Desenvolver um motor de física customizado usando HTML5 Canvas e Vanilla JavaScript.

## Justificativa
Esta escolha foi uma consequência direta da regra arquitetural de **Zero NPM** (veja a decisão `zero-npm.md`). Como estamos evitando dependências externas de JavaScript para garantir segurança e simplicidade de build, importar a biblioteca D3.js (ou requerer um bundler para ela) quebraria essa regra. Desenvolver o motor localmente nos deu controle absoluto e atendeu perfeitamente aos requisitos restritos de performance e independência.

## Benefícios
- Mantém o cumprimento da regra Zero NPM.
- Controle total sobre o código de física (Lei de Hooke e Coulomb).
- Código final extremamente enxuto e carregamento instantâneo.

## Desvantagens aceitas
- Tempo de desenvolvimento investido em reescrever algoritmos de física.
- Falta de features avançadas prontas que a comunidade do D3 já resolveu.
