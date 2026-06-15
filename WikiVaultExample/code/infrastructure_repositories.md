# Infrastructure: Repositórios

A camada de infraestrutura conecta o mundo externo (disco, rede) à lógica interna.

## vault_repository.py
Age como o "banco de dados" do sistema, mas utilizando o sistema de arquivos local.
- Varre recursivamente o diretório `VAULT_DIR`.
- Para cada pasta encontrada (ex: `NOC`), registra como um `group` (role do RBAC).
- Para cada arquivo `.md` encontrado, lê seu conteúdo, passa para o `content_parser` para descobrir os links (`[[...]]`) e devolve uma estrutura em memória com todos os nós (notes) e conexões (links) do vault inteiro.
- É aqui que a mágica de ignorar a pasta `_anexos` acontece, focando apenas no conhecimento textual.
