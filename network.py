from jogo import *
from servidor import *


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

def determinarVencedor(jogadaLocal, jogadaOponente):
    if jogadaLocal == jogadaOponente:
        return -1 #empate
    
    regrasVitoria = { 
        'r' : 't',
        'p' : 'r',
        't' : 'p'
    }

    if regrasVitoria[jogadaLocal] == jogadaOponente:
        return 0 #jogador local venceu
    else:
        return 1 #oponente venceu
    
def server():
    ip, protocolo, conexao, porta = configurarRede

    sock = None
    conn = None #tcp
    endOponente = None #udp

    #identificar host e jogador conectado

    if conexao == 'h': #hospedar
        meuId = 0
        print(f'\n ---> Hospedando partida em {ip}:{porta} usando {protocolo}.')
    else: #conectar-se
        meuId = 1
        print(f'\n---> Conectando a {ip}:{porta} usando {protocolo}...')

    sock = createSocket(protocolo, ip, porta)

    if meuId == 0: #jogador host
        sock.bind((ip, porta))
        if protocolo == 'tcp':
            sock.listen(1)
            print('[ Aguardando conexão do oponente... ]')
            conn, addr = sock.accept()
            print(f'[ Oponente conectado de {addr}. Partida iniciada. ]')
            sockComunicar = conn
        else:
            print('[ Aguardando mensagem do oponente para iniciar... ]')
            dadosIniciais, endOponente = receberMsg(sock,'udp')
            if dadosIniciais and dadosIniciais.get('status') == 'iniciar':
                print(f'[ Oponente conectado de {endOponente}. Partida iniciada. ]')
            else:
                print('[ Falha ao estabelecer conexão. ]')
                sock.close()
                return
            sockComunicar = sock
    else: #jogador conectado
        endOponente = (ip, porta)
        if protocolo == 'tcp':
            try:
                sock.connect(endOponente)
                print('[ Conectando-se a partida. Partida inciada. ]')
            except ConnectionRefusedError:
                print('[ Conexão recusada. ]')
                return
            sockComunicar = sock
        else: #udp
            enviarMsg(sock, {'status':'iniciar'}, 'udp', endOponente)
            print('[ Mensagem inicial enviada. Aguardando jogada do host...]')
            sockComunicar = sock
    # PARTIDA
    
