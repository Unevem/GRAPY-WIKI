import markdown as md
import re
import os
import bleach
from urllib.parse import quote

# Tags e atributos permitidos pelo sanitizador HTML
_ALLOWED_TAGS = (
    bleach.sanitizer.ALLOWED_TAGS
    | {'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'code',
       'blockquote', 'img', 'table', 'thead', 'tbody', 'tr', 'th',
       'td', 'ul', 'ol', 'li', 'strong', 'em', 'br', 'hr', 'div', 'span'}
)
_ALLOWED_ATTRS = {
    '*': ['class'],
    'a': ['href', 'class'],
    'img': ['src', 'alt', 'class'],
}

def process_obsidian_syntax(text: str, current_folder: str, vault_dir: str) -> str:
    """
    Identifica anexos de imagem (![[Target]]) e links ([[Target|Display]])
    do Obsidian e os converte para tags HTML responsivas padrão.
    """
    # 1. Processar Imagens
    def img_repl(match):
        filename = match.group(1)
        
        # Determinar o caminho esperado físico da imagem
        if current_folder == "Geral":
            expected_path = os.path.join(vault_dir, "_anexos", filename)
        else:
            expected_path = os.path.join(vault_dir, current_folder, "_anexos", filename)
            
        if os.path.exists(expected_path):
            src = f"/wiki/{current_folder}/_anexos/{filename}"
            return f'<img src="{src}" alt="{filename}" class="max-w-full h-auto rounded shadow-md my-4">'
        else:
            return (
                f'<div class="bg-amber-500/10 border border-amber-500 text-amber-500 p-4 rounded-lg my-4 flex flex-col gap-1 text-sm font-medium">'
                f'⚠️ Alerta de Mídia: A imagem \'{filename}\' não foi encontrada na subpasta \'_anexos\' deste setor. '
                f'Certifique-se de que o Obsidian está configurado para salvar anexos na subpasta atual ou mova o arquivo manualmente no seu gerenciador.'
                f'</div>'
            )

    text = re.sub(r'!\[\[(.*?)\]\]', img_repl, text)

    # 2. Processar Links de Texto
    def link_repl(match):
        content = match.group(1)
        if '|' in content:
            target_url, display_text = content.split('|', 1)
        else:
            target_url = content
            display_text = content

        display_text = display_text.replace("_", " ")
        # Codifica o target para evitar injeção de HTML/JS no atributo href
        safe_url = quote(target_url, safe='/')
        return f'<a href="/wiki/{safe_url}" class="text-sky-400 hover:text-sky-300 hover:underline font-medium">{display_text}</a>'

    text = re.sub(r'\[\[(.*?)\]\]', link_repl, text)
    
    return text


def render_markdown(text: str, current_folder: str = "Geral", vault_dir: str = "") -> str:
    """
    Serviço de domínio puro — converte texto Markdown em HTML.
    
    Agora suporta renderização de imagens relativas à pasta atual, herdando RBAC.
    """
    # 1º Passo: pré-processar sintaxes exclusivas do Obsidian
    processed_text = process_obsidian_syntax(text, current_folder, vault_dir)

    # 2º Passo: renderizar Markdown tradicional
    raw_html = md.markdown(
        processed_text,
        extensions=["fenced_code", "tables", "toc"],
    )

    # 3º Passo: sanitizar o HTML contra XSS
    return bleach.clean(raw_html, tags=_ALLOWED_TAGS, attributes=_ALLOWED_ATTRS, strip=False)
