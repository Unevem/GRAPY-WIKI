# Roadmap — grapy-wiki

## Visão Geral

O objetivo desta fase é entregar um MVP (Produto Mínimo Viável) funcional e bem estruturado, com foco no motor de física do mapa de grafo antes de incorporar o sistema completo de rotas e renderização de conteúdo da Wiki.

A arquitetura segue os padrões **MVC (Model-View-Controller)** e **DDD (Domain-Driven Design)**, garantindo separação clara de responsabilidades e facilitando a evolução do projeto ao longo do tempo.

---

## Princípios e Restrições da Stack

### Regras Inegociáveis

- **PROIBIDO** o uso de `npm`, `yarn`, `pnpm` ou qualquer gerenciador de pacotes JavaScript. Toda dependência de frontend deve ser incluída via arquivo local (`.js`, `.css`) ou CDN declarativo, nunca via instalação por terminal.
- **PROIBIDO** o uso de frameworks ou bibliotecas JS instaladas como dependências de projeto (ex.: React, Vue, Svelte, Webpack, Vite, etc.).
- O frontend é construído exclusivamente com **HTML5, Vanilla JS e CSS/Tailwind CLI standalone** (binário autônomo, sem `node_modules`).

### Stack Definida

| Camada      | Tecnologia                                         |
|-------------|----------------------------------------------------|
| Backend     | Python 3 + Flask                                   |
| Frontend    | HTML5 Canvas + Vanilla JS                          |
| Estilização | Tailwind CSS CLI (binário standalone)              |
| Algoritmos  | NetworkX (Python)                                  |
| Watcher     | `watchdog` (Python) — escuta de eventos de I/O     |
| Dados       | Arquivos `.md` locais (Vault do Obsidian)          |
| Áudio       | Web Audio API (nativo do navegador, sem dependências) |

---

## Arquitetura do Projeto

O projeto é organizado segundo os princípios de **MVC** e **DDD**. A separação de camadas é desenhada para que a troca do framework web (ex.: de Flask para Django) exija mudanças apenas na camada de infraestrutura/apresentação, sem tocar na lógica de domínio.

```
brayo-wiki/
│
├── domain/                  # Camada de Domínio (DDD)
│   ├── entities/            # Entidades: Note, Graph, Link
│   └── services/            # Regras de negócio puras (sem dependência de framework)
│       ├── graph_builder.py      # Construção do grafo a partir das notas
│       └── content_parser.py     # Extração de links internos [[...]]
│
├── application/             # Casos de Uso (orquestra domínio + infraestrutura)
│   └── use_cases/
│       └── build_graph_use_case.py
│
├── infrastructure/          # Camada de Infraestrutura (adaptável por framework)
│   ├── repositories/
│   │   └── vault_repository.py   # Leitura do sistema de arquivos local
│   ├── watchers/
│   │   └── vault_watcher.py      # Processo assíncrono watchdog (escuta de eventos de I/O)
│   └── web/                 # Ponto de troca: Flask hoje, Django amanhã
│       ├── flask_app.py          # Factory da aplicação Flask
│       └── routes.py             # Definição de rotas (Controllers no MVC)
│
├── presentation/            # Camada de Apresentação (View no MVC)
│   ├── templates/           # Templates HTML (Jinja2 / Django Templates)
│   └── static/
│       ├── js/              # Vanilla JS (sem bundler, sem NPM)
│       └── css/             # CSS compilado pelo Tailwind CLI standalone
│
├── cache/
│   └── mapa_cache.json      # Grafo de Grau 1 pré-computado (atualizado pelo watcher)
│
└── tests/                   # Testes unitários e de integração
```

### Por que essa estrutura facilita a migração para Django?

A lógica de negócio (domínio e casos de uso) é **completamente agnóstica ao framework web**. A migração de Flask para Django se resume a:

1. Criar um novo `django_app/` dentro de `infrastructure/web/`.
2. Mapear as rotas Flask existentes para `urls.py` do Django.
3. Substituir o template engine (Jinja2 → Django Templates, que são compatíveis).
4. Nenhuma linha de código em `domain/` ou `application/` precisa ser alterada.

