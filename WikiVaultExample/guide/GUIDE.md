# GUIDE.md

# Guia de Documentação — EXEMPLO-WIKI

Este documento define como a documentação é organizada e mantida neste repositório.

Todos os contribuidores, agentes, assistentes e ferramentas de automação devem seguir estas regras ao criar ou atualizar documentação.

---

# Filosofia de Documentação

O propósito desta documentação não é apenas descrever o código.

O objetivo principal é preservar o conhecimento arquitetural, o raciocínio de negócio, as decisões de design e o comportamento do sistema.

O código pode ser inspecionado diretamente.

Os motivos por trás das decisões muitas vezes não podem.

A documentação deve priorizar explicar:

* Por que algo existe
* Por que uma decisão foi tomada
* Por que uma solução foi escolhida em vez de outra
* Quais trade-offs foram aceitos

em vez de simplesmente descrever detalhes de implementação.

---

# Estrutura de Documentação

```text
wiki/
├── guide/
│   └── GUIDE.md          ← este arquivo
├── decisions/            ← por que as coisas são como são
├── flows/                ← como os processos funcionam de ponta a ponta
├── code/                 ← como o código está organizado
└── examples/             ← templates e referências
```

Cada pasta serve a um propósito específico e responde a uma pergunta diferente.

O wiki em si é o produto — mas também é a documentação do produto.

---

# decisions/

Propósito:

Registrar decisões arquiteturais e técnicas.

Documentos de decisão respondem:

> Por que essa abordagem foi escolhida?

Exemplos de decisões já tomadas neste projeto:

* Por que NPM e dependências JavaScript externas são proibidas
* Por que o RBAC é baseado na estrutura de pastas do Obsidian
* Por que o grafo usa um motor de física customizado em vez de D3.js
* Por que o Obsidian é a fonte da verdade para permissões

Um documento de decisão deve conter:

* Problema
* Alternativas consideradas
* Solução escolhida
* Benefícios
* Desvantagens aceitas
* Consequências futuras

Um documento de decisão deve ser criado sempre que uma escolha arquitetural significativa for feita.

---

# flows/

Propósito:

Descrever o comportamento do sistema de ponta a ponta.

Documentos de fluxo respondem:

> Como um processo funciona do início ao fim?

Exemplos relevantes para este projeto:

* Fluxo de renderização de uma nota Markdown
* Fluxo de sincronização via Webhook do GitHub
* Fluxo de carregamento do grafo
* Fluxo de verificação de permissões RBAC
* Fluxo de resolução de Wikilinks entre pastas

Fluxos devem focar no movimento de informações entre camadas.

Exemplo:

```text
Obsidian (escrita)
↓
GitHub (push)
↓
Webhook HMAC → Flask
↓
git pull → Vault local
↓
Grafo recalculado na próxima requisição
```

Evite detalhes de implementação a menos que sejam necessários para entender o fluxo.

---

# code/

Propósito:

Descrever a estrutura de implementação.

Documentos de código respondem:

> Como o código está organizado?

Exemplos relevantes para este projeto:

* Camadas da arquitetura DDD (domain / infrastructure / presentation)
* Responsabilidades de cada serviço de domínio
* Como o motor de física do Canvas está estruturado
* Como o `vault_repository` varre e indexa os arquivos

Foque nos relacionamentos entre componentes.

Documente especialmente:

* Quem chama um componente
* Do que ele depende
* O que ele retorna
* Onde a lógica de negócio não deve entrar

---

# examples/

Propósito:

Fornecer templates e exemplos de documentação.

Exemplos são material de referência.

Devem demonstrar como escrever um documento de decisão, um fluxo ou uma nota de código seguindo a filosofia deste guia.

Exemplos não são documentação autoritativa.

---

# Conexões e Wikilinks

Conexões entre notas são itens de documentação de alta prioridade.

O grafo do EXEMPLO-WIKI é construído automaticamente a partir dos Wikilinks presentes nos arquivos Markdown.

Sempre que uma nota referencia outra, documente mentalmente:

* Por que a conexão existe
* Qual conhecimento ela representa
* O que um leitor ganha navegando por ela

O grafo não é apenas visual — ele é o mapa de dependências do conhecimento da organização.

Quanto mais bem conectado for o vault, mais útil é o grafo.

---

# Regras de Conteúdo

**Pastas = Cargos (Roles)**

A estrutura de pastas do vault define o sistema de controle de acesso.

Uma pasta nova criada na raiz do vault automaticamente se torna um grupo (role) no sistema RBAC.

Ao criar uma nova pasta, considere:

* Qual setor ou função ela representa
* Quem deve ter acesso às notas dentro dela
* Quais outras pastas ela precisa referenciar

**Imagens e Anexos**

Imagens devem ser salvas dentro da subpasta `_anexos` da pasta correspondente.

```text
wiki/
└── NOC/
    ├── _anexos/
    │   └── diagrama_rede.png
    └── Configurando_Radios.md
```

Imagens fora da subpasta `_anexos` serão detectadas automaticamente e um alerta visual será exibido na página no lugar da imagem.

---

# Processo de Atualização de Documentação

Antes de modificar a documentação:

1. Leia este GUIDE.md
2. Identifique os arquivos afetados
3. Identifique qual pasta responde à pergunta: decisão, fluxo ou código
4. Atualize apenas a documentação impactada pela mudança

Não reescreva documentação não relacionada à mudança.

---

# Prioridade de Documentação

Ao documentar uma mudança, priorize as informações nesta ordem:

1. Decisões
2. Fluxos
3. Código

O objetivo é preservar conhecimento, não duplicar código-fonte.

---

# Regra para Agentes

Quando houver incerteza sobre onde uma informação pertence:

* Por quê → decisions/
* Como → flows/
* Implementação → code/
* Referência → examples/

Sempre escolha o local com base na pergunta sendo respondida.

---

# Modelo de Documentação deste Projeto

Este projeto usa duas camadas de documentação.

**Documentação do Repositório (wiki/):**
- Orientada à navegação e ao conhecimento do negócio
- Mantida no Obsidian e sincronizada via GitHub
- Versionada junto com o código

**Documentação Técnica (README.md e roadmap.md na raiz):**
- Instruções de instalação e execução
- Decisões de arquitetura de alto nível
- Planejamento de fases

A wiki serve como base de conhecimento.

O repositório serve como o motor que a renderiza.

![[larry.png]]
