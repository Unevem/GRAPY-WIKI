# Presentation: Engine do Grafo e Templates

A camada de apresentação no grapy-wiki usa Jinja2 para servir o HTML inicial e Tailwind CSS para estilização, mas a grande estrela é o motor de física.

## canvas_engine.js
Implementação 100% Vanilla JS (Zero NPM) de um grafo Force-Directed rodando em um HTML5 `<canvas>`.
Ele lida com:
1. **Carregamento Assíncrono**: Faz fetch em `/api/graph` para pegar nós e links.
2. **Motor de Física**:
   - **Repulsão (Coulomb)**: Todos os nós se repelem para criar espaço.
   - **Atração (Hooke)**: Links atuam como molas conectando notas relacionadas.
   - **Gravidade e Atrito**: Puxa nós soltos para o centro e dissipa a energia gradativamente até os nós entrarem em "dormência" (sleep).
3. **Interatividade**: Usa cálculos de colisão baseados em Pitágoras (`Math.hypot`) para permitir arrastar e soltar (Drag & Drop) e um timer para diferenciar arrasto de navegação (clique rápido abre o Wikilink).
4. **Otimização BFS (Grau 1)**: Ao arrastar um nó, apenas ele e seus vizinhos imediatos são acordados, poupando processamento de física na rede inteira.

## index.html e wiki_page.html
Os templates Jinja2 que estruturam a UI. Eles importam o CSS do Tailwind pré-compilado (via binário standalone) e configuram o modo escuro (Dark Mode) de base.
