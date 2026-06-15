# Fluxo de Resolução de Wikilinks

Como o sistema lida com o recurso do Obsidian de referenciar um arquivo apenas pelo nome (`[[Monitoramento]]`), mesmo se ele estiver dentro de várias subpastas (`wiki/NOC/Atividades/Monitoramento.md`).

```text
Markdown Renderer (markdown_renderer.py)
↓
Encontra string `[[Monitoramento]]` via Regex
↓
Chama Vault Repository para buscar a nota
↓
Vault Repository (vault_repository.py)
  ├─ Mantém um índice de cache em memória: nome do arquivo -> caminho relativo completo
  ├─ Busca `monitoramento` (após normalização de string) no índice
  └─ Retorna o caminho real (ex: `NOC/Atividades/Monitoramento.md`)
↓
Markdown Renderer constrói a tag HTML
  └─ `<a href="/wiki/NOC/Atividades/Monitoramento">Monitoramento</a>`
```

## Por que funciona assim?
No Obsidian, o usuário não precisa saber a subpasta inteira, ele só digita o nome do arquivo. Para que a wiki web replique essa facilidade e não gere links quebrados em `<a>`, o `vault_repository` atua como um DNS local, traduzindo o nome curto para o caminho completo antes de renderizar (veja [[wikilinks-vs-frontmatter]]).
