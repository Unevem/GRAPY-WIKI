# Controle de Acesso (RBAC) Baseado em Pastas

## Problema
Como definir quem tem acesso a qual nota ou arquivo dentro da Wiki.

## Alternativas consideradas
- **Frontmatter YAML**: Metadados dentro do arquivo (`roles: [Admin, NOC]`).
- **Banco de dados**: Tabela de permissões relacional com IDs dos arquivos.
- **Estrutura de Pastas**: A pasta física no disco dita a role que tem acesso.

## Solução escolhida
RBAC (Role-Based Access Control) baseado unicamente na **estrutura de pastas** física do Vault.

## Justificativa
Esta escolha brilha pela sua consistência de ponta a ponta e por resolver a lacuna dos arquivos anexos:
1. **Arquivos Binários**: PDFs e imagens não suportam injeção de YAML nativo. Se usássemos metadados internos, os anexos ficariam desprotegidos ou exigiriam uma base paralela de configuração.
2. **Segurança "Default"**: É impossível esquecer de definir as permissões de um arquivo recém-criado, porque o simples fato de ele estar em `NOC/Nota.md` já faz com que herde automaticamente a proteção do grupo NOC.
3. **Leveza**: Nenhuma consulta SQL ou parsing complexo é necessário, apenas checar o path do arquivo durante o request HTTP.

## Benefícios
- Anexos (imagens e PDFs) estão inerentemente protegidos com as mesmas regras das notas.
- Prevenção de falha humana (não há como esquecer de assinar uma tag de permissão).
- Integração perfeita com o modelo do Obsidian.
