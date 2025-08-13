import socket
from servidor import familiaIP, createSocket, enviarMsg, receberMsg


def configurarRede(): # configura os dados da conexão
        ip = input('Insira o endereço ip:')
        while True:
            protocolo = input('Insira o protocolo (tcp ou udp):'.lower)
            if protocolo in ['tcp','udp']:
                  break
            print('Protocolo Inválido.')

        while True:
            conexao = input('Conectar-se a uma partida ou hostear? (c/h)'.lower)
            if conexao in ['c','h']:
                break
            print('Modo inválido.')
        
        while True:
            try:
                porta = int(input('Insira o número de porta: '))
                if 1024 <= porta <= 65535:
                    break
            except ValueError:
                print('Porta inválida. Tente novamente.')

        return ip, protocolo, conexao, porta

def server():
    ip, protocolo, conexao, porta = configurarRede

    sock = createSocket(protocolo, ip, porta)
    if protocolo.lower() == 'tcp':
        sock.listen()
        conn, addr = sock.accept()
        print(f'Jogador conectado de {addr} Iniciando partida...')
        #sock_comunicacao = conn
    else:
        


