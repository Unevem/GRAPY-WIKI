# Fluxo de Verificação de Permissões RBAC

Como o sistema garante que um usuário só acesse o que deve sem depender de um banco de dados complexo.

```text
Navegador solicita anexo: GET /wiki/DIRETORIA/_anexos/balanco.pdf
↓
Flask (routes.py) entra no `serve_anexo`
↓
Sanitiza o path para evitar directory traversal (`..` ou `/`)
↓
Extrai as variáveis:
  ├─ pasta = "DIRETORIA"
  └─ imagem = "balanco.pdf"
↓
Identifica usuário autenticado (atualmente mock para 'visitante')
↓
Verificador de permissão: `verificar_permissao(usuario, "DIRETORIA")`
  ├─ Verifica se o usuário tem a role "DIRETORIA" associada
  └─ Retorna True/False
↓
Se True: Envia o arquivo em disco (`send_from_directory`)
Se False: Aborta com 403 Forbidden
```

## Por que funciona assim?
Ao usar a variável de URL `<pasta>` como unidade de controle (`DIRETORIA`), atrelamos fisicamente o permissionamento ao local do arquivo no disco. Não há como um arquivo da diretoria vazar acidentalmente por falta de metadados; enquanto ele estiver dentro do diretório `/DIRETORIA`, o Flask obriga a verificação daquela role específica antes de devolver os bytes para o usuário (veja [[rbac-por-pastas]]).
