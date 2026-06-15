# Infrastructure: Web e Rotas

A interface HTTP do grapy-wiki utilizando Flask.

## flask_app.py
A factory da aplicação. Aqui o Flask é instanciado, as pastas de `templates` e `static` são mapeadas, e a secret key e o modo DEBUG são definidos via variáveis de ambiente para garantir segurança em produção.

## routes.py
O controlador (Controller) que define as 5 portas de entrada da aplicação:
1. `/`: Rota raiz que devolve a interface do Canvas (`index.html`).
2. `/wiki/<pasta>/<arquivo>`: Serve o HTML renderizado de uma nota.
3. `/wiki/<pasta>/_anexos/<imagem>`: Serve arquivos de imagem com proteção contra *Directory Traversal* e herança de permissões (RBAC mockado no momento).
4. `/api/graph`: Rota JSON consumida pelo motor Canvas que devolve a árvore completa gerada pelo `vault_repository`.
5. `/api/webhook/github`: Endpoint seguro via HMAC-SHA256 para sincronizar o vault local via `git pull` quando ocorre um push no GitHub.
