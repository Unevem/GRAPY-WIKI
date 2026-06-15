# Suporte à Migração para Django

## Problema
Definir o nível de acoplamento entre a lógica da wiki e o framework web (Flask).

## Solução escolhida
Manter a arquitetura desacoplada e manter a documentação/roadmap prevendo uma possível migração para Django.

## Justificativa
O objetivo principal do projeto open source é facilitar a vida de quem deseja adotar o motor da wiki. O Django é um dos frameworks web mais populares e robustos no ecossistema Python. Ao mantermos a arquitetura limpa (Domain-Driven Design) e documentarmos o caminho para uma migração, garantimos que equipes que já possuem uma stack baseada em Django possam integrar esta wiki aos seus sistemas sem precisarem reescrever a lógica de negócio (parseamento de Markdown, grafos, etc).

## Benefícios
- Facilita a adoção por empresas que já usam Django.
- Força a manutenção de uma arquitetura limpa e agnóstica de framework.

## Desvantagens aceitas
- Esforço extra para manter a abstração das rotas e serviços.