---

## Funcionalidades do MVP

### Backend (Python / Flask)

O backend no MVP é responsável por processar os arquivos locais do Obsidian e expor os dados tratados para o frontend via API REST simples.

#### F1 — Scanner de Diretório (`VaultRepository`)
- Localizado em `infrastructure/repositories/vault_repository.py`.
- Aponta para a pasta local do vault do Obsidian.
- Varre recursivamente o diretório na **inicialização da aplicação**, coletando apenas arquivos com extensão `.md` para construir o estado inicial do grafo.
- Isola a leitura do sistema de arquivos do restante da lógica, permitindo futura substituição por outras fontes (banco de dados, API remota, etc.).

#### F2 — Parser de Conteúdo (`ContentParser`)
- Localizado em `domain/services/content_parser.py`.
- Lê o texto de cada nota e aplica a expressão regular `r'\[\[(.*?)\]\]'` para identificar e extrair links internos no padrão `[[Nome da Nota]]`.
- Serviço de domínio puro: sem dependência de Flask, Django ou qualquer framework.

#### F3 — Watcher Orientado a Eventos (`VaultWatcher`)
- Localizado em `infrastructure/watchers/vault_watcher.py`.
- Tecnologia: biblioteca `watchdog` (Python).
- Opera como um processo assíncrono paralelo ao servidor Flask, escutando eventos nativos de I/O do sistema operacional sobre o diretório do vault.
- **Fluxo de execução ao detectar uma modificação:**
  1. O usuário salva um arquivo `.md` no Obsidian.
  2. O `watchdog` captura o evento `on_modified` para o arquivo alterado.
  3. O `ContentParser` é invocado **exclusivamente sobre o arquivo modificado** (sem reprocessar o vault inteiro).
  4. A estrutura de dados em memória é atualizada e o arquivo `cache/mapa_cache.json` é sobrescrito com o grafo de Grau 1 atualizado.
- **Vantagem de desempenho:** elimina a necessidade de varreduras por cronjob (que introduzem atraso) ou processamento sob demanda (que sobrecarregam o servidor no momento da requisição).
- **Debounce de 300ms:**
  - O Obsidian dispara múltiplos eventos `on_modified` em sequência rápida enquanto o usuário digita, podendo gerar erros de `I/O` (arquivo bloqueado pelo processo do Obsidian) e desperdício de CPU.
  - Solução: ao capturar um evento, o watcher **não processa imediatamente** — em vez disso, inicia (ou reinicia) um cronômetro de 300ms via `threading.Timer`. O processamento do arquivo só ocorre quando o usuário para de digitar por 300ms contínuos.
  - Implementação: cada novo evento cancela o `Timer` anterior (`timer.cancel()`) e cria um novo, garantindo que apenas a última versão estável do arquivo seja lida.

#### F4 — Construtor de Grafo (`GraphBuilder`)
- Localizado em `domain/services/graph_builder.py`.
- Recebe a lista de notas e conexões produzida pelo `ContentParser`.
- Alimenta a biblioteca `NetworkX` para construir o grafo e executa o algoritmo `spring_layout` no servidor, gerando as coordenadas iniciais $(X, Y)$ de cada nó.
- O resultado é persistido em `cache/mapa_cache.json` na inicialização e atualizado incrementalmente pelo `VaultWatcher`.

#### F5 — Endpoint de API (`/api/graph`)
- Localizado em `infrastructure/web/routes.py` (Controller no MVC).
- Complexidade de leitura **O(1)**: o Flask serve o arquivo `cache/mapa_cache.json` já pré-computado em disco, sem nenhum processamento adicional na requisição.
- Latência de resposta próxima de zero na carga inicial do HUB.
- **Estrutura do payload (conexões de Grau 1):**

```json
{
  "nodes": [
    { "id": "Nota_A", "x": 120, "y": 250, "url": "/wiki/Nota_A" }
  ],
  "links": [
    { "source": "Nota_A", "target": "Nota_B" }
  ]
}
```

