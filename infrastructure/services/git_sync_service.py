import hmac
import hashlib
import subprocess
import os

class GitSyncService:
    @staticmethod
    def verify_signature(payload_body: bytes, secret_token: str, signature_header: str) -> bool:
        """
        Verifica a assinatura HMAC SHA-256 do webhook enviada pelo GitHub.
        """
        if not secret_token or not signature_header:
            return False

        # Cria o hash HMAC usando a chave secreta e o corpo do payload
        # msg como argumento posicional garante compatibilidade entre versões do Python
        hash_object = hmac.new(
            secret_token.encode('utf-8'),
            payload_body,
            hashlib.sha256
        )
        
        # O GitHub envia o formato 'sha256=HASH'
        expected_signature = "sha256=" + hash_object.hexdigest()

        # Compara as strings de forma segura contra ataques de timing
        return hmac.compare_digest(expected_signature, signature_header)

    @staticmethod
    def pull_repo(vault_path: str) -> str:
        """
        Executa 'git pull' dentro do diretório especificado para sincronizar com o repositório remoto.
        """
        try:
            result = subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                cwd=vault_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            # Em caso de falha, levanta exceção para ser tratada ou logada na rota
            raise Exception(f"Erro ao sincronizar repositório: {e.stderr}")
