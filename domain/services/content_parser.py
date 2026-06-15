import re

class ContentParser:
    @staticmethod
    def extract_links(markdown_text: str) -> list[str]:
        """
        Extrai os links do formato Obsidian [[Link]] ou [[Link|Display]].
        Retorna uma lista de strings com os nomes dos arquivos alvo.
        """
        links = []
        matches = re.finditer(r'\[\[(.*?)\]\]', markdown_text)
        for match in matches:
            content = match.group(1)
            target = content.split('|')[0]
            links.append(target)
        return links
