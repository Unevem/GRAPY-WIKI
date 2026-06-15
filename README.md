# grapy-wiki

Mapa de conhecimento interativo baseado nas notas do Obsidian. Grafo force-directed renderizado em HTML5 Canvas com motor de física customizado em Vanilla JS, backend em Flask e arquitetura MVC + DDD.

---

## 📋 Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- O binário **Tailwind CSS CLI v4** (standalone, sem Node.js):
  - Baixe em: https://github.com/tailwindlabs/tailwindcss/releases
  - Arquivo: `tailwindcss-windows-x64.exe`
  - Renomeie para `tailwindcss.exe` e coloque na **raiz do projeto**

---

## 🚀 Configuração Inicial (apenas na primeira vez)

### 1. Criar e ativar o ambiente virtual

```powershell
python -m venv venv
venv\Scripts\activate
```

### 2. Instalar as dependências Python

```powershell
pip install -r requirements.txt
```

### 3. Configurar as variáveis de ambiente

```powershell
copy .env.example .env
```

Abra o `.env` e preencha os valores:

| Variável | Descrição |
|---|---|
| `FLASK_SECRET_KEY` | Chave para assinar sessões. Gere com `python -c "import secrets; print(secrets.token_hex(32))"` |
| `FLASK_DEBUG` | `true` em desenvolvimento, `false` em produção |
| `GITHUB_WEBHOOK_SECRET` | Secret configurado no GitHub para validação HMAC do webhook de sync |

### 4. Criar o vault de notas

O projeto lê arquivos Markdown da pasta configurada via VAULT_DIR.
Se não configurado, ele lê a pasta `WikiVaultExample/` na raiz do repositório.

A estrutura de pastas define automaticamente os grupos do grafo e as roles do RBAC:

```
WikiVaultExample/
├── NOC/                  ← grupo "NOC" no grafo
│   ├── _anexos/          ← imagens e anexos do setor
│   └── Nota.md
├── DIRETORIA/
│   ├── _anexos/
│   └── Guia_Geral.md
└── guide/
    └── GUIDE.md
```

---

## ▶️ Iniciando o Desenvolvimento

Abra **dois terminais** na raiz do projeto.

### Terminal 1 — Tailwind CSS (watch)

```powershell
.\tailwindcss.exe -i presentation\static\css\input.css -o presentation\static\css\output.css --watch
```

### Terminal 2 — Servidor Flask

```powershell
venv\Scripts\activate
flask --app infrastructure\web\flask_app.py run --debug
```

Acesse em: **http://127.0.0.1:5000**

---

## 📁 Estrutura do Projeto

```
grapy-wiki/
│
├── domain/                       # Camada de Domínio (DDD) — lógica pura, sem framework
│   └── services/
│       ├── markdown_renderer.py  # Converte Markdown + Wikilinks do Obsidian em HTML
│       └── content_parser.py     # Extrai links [[...]] para montar o grafo
│
├── infrastructure/               # Infraestrutura (adaptável: Flask hoje, Django amanhã)
│   ├── repositories/
│   │   └── vault_repository.py  # Varre o vault e monta a árvore de pastas/notas
│   ├── services/
│   │   └── git_sync_service.py  # Webhook GitHub com validação HMAC-SHA256
│   └── web/
│       ├── flask_app.py          # Factory da aplicação Flask
│       └── routes.py             # Rotas: wiki, grafo, anexos, webhook
│
├── presentation/                 # Camada de Apresentação
│   ├── templates/
│   │   ├── index.html            # Mapa de grafo interativo (Canvas)
│   │   └── wiki_page.html        # Renderização de notas Markdown
│   └── static/
│       ├── js/
│       │   └── canvas_engine.js  # Motor de física force-directed (Vanilla JS puro)
│       └── css/
│           ├── input.css         # Entrada do Tailwind
│           └── output.css        # CSS compilado — gerado automaticamente
│
├── WikiVaultExample/             # Vault de notas de exemplo (fonte da verdade)
│   └── <SETOR>/
│       ├── _anexos/              # Imagens do setor (RBAC herdado da pasta pai)
│       └── Nota.md
│
├── tests/                        # Testes unitários e de integração
├── .env.example                  # Template de variáveis de ambiente
├── .gitignore
├── requirements.txt
├── roadmap.md
└── README.md
```

---

## 🌐 Rotas Disponíveis

| Rota | Método | Descrição |
|---|---|---|
| `/` | GET | Mapa de grafo interativo |
| `/wiki/<pasta>/<arquivo>` | GET | Renderiza uma nota Markdown |
| `/wiki/<pasta>/_anexos/<imagem>` | GET | Serve imagens com validação de permissão |
| `/api/graph` | GET | JSON com nós e links do grafo completo |
| `/api/webhook/github` | POST | Sincronização automática via push do GitHub |

---

## 🔗 Webhook de Sincronização (produção)

O grapy-wiki suporta sincronização automática via push no GitHub.

Configure no seu repositório:

1. Vá em **Settings → Webhooks → Add webhook**
2. **Payload URL:** `https://seu-servidor.com/api/webhook/github`
3. **Content type:** `application/json`
4. **Secret:** o mesmo valor de `GITHUB_WEBHOOK_SECRET` no `.env`
5. **Evento:** apenas `push`

A cada `git push`, o servidor executa `git pull` automaticamente no vault.

---

## ⚠️ Regras da Stack

| Regra | Detalhe |
|---|---|
| **PROIBIDO** `npm`, `yarn`, `pnpm` | Zero dependências JS instaladas por terminal |
| **PROIBIDO** frameworks JS | Sem React, Vue, Vite, Webpack, etc. |
| Tailwind via **binário standalone** | Baixar o `.exe` direto — sem `node_modules` |
| Estilo via **Vanilla CSS + Tailwind** | Motor de grafo em Canvas puro |

---

## 🏗️ Arquitetura

O projeto segue **DDD (Domain-Driven Design)** com separação em camadas:

- **`domain/`** — lógica de negócio pura, sem dependência de Flask ou qualquer framework
- **`infrastructure/`** — implementações concretas (leitura de arquivos, rotas HTTP, serviços externos)
- **`presentation/`** — templates HTML e assets estáticos

A camada `domain/` é 100% agnóstica ao framework. Para migrar de Flask para Django, basta reescrever `infrastructure/web/` — nenhuma linha de `domain/` precisa ser alterada.

---

## 📖 Documentação

A documentação do projeto vive dentro do próprio vault, na pasta `WikiVaultExample/guide/`:

- [`WikiVaultExample/guide/GUIDE.md`](WikiVaultExample/guide/GUIDE.md) — filosofia e estrutura da documentação
- [`roadmap.md`](roadmap.md) — fases de desenvolvimento planejadas