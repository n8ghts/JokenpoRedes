import json
import socket
import ipaddress

def familiaIP(host):
    try:
        ip = ipaddress.ip_address(host) #cria o objeto ip

        if isinstance(ip,ipaddress.IPv4Address):
            return socket.AF_INET #endereço ipv4
        elif isinstance(ip,ipaddress.IPv6Address):
            return socket.AF_INET6 #endereço ipv6
    except ValueError:
        raise ValueError(f"IP inválido: {host}") 
    
def createSocket(protocolo, host, porta):
    familia = familiaIP(host) #puxa a familia da função
    if protocolo.lower() == 'tcp':
        tipoSocket = socket.SOCK_STREAM
    else:
        tipoSocket = socket.SOCK_DGRAM #tipo udp
    
    sock = socket.socket(familia, tipoSocket) #cria o socket e recebe os dados
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #previne erro de endereço já utilizado
    return sock

def enviarDados(sock, dados, protocolo, endOponente = None):
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

def receberDados(sock, protocolo, buffer = 1024):
    try:
        if protocolo.lower() == 'tcp':
            enviar = sock.recv(buffer) #recebe os dados do socket
            if not enviar:
                return None, None
            endOponente = None #não precisa
        else:
            enviar, endOponente = sock.recvfrom(buffer)
        
        dados = json.loads(enviar.decode('utf-8')) #desserializa
        return dados, endOponente
    except (socket.error, json.JSONDecodeError, ConnectionResetError) as e:
        print(f'erro: {e}')
        return None, None