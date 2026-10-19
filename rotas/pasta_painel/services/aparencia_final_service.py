"""APARÊNCIA FINAL — Service (orquestra config + template + merge)"""

import logging
from utils.config.merge import merge_recursivo
from .aparencia_config_service import AparenciaConfigService
from .template_service import TemplateService

logger = logging.getLogger(__name__)


class AparenciaFinalService:

    def __init__(self, conexao, cursor):
        self.conexao = conexao
        self.cursor = cursor
        self.config = AparenciaConfigService(conexao, cursor)
        self.template = TemplateService(conexao, cursor)

    def _merge(self, template_slug, user_config):
        template = self.template.buscar_por_slug(template_slug)
        if not template:
            return user_config or {}
        return merge_recursivo(template['config_default'], user_config or {})

    def buscar_por_usuario(self, usuario_id):
        """Retorna {template_slug, config_final, config_user, template}."""
        perfil = self.config.buscar_por_usuario(usuario_id)
        if not perfil:
            return None

        template = self.template.buscar_por_slug(perfil['template_slug'])
        config_final = self._merge(perfil['template_slug'], perfil['config'])

        return {
            'template_slug': perfil['template_slug'],
            'config_final': config_final,
            'config_user': perfil['config'],
            'template': template,
        }

    def buscar_por_username(self, username):
        """Retorna {usuario_id, template_slug, config_final, config_user, template}."""
        perfil = self.config.buscar_por_username(username)
        if not perfil:
            return None

        template = self.template.buscar_por_slug(perfil['template_slug'])
        config_final = self._merge(perfil['template_slug'], perfil['config'])

        return {
            'usuario_id': perfil['usuario_id'],
            'template_slug': perfil['template_slug'],
            'config_final': config_final,
            'config_user': perfil['config'],
            'template': template,
        }