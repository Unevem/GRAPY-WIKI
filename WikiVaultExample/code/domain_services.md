# Domain: Serviços de Negócio

A camada de Domínio (`domain/`) contém a lógica pura da aplicação. Ela não conhece Flask, HTTP ou sistema de arquivos.

## markdown_renderer.py
Responsável por transformar o texto Markdown cru (que vem do Obsidian) em HTML seguro para o navegador.
- Resolve links no formato `[[Nota]]` para URLs `/wiki/<pasta>/Nota`.
- Captura anexos de imagem `![[imagem.png]]` e traduz para tags `<img>` apontando para a subpasta segura `_anexos`.
- Inclui proteção contra XSS utilizando a biblioteca `bleach` para limpar o HTML gerado.

## content_parser.py
Responsável por analisar os arquivos Markdown (via Regex) **apenas** para identificar os Wikilinks (`[[...]]`).
Ele extrai a lista de conexões que uma nota faz para outras notas, devolvendo esses dados para que o repositório consiga montar a lista de arestas (links) do grafo.
