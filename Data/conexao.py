import socket

def test_conexao(Host='8.8.8.8',port=53,timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET,socket.SOCK_STREAM).connect((Host,port))
        return True

    except Exception:
        return False