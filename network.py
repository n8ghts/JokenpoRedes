from jogo import *
from servidor import *


def configurarRede(): # configura os dados da conexão
    ip = input('Insira o endereço ip:')
    while True:
        protocolo = input('Insira o protocolo (tcp ou udp):'.lower())
        if protocolo in ['tcp','udp']:
            break
        print('Protocolo Inválido.')

    while True:
        conexao = input('Conectar-se a uma partida ou hostear? (c/h)'.lower())
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
    ip, protocolo, conexao, porta = configurarRede()

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
    partida = jogo(meuId) 
    print("\nDigite 'SAIR' a qualquer momento para encerrar a partida.")
    print('\n=== Início do Jogo Pedra-Papel-Tesoura ===\n')

    while True:
        # host joga primeiro, cliente aguarda, depois inverte
        sequence = [0, 1] if meuId == 0 else [1, 0]
        for jogador in sequence:
            prompt = 'Sua jogada' if jogador == meuId else 'Jogada do oponente recebida'
            if jogador == meuId:
                move = input(f'{prompt} (pedra/papel/tesoura): ').strip()
                if move.upper() == 'SAIR':
                    print('Encerrando partida a pedido do usuário.')
                    return

                try:
                    partida.jogador(meuId, move)
                except ValueError as ve:
                    print(ve)
                    # repete esse mesmo jogador
                    break

                # envia jogada
                msg = {'move': move.strip().lower()}
                if protocolo == 'udp':
                    enviarMsg(sockComunicar, msg, 'udp', endOponente) 
                else:
                    enviarMsg(sockComunicar, msg, 'tcp')

            else:
                # recebe a jogada do outro
                print('[ Aguardando jogada do oponente... ]')
                if protocolo == 'udp':
                    dados, _ = receberMsg(sockComunicar, 'udp')
                else:
                    dados, _ = receberMsg(sockComunicar, 'tcp')
                opp_move = dados.get('move')
                partida.jogador(1 - meuId, opp_move)
                print(f'{prompt}: {opp_move}')

        # só decide quando ambos jogaram
        if partida.bothWent():
            m1 = partida.get_player_move(0)
            m2 = partida.get_player_move(1)
            print(f'\nJogador 1 jogou: {m1}')
            print(f'Jogador 2 jogou: {m2}\n')

            partida.vencedor()

            # pergunta se quer resetar ou sair
            while True:
                escolha = input("\nDigite 'ENTER' para nova rodada ou 'SAIR' para encerrar: ").strip()
                if escolha.upper() == 'SAIR':
                    print('Encerrando partida. Até a próxima!')
                    sockComunicar.close()
                    if conn:
                        conn.close()
                    sock.close()
                    return
                else:
                    partida.reset()
                    print('\n=== Nova Rodada Iniciada ===\n')
                    break 
server() 
    