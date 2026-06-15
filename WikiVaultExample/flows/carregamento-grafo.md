# Fluxo de Carregamento do Grafo

Como o mapa visual interativo é desenhado na tela inicial usando os dados do Obsidian.

```text
Navegador (Usuário abre raiz /)
↓
Flask serve index.html (UI base)
↓
Canvas Engine JS inicia (Vanilla JS)
↓
AJAX (fetch) chama GET /api/graph
↓
Flask (routes.py)
↓
Vault Repository (vault_repository.py)
  ├─ Varre todas as pastas e arquivos do VAULT_DIR recursivamente
  ├─ Ignora pastas `_anexos` e lixos
  ├─ Para cada arquivo, extrai os Wikilinks com `content_parser.py`
  └─ Monta listas de `nodes` e `links` com IDs normalizados
↓
JSON retornado para o navegador
↓
Canvas Engine carrega nós no centro da tela e inicia a física
  ├─ Coulomb afasta todos os nós
  ├─ Hooke puxa nós que possuem links
  └─ Fricção desacelera a animação até dormir (sleepThreshold)
```

## Importância
Esse fluxo garante que a visualização de dados não onere a carga inicial da página. Primeiro o usuário vê a casca vazia do app, e depois a física começa a atuar no front-end, garantindo responsividade (veja [[motor-fisica-customizado]]).
