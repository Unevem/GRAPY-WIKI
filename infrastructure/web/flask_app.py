import os
import sys

# Garante que a raiz do projeto (dois níveis acima deste arquivo) esteja
# no sys.path, permitindo imports absolutos como 'from domain.services...'
# independente do diretório de onde o Flask é executado.
_PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from flask import Flask
from .routes import web_bp


def create_app() -> Flask:
    """
    Factory da aplicação Flask.

    Separa a criação da instância da sua execução, permitindo
    diferentes configurações para desenvolvimento, teste e produção
    sem alterar o código-fonte.
    """
    # Resolve os caminhos relativos a partir da localização deste arquivo,
    # garantindo que funcionem independente do diretório de execução.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(base_dir, "..", "..", "presentation", "templates")
    static_dir = os.path.join(base_dir, "..", "..", "presentation", "static")

    app = Flask(
        __name__,
        template_folder=os.path.normpath(template_dir),
        static_folder=os.path.normpath(static_dir),
    )

    # SECRET_KEY protege cookies assinados e sessões (necessário para o futuro RBAC)
    app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))

    # DEBUG nunca deve ser True em produção (expõe Werkzeug Debugger interativo)
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

    # Registro de Blueprints (Controllers no MVC)
    app.register_blueprint(web_bp)

    return app
