# Conector: Organização do Código

Este documento atua como o sumário para entender o que cada arquivo crítico do projeto faz. A estrutura segue os princípios de Domain-Driven Design (veja [[arquitetura-ddd]]).

- [[domain_services]] — A lógica agnóstica de parseamento e conversão de Markdown e Wikilinks.
- [[infrastructure_repositories]] — A varredura física do sistema de arquivos para mapear o vault local.
- [[infrastructure_web]] — As rotas do Flask, fábrica da aplicação e webhooks de sync.
- [[presentation_canvas]] — O motor customizado de grafo force-directed e os templates HTML.
