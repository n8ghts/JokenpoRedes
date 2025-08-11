class jogo:  
    def __init__(self, id):
        self.j1Went = False #define se o jogador 1 fez ou não sua jogada
        self.j2Went = False #define se o jogador 2 fez ou não sua jogada
        self.ready = False 
        self.id = id  #cada jogo tem seu próprio id, para identificar que clientes pertencem a qual jogo
        self.mov = [None, None] 
        self.vitoria = [0, 0] 
        self.empate = 0 

    def get_player_move(self, j): # pega o movimento do jogador , onde jogador 1 = 0 e jogador 2 = 1
        return self.mov[j]
    
    def jogador(self, jogador, move): #atualiza os movimentos com a jogada do jogador  
        self.mov[jogador] = move
        if jogador == 0: 
            self.j1Went = True 
        else: 
            self.j2Went = True 

    def conexao(self):  #determina se os jogadores estão ou não conectados 
        return self.ready 
    
    def bothWent(self): #determina se os dois jogadores fizeram suas jogadas 
        return self.j1Went and self.j2Went 
    
    def vencedor(self):   #define quem ganhou o jogo 
        j1 = self.mov[0].upper() [0] 
        j2 = self.mov[1].upper() [0]

        vencedor = -1  # R = Rocha, P = Papel, T = Tesoura 
        if j1 == "R" and j2 == "T": 
            vencedor = 0
            print("O jogador 1 Venceu!")
        elif j1 == "T" and j2 == "R":  
            vencedor = 1 
            print("O jogador 2 Venceu!")
        elif j1 == "P" and j2 == "R": 
            vencedor = 0 
            print("O jogador 1 Venceu!")
        elif j1 == "R" and j2 == "P":
            vencedor = 1 
            print("O jogador 2 Venceu!")
        elif j1 == "T" and j2 == "P": 
            vencedor = 0 
            print("O jogador 1 Venceu!")
        elif j1 == "P" and j2 == "T": 
            vencedor = 1
            print("O jogador 2 Venceu!")
        elif j1 == j2: 
            print("O jogo Empatou!")


        return vencedor  
    
    def resetWent(self): #reseta as jogadas 
        self.j1Went = False 
        self.j2Went = False 

