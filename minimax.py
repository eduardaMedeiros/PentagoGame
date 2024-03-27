class IA:
    def __init__(self, type):
        self.algortimo = None
        self.visitado = dict()

        self.nos_expandidos = 0
        self.profundidade_expandida = 0

        if type == 0:
            self.algortimo = self.minimax
        else:
            self.algortimo = self.alpha_beta
    
    def minimax(self, jogo, profundidade_max, profundidade = 0):
        melhores_jogadas = [None]

        def minimax_auxiliar(IA, jogo, profundidade_max, profundidade, melhores_jogadas):
            IA.profundidade_expandida = max(IA.profundidade_expandida, profundidade)

            if(profundidade >= profundidade_max):
                return jogo.utilidades()
            elif(jogo.utilidade() == jogo.utilidade_ganhador):
                return jogo.utilidade_ganhador
            elif(jogo.utilidade() == jogo.utilidade_perdedor):
                return jogo.utilidade_perdedor
            else:
                jogadas_possiveis = jogo.jogadas_possiveis()

                melhor_jogada = None
                melhor_utilidade = None

                for jogada in jogadas_possiveis:
                    proximo = jogo.copy()
                    proximo.jogar(jogada)

                    if(str(proximo.blocos) in IA.visitado):
                        proximo_utilidade = IA.visitado[str(proximo.blocos)]
                    else:
                        proximo_utilidade = minimax_auxiliar(IA, proximo, profundidade_max, profundidade+1, melhores_jogadas)
                        IA.visitado[str(proximo.blocos)] = proximo_utilidade
                    
                    IA.nos_expandidos += 1
                    if(melhor_jogada == None):
                        melhor_jogada = jogada
                        melhor_utilidade = proximo_utilidade
                    
                    if(melhor_utilidade < proximo_utilidade if jogo.primeira_jogada_turno else melhor_utilidade > proximo_utilidade):
                        melhor_jogada = jogada
                        melhor_utilidade = proximo_utilidade
                    
                melhores_jogadas[0] = melhor_jogada
                return int(melhor_utilidade)
            
        minimax_auxiliar(self, jogo, profundidade_max, profundidade, melhores_jogadas)
        return melhores_jogadas[0]
    
    def alpha_beta(self, jogo, profundidade_max, profundidade=0):
        melhores_jogadas = [None]

        def alpha_beta_auxiliar(IA, jogo, profundidade_max, profundidade, alpha, beta, melhores_jogadas):
            IA.profundidade_expandida = max(IA.profundidade_expandida, profundidade)

            if(profundidade >= profundidade_max):
                return jogo.utilidades()
            elif(jogo.utilidade() == jogo.utilidade_ganhador):
                return jogo.utilidade_ganhador
            elif(jogo.utilidade() == jogo.utilidade_perdedor):
                return jogo.utilidade_perdedor
            else:
                jogadas_possiveis = jogo.jogadas_possiveis()

                melhor_jogada = None
                melhor_utilidade = None

                for jogada in jogadas_possiveis:
                    proximo = jogo.copy()
                    proximo.jogar(jogada)

                    if(str(proximo.blocos) in IA.visitado):
                        proximo_utilidade = IA.visitado[str(proximo.blocos)]
                    else:
                        proximo_utilidade = alpha_beta_auxiliar(IA, proximo, profundidade_max, profundidade+1, alpha, beta, melhores_jogadas)
                        IA.visitado[str(proximo.blocos)] = proximo_utilidade

                    IA.nos_expandidos += 1
                    if(melhor_jogada == None):
                        melhor_jogada = jogada
                        melhor_utilidade = proximo_utilidade
                    
                    if(melhor_utilidade < proximo_utilidade if jogo.primeira_jogada_turno else melhor_utilidade > proximo_utilidade):
                        melhor_jogada = jogada
                        melhor_utilidade = proximo_utilidade

                    if(jogo.primeira_jogada_turno):
                        alpha = max(alpha, int(proximo_utilidade))
                    else:
                        beta = min(beta, int(proximo_utilidade))
                    
                    if(beta <= alpha):
                        break
                    
                melhores_jogadas[0] = melhor_jogada
                return int(melhor_utilidade)
        
        alpha_beta_auxiliar(self, jogo, profundidade_max, profundidade, float("-inf"), float("inf"), melhores_jogadas)
        return melhores_jogadas[0]
    
    def jogar(self, jogo, profundidade_max = 2):
        self.nos_expandidos = 0
        self.profundidade_expandida = 0

        jogada = self.algortimo(jogo, profundidade_max)
        jogo.jogar(jogada)

        print("Nós expandidos:", self.nos_expandidos)
        print("Profundidade expandida:", self.profundidade_expandida, "\n")

        self.visitado.clear()
        return jogada 

            