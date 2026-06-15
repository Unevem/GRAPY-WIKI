# Fluxo de Renderização de Nota Markdown

Como o sistema transforma um arquivo local `.md` em uma página HTML protegida.

```text
Navegador (Usuário)
↓ (GET /wiki/NOC/Monitoramento.md)
Flask (routes.py)
↓
Verifica permissões (mock atual via RBAC por pastas)
↓
Lê arquivo físico (vault_repository.py)
↓
Sanitiza e processa texto (markdown_renderer.py)
  ├─ Converte Markdown para HTML (python-markdown)
  ├─ Substitui `[[...]]` por tags `<a>`
  ├─ Substitui `![[...]]` por tags `<img>` apontando para `_anexos`
  └─ Limpa HTML final via bleach (anti-XSS)
↓
Jinja2 (wiki_page.html)
↓
Navegador (HTML CSS Tailwind)
```

## Por que funciona assim?
Porque separa claramente a lógica de segurança (routes), o I/O de disco (repository) e a lógica de apresentação pura (renderer), isolando as responsabilidades (veja [[arquitetura-ddd]]).
