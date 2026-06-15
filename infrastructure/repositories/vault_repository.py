import os

def get_directory_tree(vault_path: str) -> dict:
    """
    Varre a pasta raiz do vault de documentação.
    Retorna um dicionário onde a CHAVE é o nome da pasta (Role) e o VALOR
    é uma lista de dicionários contendo o nome do arquivo (sem .md) e o path.

    Ignora qualquer pasta ou arquivo oculto (que comece com '.').
    """
    tree = {}
    if not os.path.exists(vault_path):
        return tree

    # Lista apenas pastas do primeiro nível (ex: NOC, SUPORTE)
    for folder_name in os.listdir(vault_path):
        folder_path = os.path.join(vault_path, folder_name)

        if folder_name.startswith('.'):
            continue

        if os.path.isdir(folder_path):
            files_list = []
            
            # Varre os arquivos dentro dessa pasta
            for root, _, files in os.walk(folder_path):
                # Ignora pastas ocultas na varredura profunda também
                if any(part.startswith('.') for part in root.replace('\\', '/').split('/')):
                    continue
                
                for file in files:
                    if file.endswith('.md') and not file.startswith('.'):
                        name = file[:-3].replace("_", " ")  # remove .md e limpa os underlines
                        
                        # Calcula o caminho relativo desde a raiz do vault
                        # Ex: "NOC/Configurando_Radios.md"
                        full_file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_file_path, vault_path)
                        rel_path = rel_path.replace("\\", "/") # Garante barras normais
                        
                        files_list.append({
                            "name": name,
                            "path": rel_path
                        })
            
            if files_list:
                # Ordena os arquivos em ordem alfabética para a UI
                tree[folder_name] = sorted(files_list, key=lambda x: x["name"])

    return tree
