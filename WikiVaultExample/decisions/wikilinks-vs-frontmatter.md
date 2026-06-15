# Wikilinks vs Frontmatter para o Grafo

## Problema
Definir a fonte de verdade para criar as conexões (arestas) no mapa de conhecimento.

## Alternativas consideradas
- **Frontmatter YAML**: Metadados estruturados no topo de cada arquivo Markdown (ex: `related: [Nota A, Nota B]`).
- **Wikilinks inline**: Links diretamente no corpo do texto (ex: `[[Nota A]]`).

## Solução escolhida
Utilizar os Wikilinks (`[[...]]`) inline do Obsidian como única fonte para a formação do grafo.

## Justificativa
A decisão foca na **facilidade de documentação e fluidez da escrita**. Exigir que o usuário suba ao topo do arquivo para preencher um frontmatter toda vez que quiser criar uma relação quebra o fluxo de raciocínio. Ao utilizar Wikilinks, a pessoa apenas escreve o texto e linka naturalmente as ideias conforme elas surgem. O parser do backend varre o texto e extrai esses links magicamente para formar o grafo.

## Benefícios
- Experiência de escrita sem interrupções (frictionless).
- Funciona exatamente como o Obsidian nativo.
- O grafo representa conexões orgânicas reais do texto, não apenas categorização metadados.