---

### Frontend (HTML5 Canvas / Vanilla JS / Tailwind CLI)

O frontend consome o JSON de Grau 1 da API e executa toda a renderização, simulação física, busca em grafo e feedback visual no lado do cliente, sem dependências externas instaladas via NPM.

#### F6 — Motor de Renderização (`Canvas Engine`)
- Inicialização de um elemento `<canvas>` que ocupa 100% da área útil da janela.
- Loop de desenho via `requestAnimationFrame`: limpa e redesenha os nós (círculos), rótulos e arestas (linhas) a cada frame.
- Nós em estado de dormência (`active = false`) são ignorados pelo loop de cálculo físico, mas continuam sendo renderizados em suas últimas coordenadas conhecidas.
- **Ajuste de Escala HiDPI (`devicePixelRatio`):**
  - Telas de alta densidade (Full HD, 4K, Retina) mapeiam múltiplos pixels físicos para cada pixel lógico do navegador. Sem ajuste, o Canvas renderiza na resolução lógica e o SO estica o resultado, gerando linhas borradas e textos serrilhados.
  - Solução em três passos aplicados na inicialização e em todo `resize`:
    1. Ler `window.devicePixelRatio` (ex.: `2.0` em telas Retina).
    2. Multiplicar a resolução interna do Canvas (`canvas.width` e `canvas.height`) pelo ratio.
    3. Usar CSS para manter o tamanho visual original (`canvas.style.width/height`), e aplicar `ctx.scale(ratio, ratio)` para que todas as chamadas de desenho se ajustem automaticamente à nova resolução.
  - Resultado: linhas de 1px visualmente nítidas em qualquer densidade de tela, sem nenhuma alteração nas coordenadas de desenho do motor de física.

#### F7 — Motor de Física com BFS Local e Dormência de Nós (`Force-Directed + Sleeping Nodes`)
- O navegador recebe o JSON de Grau 1 e o mantém integralmente na memória RAM.
- **Busca em Largura (BFS) sob demanda:** no evento `mousedown`, o motor JS executa uma BFS instantânea na estrutura de dados em memória, mapeando a árvore de conexões até o limite configurável (ex.: 3 a 4 graus de profundidade). Tempo estimado de execução: < 1ms.
- **Física Force-Directed:**
  - **Repulsão:** nós se afastam uns dos outros (simulação da lei de Coulomb).
  - **Atração:** arestas funcionam como molas (simulação da lei de Hooke).
- **Otimização por Atenuação e Dormência:**
  - Cada salto a partir do nó arrastado aplica um fator de atenuação de energia (ex.: −15% por grau de separação na BFS).
  - Nós cuja força resultante caia abaixo do limiar configurável entram em dormência (`active = false`) e são removidos do loop de cálculo, poupando a CPU de computar a posição de milhares de nós irrelevantes.

#### F8 — Detecção de Clique por Raycasting
- O Canvas é uma superfície plana sem elementos DOM individuais por nó.
- O JavaScript escuta eventos de clique na tela, calcula a distância geométrica do cursor até cada nó e determina qual nó foi selecionado com base em um raio de tolerância configurável.

#### F9 — Interatividade do Mouse (Drag, Pan & Zoom)
- **Drag:** clicar e arrastar um nó reativa o motor de física nos nós vizinhos mapeados pela BFS.
- **Pan:** clicar no fundo e arrastar translada o ponto de origem do mapa.
- **Zoom:** scroll do mouse aplica escala ao canvas, com zoom centrado na posição do cursor.

