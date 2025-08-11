import json
import socket

def familiaIP(ip):
    try:
        if ':' in ip:
            return socket.AF_INET6 #ipv6
        else:
            return socket.AF_INET #ipv4
    except ValueError:
        raise ValueError(f"IP inválido: {ip}") 
    
def createSocket(protocolo, ip, porta):
    familia = familiaIP(ip) #puxa a familia da função
    if protocolo.lower() == 'tcp':
        tipo = socket.SOCK_STREAM
    else:
        tipo = socket.SOCK_DGRAM #tipo udp
    
    sock = socket.socket(familia, tipo) #cria o socket e recebe os dados
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #previne erro de endereço já utilizado
    return sock

def enviarMsg(sock, dados, protocolo, endOponente = None):
    enviar = json.dumps(dados).encode('UTF-8') #serializa os dados
    try:
        if protocolo.lower() == 'tcp': #tcp já tem o endereço da conexão
            sock.sendall(enviar) #envia os dados do socket
        else: #udp
            if endOponente:
                sock.sendto(enviar, endOponente) #envia os dados para o endereço informado
    except socket.error as e: #throws an exception
        print(f'erro: {e}')
        return False
    return True

def receberMsg(sock, protocolo):
    try:
        if protocolo.lower() == 'tcp':
            enviar = sock.recv(1024) #recebe os dados do socket
            if not enviar:
                return None, None
            endOponente = None #não precisa
        else:
            enviar, endOponente = sock.recvfrom(1024)
        
        dados = json.loads(enviar.decode('utf-8')) #desserializa
        return dados, endOponente
    except (socket.error, json.JSONDecodeError, ConnectionResetError) as e:
        print(f'erro: {e}')
        return None, None