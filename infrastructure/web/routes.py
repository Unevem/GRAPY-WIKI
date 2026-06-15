import os
import unicodedata
from flask import Blueprint, render_template, abort, jsonify, send_from_directory, request
from domain.services.markdown_renderer import render_markdown
from domain.services.content_parser import ContentParser

web_bp = Blueprint("web", __name__)

def clean_for_search(name: str) -> str:
    """
    Normaliza um nome de arquivo para busca: remove acentos, transforma espaços em underscores e deixa minúsculo.
    """
    name = name.replace(".md", "")
    nfkd = unicodedata.normalize('NFKD', name)
    no_accents = "".join([c for c in nfkd if not unicodedata.combining(c)])
    return no_accents.replace(" ", "_").lower()

# Raiz do projeto (dois níveis acima de infrastructure/web/)
_PROJECT_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

# Caminho do vault de notas.
# Configure VAULT_DIR no .env para apontar para o seu vault do Obsidian.
# Fallback para WikiVaultExample/ — vault de exemplo incluído no repositório.
vault_env = os.environ.get("VAULT_DIR", "").strip()
if not vault_env:
    vault_env = os.path.join(_PROJECT_ROOT, "WikiVaultExample")
VAULT_DIR = os.path.abspath(vault_env)


from infrastructure.repositories.vault_repository import get_directory_tree
from infrastructure.services.git_sync_service import GitSyncService

@web_bp.route("/")
def index():
    """
    Rota raiz — entrega a View principal do mapa de grafo e a sidebar dinâmica.
    """
    file_tree = get_directory_tree(VAULT_DIR)
    return render_template("index.html", file_tree=file_tree)


@web_bp.route("/wiki/")
@web_bp.route("/wiki/<path:page_path>")
def wiki_page(page_path: str = "home.md"):
    """
    Rota da Wiki — lê um arquivo .md do vault, converte para HTML
    e renderiza o template wiki_page.html.

    Suporta caminhos em subpastas via '<path:page_path>', ex: NOC/Arquivo.md
    """
    # Proteção robusta contra Directory Traversal
    # Normaliza o path e verifica que permanece dentro do VAULT_DIR
    file_path = os.path.normpath(os.path.join(VAULT_DIR, page_path))
    vault_root = os.path.normpath(VAULT_DIR) + os.sep
    if not file_path.startswith(vault_root):
        abort(403)
        
    # Se omitiram a extensão .md na URL
    if not file_path.endswith('.md'):
        file_path += ".md"

    # Se não encontrar no caminho exato, fazemos uma busca no vault inteiro
    # Isso simula o comportamento real do Obsidian de achar a nota em qualquer pasta
    if not os.path.isfile(file_path):
        target_name_clean = clean_for_search(os.path.basename(file_path))
        found_path = None
        
        for root, dirs, files in os.walk(VAULT_DIR):
            for file in files:
                if file.endswith('.md'):
                    # Compara ignorando espaços/underscores, case e acentos!
                    if clean_for_search(file) == target_name_clean:
                        found_path = os.path.join(root, file)
                        break
            if found_path:
                break
                
        if found_path:
            file_path = found_path
        else:
            abort(404)

    with open(file_path, encoding="utf-8") as f:
        raw_markdown = f.read()

    # Identifica a pasta atual para o renderizador de markdown saber onde buscar as imagens
    folder = os.path.basename(os.path.dirname(file_path))
    if folder == os.path.basename(VAULT_DIR):
        folder = "Geral"

    html_content = render_markdown(raw_markdown, current_folder=folder, vault_dir=VAULT_DIR)
    
    # Busca a árvore para renderizar a mesma sidebar na página wiki também
    file_tree = get_directory_tree(VAULT_DIR)

    return render_template(
        "wiki_page.html",
        page_name=os.path.basename(page_path).replace(".md", "").replace("_", " "),
        content=html_content,
        file_tree=file_tree
    )

def verificar_permissao(usuario: str, pasta: str) -> bool:
    """
    Mock do Adapter de Autorização (RBAC).
    Garante que as políticas baseadas em pastas sejam aplicadas.
    """
    # TODO: Implementar lógica de cargos/grupos reais
    return True

@web_bp.route("/wiki/<pasta>/_anexos/<imagem>")
def serve_anexo(pasta, imagem):
    """
    Rota protegida para servir anexos de imagem.
    Garante que a imagem herde as permissões da pasta onde está armazenada.
    """
    # Bloqueia qualquer tentativa de Directory Traversal nas variáveis de URL
    if os.sep in pasta or '/' in pasta or '..' in pasta:
        abort(403)
    if os.sep in imagem or '/' in imagem or '..' in imagem:
        abort(403)

    usuario_atual = "visitante"
    
    if not verificar_permissao(usuario_atual, pasta):
        abort(403)
        
    if pasta == "Geral":
        pasta_base = VAULT_DIR
    else:
        pasta_base = os.path.join(VAULT_DIR, pasta)
        
    pasta_anexos = os.path.join(pasta_base, "_anexos")
    return send_from_directory(pasta_anexos, imagem)


@web_bp.route("/api/graph")
def api_graph():
    """
    Retorna os nós e links reais do Obsidian varrendo o Vault.
    """
    nodes = []
    links = []

    if not os.path.exists(VAULT_DIR):
        return jsonify({"nodes": nodes, "links": links})

    for root, dirs, files in os.walk(VAULT_DIR):
        # Ignora pastas ocultas
        if any(part.startswith('.') for part in root.replace('\\', '/').split('/')):
            continue

        for file in files:
            if file.endswith('.md') and not file.startswith('.'):
                file_path = os.path.join(root, file)
                
                # Extrair grupo (nome da pasta pai) ou "Geral" se estiver na raiz
                folder = os.path.basename(root)
                group = folder if folder != os.path.basename(VAULT_DIR) else "Geral"
                
                # ID interno seguro e normalizado
                node_clean_id = clean_for_search(file)
                # Label legível para o usuário (remove .md e transforma _ em espaço)
                node_label = file.replace(".md", "").replace("_", " ")
                
                rel_path = os.path.relpath(file_path, VAULT_DIR).replace("\\", "/")
                
                nodes.append({
                    "id": node_clean_id,
                    "label": node_label,
                    "group": group,
                    "url": f"/wiki/{rel_path}"
                })

                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                extracted_links = ContentParser.extract_links(content)
                for target in extracted_links:
                    target_clean_id = clean_for_search(target)
                    links.append({
                        "source": node_clean_id,
                        "target": target_clean_id
                    })

    return jsonify({"nodes": nodes, "links": links})

@web_bp.route("/api/webhook/github", methods=["POST"])
def github_webhook():
    """
    Webhook para sincronização automática com o GitHub.
    Protegido via assinatura HMAC SHA-256.
    """
    signature_header = request.headers.get("X-Hub-Signature-256")
    payload_body = request.get_data()  # Lê o payload do webhook
    secret_token = os.environ.get("GITHUB_WEBHOOK_SECRET")

    if not GitSyncService.verify_signature(payload_body, secret_token, signature_header):
        abort(403, description="Assinatura inválida ou ausente.")

    try:
        # Executa o pull dentro do vault para buscar os arquivos Markdown mais recentes
        GitSyncService.pull_repo(VAULT_DIR)
        return jsonify({"status": "success", "message": "Repository updated"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
