class jogo:  
    def __init__(self, id):
        self.j1Went = False #define se o jogador 1 fez ou não sua jogada
        self.j2Went = False #define se o jogador 2 fez ou não sua jogada 
        self.id = id  #cada jogo tem seu próprio id, para identificar que clientes pertencem a qual jogo
        self.mov = [None, None] 
       

    def get_player_move(self, jogador): # pega o movimento do jogador( , onde jogador 1 = 0 e jogador 2 = 1
        return self.mov[jogador]
    
    def jogador(self, jogador, move): #atualiza os movimentos com a jogada do jogador  
       jogadas_validas = ["pedra", "papel", "tesoura"]
       self.mov[jogador] = move.strip().lower()
       if self.mov[jogador] not in jogadas_validas:
           raise ValueError("Jogada inválida. Use: pedra, papel ou tesoura.")
       if jogador == 0:
           self.j1Went = True
       else: 
           self.j2Went = True

    
    
    def bothWent(self): #determina se os dois jogadores fizeram suas jogadas 
        return self.j1Went and self.j2Went 
    
    def vencedor(self):   #define quem ganhou o jogo 
        j1 = self.mov[0]
        j2 = self.mov[1]

        vencedor = -1  # pedra papel, tesoura 
        if j1 == "pedra" and j2 == "tesoura": 
            vencedor = 0
            print("O jogador 1 Venceu!")
        elif j1 == "tesoura" and j2 == "pedra":  
            vencedor = 1 
            print("O jogador 2 Venceu!")
        elif j1 == "papel" and j2 == "pedra": 
            vencedor = 0 
            print("O jogador 1 Venceu!")
        elif j1 == "pedra" and j2 == "papel":
            vencedor = 1 
            print("O jogador 2 Venceu!")
        elif j1 == "tesoura" and j2 == "papel": 
            vencedor = 0 
            print("O jogador 1 Venceu!")
        elif j1 == "papel" and j2 == "tesoura": 
            vencedor = 1
            print("O jogador 2 Venceu!")
        elif j1 == j2: 
            print("O jogo Empatou!")


        return vencedor  
    
    def reset(self): #reseta as jogadas 
        self.j1Went = False 
        self.j2Went = False 
        self.mov = [None, None]
       


