import random
import smtplib
import email.message

def gerarNumero():
    return random.randint(1,10000)

def dicionarioEmail(tipo,mensagem):
    corpo_do_email_senha = f"""
            <p>Acho que você esqueceu sua senha!</p>

            <p>A sua senha é esta daqui: {mensagem}</p>
            
            <p>Não a perca novamente em!</p>

            <p>Att,</p>
            <p>ADM.</p>
        """

    corpo_do_email_confirmacao = f"""
                <p>Para sua segurança, favor confirmar o seu email!</p>

                <p>Este é o seu código de confirmaçãoo: {mensagem}</p>

                <p>Cole este código na entrada do programa para confirmar este email!</p>

                <p>Att,</p>
                <p>ADM.</p>
            """

    dic = {'senha':corpo_do_email_senha,'confirmar':corpo_do_email_confirmacao}

    return dic[tipo]

def envioEmail(destino,assunto,mensagem,tipo):

    try:
        corpo_do_email = dicionarioEmail(tipo,mensagem)
        msg = email.message.Message()
        msg['Subject'] = assunto
        msg['From'] = 'dizimistasadm@gmail.com'
        msg['To'] = destino
        password = 'ghwabhhapqdgpuxk'
        msg.add_header('Content-Type','text/html')
        msg.set_payload(corpo_do_email)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()

        s.login(msg['From'],password)
        s.sendmail(msg['From'],[msg['To']],msg.as_string().encode('utf-8'))
        return True

    except Exception:
        return False