# Fluxo de Sincronização via Webhook (GitHub)

Como a wiki mantém o vault local atualizado automaticamente a partir do repositório remoto sem intervenção manual.

```text
GitHub
↓ (Evento: push no repositório)
Webhook dispara POST /api/webhook/github
↓
Flask (routes.py) recebe payload
↓
Validação de Autenticidade (git_sync_service.py)
  ├─ Lê variável de ambiente GITHUB_WEBHOOK_SECRET
  ├─ Calcula HMAC-SHA256 do payload cru
  └─ Compara usando timing-safe compare (evita ataques de timing)
↓
Se inválido: Retorna 403 Forbidden
↓
Se válido: Executa script de sync
  └─ subprocess: `git pull origin main` no diretório do vault
↓
Vault local é atualizado (novas notas entram no disco)
↓
Próximo refresh do usuário já lerá os novos arquivos (estado stateless)
```

## Importância
Este fluxo garante que a equipe possa escrever notas no Obsidian e subir para o GitHub sem precisar avisar ou reiniciar o servidor Python manualmente. Tudo acontece em background de forma segura.
