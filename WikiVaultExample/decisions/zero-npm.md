# Regra de Zero NPM

## Problema
Definir o ecossistema de dependências frontend do projeto.

## Solução escolhida
Proibir completamente o uso do NPM (Node Package Manager) e de frameworks JavaScript modernos (React, Vue, Webpack, etc). Todo o JS deve ser Vanilla e o CSS/Tailwind deve ser compilado via executável standalone.

## Justificativa
A decisão é baseada em segurança e simplicidade. A cadeia de suprimentos do NPM tem sofrido com vulnerabilidades críticas e malwares (como worms) injetados em pacotes populares. Ao contrário de outras wikis que dependem pesadamente de ecossistemas JS complexos, o **grapy-wiki** foi projetado para ser uma alternativa ultraleve e segura, com **zero dependências Node.js**.

## Benefícios
- Superfície de ataque drasticamente reduzida no ambiente de build/produção.
- Sem necessidade de gerenciar `node_modules` gigantescos.
- Deploy mais simples (apenas Python e um binário standalone).

## Desvantagens aceitas
- Necessidade de escrever código Vanilla JS para funcionalidades que já teriam bibliotecas prontas no NPM (ex: motor do grafo).
