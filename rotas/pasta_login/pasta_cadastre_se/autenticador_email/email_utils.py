"""UTILITÁRIOS DE EMAIL"""

import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from utils.database.conexao_global import ini_conexao

from rotas.pasta_login.pasta_cadastre_se.autenticador_email.config_email import EmailConfig


def gerar_codigo():
    """Gera código de 6 dígitos aleatório"""
    return ''.join(random.choices(string.digits, k=EmailConfig.CODIGO_TAMANHO))


def enviar_email_confirmacao(email_destino, codigo):
    """Envia email com código de confirmação"""
    try:
        msg = MIMEMultipart()
        msg['Subject'] = 'Confirme seu cadastro — MeuLinks'
        msg['From'] = EmailConfig.MAIL_DEFAULT_SENDER
        msg['To'] = email_destino

        corpo = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Bem-vindo ao MeuLinks!</h2>
            <p>Para confirmar seu cadastro, utilize o código abaixo:</p>
            <div style="background-color: #f0f0f0; padding: 15px; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 5px;">
                {codigo}
            </div>
            <p>Este código expira em {EmailConfig.CODIGO_EXPIRACAO_MINUTOS} minutos.</p>
            <p>Se não foi você quem solicitou, ignore este email.</p>
            <hr>
            <small>MeuLinks — Seus links em uma única página</small>
        </body>
        </html>
        """

        msg.attach(MIMEText(corpo, 'html'))

        with smtplib.SMTP(EmailConfig.MAIL_SERVER, EmailConfig.MAIL_PORT) as server:
            server.starttls()
            server.login(EmailConfig.MAIL_USERNAME, EmailConfig.MAIL_PASSWORD)
            server.send_message(msg)

        return True, "Email enviado com sucesso!"

    except Exception as e:
        return False, f"Erro ao enviar email: {str(e)}"


def enviar_email_recuperacao(email_destino, codigo):
    """Envia email com código de recuperação de senha"""
    try:
        msg = MIMEMultipart()
        msg['Subject'] = 'Recuperação de Senha — MeuLinks'
        msg['From'] = EmailConfig.MAIL_DEFAULT_SENDER
        msg['To'] = email_destino

        corpo = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Recuperação de Senha</h2>
            <p>Você solicitou a recuperação de senha. Utilize o código abaixo:</p>
            <div style="background-color: #f0f0f0; padding: 15px; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 5px;">
                {codigo}
            </div>
            <p>Este código expira em {EmailConfig.CODIGO_EXPIRACAO_MINUTOS} minutos.</p>
            <p>Se não foi você quem solicitou, ignore este email.</p>
            <hr>
            <small>MeuLinks</small>
        </body>
        </html>
        """

        msg.attach(MIMEText(corpo, 'html'))

        with smtplib.SMTP(EmailConfig.MAIL_SERVER, EmailConfig.MAIL_PORT) as server:
            server.starttls()
            server.login(EmailConfig.MAIL_USERNAME, EmailConfig.MAIL_PASSWORD)
            server.send_message(msg)

        return True, "Email enviado com sucesso!"

    except Exception as e:
        return False, f"Erro ao enviar email: {str(e)}"


def salvar_codigo_verificacao(user_id, codigo):
    """Salva código de verificação"""
    expiracao = datetime.now() + timedelta(minutes=EmailConfig.CODIGO_EXPIRACAO_MINUTOS)
    conexao, cursor = ini_conexao()

    cursor.execute("""
        UPDATE usuarios
        SET codigo_verificacao = %s,
            codigo_expiracao = %s,
            tentativas_verificacao = 0
        WHERE id = %s
    """, (codigo, expiracao, user_id))
    conexao.commit()


def verificar_codigo(user_id, codigo_digitado):
    """Verifica código de confirmação"""
    conexao, cursor = ini_conexao()

    cursor.execute("""
        SELECT codigo_verificacao, codigo_expiracao, tentativas_verificacao
        FROM usuarios WHERE id = %s
    """, (user_id,))
    resultado = cursor.fetchone()

    if not resultado:
        return False, "Usuário não encontrado"

    codigo_salvo, expiracao, tentativas = resultado

    if tentativas >= EmailConfig.MAX_TENTATIVAS:
        return False, "Muitas tentativas. Solicite um novo código."

    if expiracao and datetime.now() > expiracao:
        return False, "Código expirado. Solicite um novo."

    if codigo_salvo != codigo_digitado:
        cursor.execute(
            "UPDATE usuarios SET tentativas_verificacao = tentativas_verificacao + 1 WHERE id = %s",
            (user_id,)
        )
        conexao.commit()
        return False, f"Código inválido. Você tem mais {EmailConfig.MAX_TENTATIVAS - tentativas - 1} tentativas."

    cursor.execute("""
        UPDATE usuarios
        SET email_verificado = 1,
            codigo_verificacao = NULL,
            codigo_expiracao = NULL,
            tentativas_verificacao = 0
        WHERE id = %s
    """, (user_id,))
    conexao.commit()

    return True, "Email verificado com sucesso!"


def salvar_codigo_recuperacao(email, codigo):
    """Salva código de recuperação"""
    expiracao = datetime.now() + timedelta(minutes=EmailConfig.CODIGO_EXPIRACAO_MINUTOS)
    conexao, cursor = ini_conexao()

    cursor.execute("""
        UPDATE usuarios
        SET codigo_recuperacao = %s,
            codigo_recuperacao_expiracao = %s,
            tentativas_recuperacao = 0
        WHERE email = %s
    """, (codigo, expiracao, email))
    conexao.commit()


def verificar_codigo_recuperacao(email, codigo_digitado):
    """Verifica código de recuperação"""
    conexao, cursor = ini_conexao()

    cursor.execute("""
        SELECT id, codigo_recuperacao, codigo_recuperacao_expiracao, tentativas_recuperacao
        FROM usuarios WHERE email = %s
    """, (email,))
    resultado = cursor.fetchone()

    if not resultado:
        return False, "Email não encontrado", None

    user_id, codigo_salvo, expiracao, tentativas = resultado

    if tentativas >= EmailConfig.MAX_TENTATIVAS:
        return False, "Muitas tentativas. Solicite um novo código.", None

    if expiracao and datetime.now() > expiracao:
        return False, "Código expirado. Solicite um novo.", None

    if codigo_salvo != codigo_digitado:
        cursor.execute(
            "UPDATE usuarios SET tentativas_recuperacao = tentativas_recuperacao + 1 WHERE email = %s",
            (email,)
        )
        conexao.commit()
        return False, f"Código inválido. Você tem mais {EmailConfig.MAX_TENTATIVAS - tentativas - 1} tentativas.", None

    cursor.execute("""
        UPDATE usuarios
        SET codigo_recuperacao = NULL,
            codigo_recuperacao_expiracao = NULL,
            tentativas_recuperacao = 0
        WHERE email = %s
    """, (email,))
    conexao.commit()

    return True, "Código válido!", user_id