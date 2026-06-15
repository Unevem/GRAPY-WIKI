import hmac
import hashlib
import json
import urllib.request
import urllib.error
import os

# Segredo configurado no .env
SECRET = "teste123"
URL = "http://127.0.0.1:5000/api/webhook/github"

# Payload simulando o envio do GitHub
payload = {
    "ref": "refs/heads/main",
    "repository": {
        "name": "GRAPY-WIKI",
        "full_name": "usuario/GRAPY-WIKI"
    },
    "pusher": {
        "name": "usuario"
    }
}

payload_bytes = json.dumps(payload).encode('utf-8')

# Gerar a assinatura
hash_object = hmac.new(SECRET.encode('utf-8'), payload_bytes, hashlib.sha256)
signature = "sha256=" + hash_object.hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Hub-Signature-256": signature
}

print(f"Enviando POST para {URL}...")
req = urllib.request.Request(URL, data=payload_bytes, headers=headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.status}")
        print(f"Response: {response.read().decode('utf-8')}")
except urllib.error.URLError as e:
    print(f"Erro: {e.reason}. Certifique-se de que o servidor Flask está rodando.")