#### F10 — Feedback Tátil e Visual (`Juiciness`)
- Tecnologia: HTML5 Canvas API + Web Audio API (nativa do navegador, sem dependências externas).
- Princípio: desacoplar a **percepção visual** do tempo de cálculo matemático, criando a ilusão de física elástica e resposta imediata sem lag perceptivo.
- **Ciclo de interação:**
  - `mousedown`: a BFS é executada na RAM. Simultaneamente, o raio do nó selecionado aumenta (ex.: 10px → 15px), `ctx.shadowBlur` é ativado para gerar um brilho ao redor do nó, e um som de feedback ("pop") é disparado via `new Audio()` — nativo, sem biblioteca.
  - `mousemove`: o nó arrastado atualiza suas coordenadas $(X, Y)$ em tempo real colado ao cursor, enquanto os vizinhos respondem à física direcional calculada frame a frame.
  - `mouseup`: o raio e o brilho retornam ao estado original com transição suave, e a lista de arrasto temporária é descartada pelo Garbage Collector do V8.

#### F11 — Interface Base (Tailwind CLI Standalone)
- Layout estruturado em HTML ao redor do Canvas.
- Compilação de classes utilitárias do Tailwind via binário CLI autônomo (sem `node_modules`, sem `package.json`).
- Painel lateral exibindo estatísticas do grafo: total de notas, total de conexões, e estado do motor de física.

---

## Fase 2: Renderização de Markdown (Ainda no MVP/Flask)

O objetivo desta fase é consolidar a Wiki, lendo arquivos `.md` físicos do vault e renderizando-os em HTML usando a biblioteca nativa `markdown` do Python.

#### F12 — Motor de Renderização de Markdown
- **Domínio:** Criação do serviço de domínio puro `domain/services/markdown_renderer.py`, responsável pela conversão para HTML.
- **Rotas e Views:** Criação da rota `/wiki/<pasta>/<arquivo>` no `infrastructure/web/routes.py`, que lê o arquivo correspondente no sistema local e renderiza o conteúdo processado no template `presentation/templates/wiki_page.html`.

---

## Segurança e Controle de Acesso (RBAC baseada em Pastas)

A arquitetura de controle de acesso (Role-Based Access Control - RBAC) utiliza as pastas do Obsidian como fonte primária da verdade para a definição de papéis.

#### Princípios de RBAC Integrados ao Vault
- O **Obsidian é a Fonte da Verdade:** Pastas criadas na raiz do vault (ex.: `/NOC`, `/Diretoria`) atuam automaticamente como "Cargos" (Roles) no sistema.
- As notas, mídias e imagens dentro dessas pastas herdam implicitamente as restrições da pasta pai.

#### Implementação via Padrão Adapter (Ports and Adapters)
- A verificação de permissões é isolada em um **Adapter** arquitetural.
- **No MVP (Flask):** O componente `auth_adapter.py` (na camada de infraestrutura) utilizará dados *mockados* (hardcoded) para verificar se o usuário solicitante tem permissão para a pasta requerida. Em caso negativo, a rota é bloqueada devolvendo um erro `403 Forbidden`.

---

## Plano de Migração para Django (Fase 3)

A migração completa do framework web de Flask para Django (que hospeda o App Principal da empresa) ocorrerá **estritamente após a conclusão e validação da Fase 2**.

#### Motivadores da Espera
- Evitar o desenvolvimento de lógicas complexas de usuários, sessões e permissões no Flask. O Flask serve como um ambiente ágil e isolado para afiar a matemática do Canvas e o parser de Markdown.

#### O que será feito nativamente no Django
Ao migrar a camada `infrastructure/web`, o domínio permanece intacto e as seguintes funcionalidades de infraestrutura ganham vida no Django:
- **Integração real com Active Directory (AD)** corporativo.
- Substituição do *mock* de permissões no `auth_adapter.py` por consultas reais ao banco de dados relacional.
- Construção de um **Painel Administrativo de Permissões** usando o Django Admin.
- Integração com um **Motor de Busca Global** robusto (ex.: ElasticSearch/Postgres Full-Text Search).

---

> **Nota de Arquitetura:** A separação entre domínio, aplicação e infraestrutura não é burocracia — é o que garante que cada fase futura seja uma evolução, não uma reescrita. O uso do padrão Adapter para a segurança garante que o domínio do grafo jamais precise conhecer se o usuário veio de uma sessão do Flask ou de um token JWT do Django.