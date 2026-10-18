"""CONFIGURAÇÕES DE EMAIL"""

import os

class EmailConfig:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    CODIGO_TAMANHO = 6
    CODIGO_EXPIRACAO_MINUTOS = 15
    MAX_TENTATIVAS = 5