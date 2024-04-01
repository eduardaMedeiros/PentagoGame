import re, copy

BOLA_PRETA = '\033[30m' + '●' + '\033[0;0m'
BOLA_BRANCA = '\033[37m' + '●' + '\033[0;0m'

class Pentago:
    def __init__(self):
        self.branco_venceu = False
        self.preto_venceu = False

        self.utilidade_max = 1000
        self.utilidade_min = -1000

        self.venceu = False
        self.empatou = False

        self.primeira_jogada_turno = True

        self.blocos = []

        for i in range(4):
            posicoes = [None] * 9 
            self.blocos.append(posicoes)

    def verifica_ganhador(self):
        branco = self.calcular_utilidade(BOLA_BRANCA, BOLA_PRETA)
        preto = -self.calcular_utilidade(BOLA_PRETA, BOLA_BRANCA)

        if (branco == self.utilidade_max):
            self.branco_venceu = True
        
        if (preto == self.utilidade_min):
            self.preto_venceu = True
        
        if (self.branco_venceu and self.preto_venceu):
            self.empatou = True
        elif (self.branco_venceu or self.preto_venceu):
            self.venceu = True
            
    def validar_jogada(self, jogada):
        parametros = re.split(' |/', jogada)

        if(len(parametros) < 3):
            print("Movimentação fora do padrão solicitado")
            return False

        if(parametros[0].isdigit() and parametros[1].isdigit() and parametros[2][0].isdigit()):
            bloco = int(parametros[0]) - 1
            posicao = int(parametros[1]) - 1
            bloco_rotacao = int(parametros[2][0]) - 1

            if((bloco < 0 or bloco > 3) or (posicao < 0 or posicao > 8)):
                print("Movimento inválido")
                return False
            elif (self.blocos[bloco][posicao] != None):
                print("Movimento inválido")
                return False
            
            if(bloco_rotacao < 0 or bloco_rotacao > 3):
                print("Número do bloco para rotação inválido")
                return False    
        else:
            print("Dados inválidos. Os blocos e a posição devem ser enviadas no formato númerico")
            return False

        direcao_rotacao = parametros[2][1]
        if(direcao_rotacao not in ("l", "r", "L", "R")):
            print("Rotação inválida")
            return False
        
        return True

    def jogar(self, jogada):
        def convert(linha, coluna):
            return linha * 3 + coluna
        
        if (self.primeira_jogada_turno):
            jogador = BOLA_BRANCA
        else:
            jogador = BOLA_PRETA
        
        parametros = re.split(' |/', jogada)
        bloco = int(parametros[0]) - 1
        posicao = int(parametros[1]) - 1

        bloco_rotacao = int(parametros[2][0]) - 1
        direcao_rotacao = parametros[2][1]

        self.blocos[bloco][posicao] = jogador
        self.verifica_ganhador()

        temp = [None] * 9
            
        for linha in range(3):
            for coluna in range(3):
                if (direcao_rotacao in ("L", "l")):
                    temp[convert(2 - coluna, linha)] = self.blocos[bloco_rotacao][convert(linha, coluna)] 
                else:
                    temp[convert(coluna, 2 -linha)] = self.blocos[bloco_rotacao][convert(linha, coluna)]
        
        self.blocos[bloco_rotacao] = temp
        self.verifica_ganhador()
        self.primeira_jogada_turno = not self.primeira_jogada_turno
            

    def jogadas_possiveis(self):
        jogadas = []

        for bloco in range(4):
            for posicao in range(9):
                for rbloco in range(4):
                    if(self.blocos[bloco][posicao] == None):
                        jogadas.append(str(bloco + 1) + "/" + str(posicao + 1) + " " + str(rbloco + 1) + "L")
                        jogadas.append(str(bloco + 1) + "/" + str(posicao + 1) + " " + str(rbloco + 1) + "R")
        
        return jogadas
    
    def utilidade(self):
        branco = self.calcular_utilidade(BOLA_BRANCA, BOLA_PRETA)
        preto = -self.calcular_utilidade(BOLA_PRETA, BOLA_BRANCA)

        return branco if self.primeira_jogada_turno else preto
    
    def utilidades(self):
        branco = self.calcular_utilidade(BOLA_BRANCA, BOLA_PRETA)
        preto = -self.calcular_utilidade(BOLA_PRETA, BOLA_BRANCA)
        
        return branco + preto
    
    def pegar_linhas(self):
        lista = []

        def convert(linha, coluna):
            def convert_inner(linha, coluna):
                return linha * 3 + coluna

            posicao = convert_inner(linha % 3, coluna % 3)
            bloco = 2 * int(linha / 3) + int(coluna / 3) 

            return bloco, posicao

        for r in range(6):
            for c in range(6):
                bloco, posicao = convert(r, c)
                lista.append(self.blocos[bloco][posicao])
      
        matrix = [lista[i * 6:(i + 1) * 6] for i in range(6)]
        linhas = matrix + list(map(list, zip(*matrix)))

        linhas.append([matrix[i][i] for i in range(6)])
        linhas.append([matrix[i + 1][i] for i in range(5)])
        linhas.append([matrix[i][i + 1] for i in range(5)])
        linhas.append([matrix[i][5 - i] for i in range(6)])
        linhas.append([matrix[i + 1][5 - i] for i in range(5)])
        linhas.append([matrix[i][4 - i] for i in range(5)])

        return linhas
    
    def verificar_sequencia(self, linha, jogador, tamanho):
        string = ''.join(map(str, linha))
        sequencia = jogador * tamanho
        return sequencia in string
    
    def calcular_utilidade(self, max, min):
        linhas = self.pegar_linhas()

        utilidade = 0
        scores = [1, 10, 100]

        for linha in linhas:
            if self.verificar_sequencia(linha, max, 5):
                return self.utilidade_max
        
            if self.verificar_sequencia(linha, min, 5):
                return self.utilidade_min
        
        for linha in linhas:
            if self.verificar_sequencia(linha, max, 4):
                utilidade += scores[2]
                pass
            elif self.verificar_sequencia(linha, max, 3):
                utilidade += scores[1]
                pass
            elif self.verificar_sequencia(linha, max, 2):
                utilidade += scores[0]
            
        for linha in linhas:
            if self.verificar_sequencia(linha, min, 4):
                utilidade -= scores[2]
                pass
            elif self.verificar_sequencia(linha, min, 3):
                utilidade -= scores[1]
                pass
            elif self.verificar_sequencia(linha, min, 2):
                utilidade -= scores[0]
    
        if utilidade == 0:
            for i in range(4):
                if self.blocos[i][4] == max:
                    utilidade += 2
                if self.blocos[i][4] == min:
                    utilidade -= 2
     
        return utilidade
        
    def pegar_jogador_posicao(self, bloco, posicao):
        return self.blocos[bloco][posicao]
    
    def __str__(self):
        comeco = '\033[1;31m' + "+-------+-------+\n" + '\033[0;0m' 
        texto = [comeco]

        for bloco in range(2, 5, 2):
            for i in range(0, 7, 3):
                for j in range(bloco - 2, bloco):
                    texto.append('\033[1;31m' + "| " + '\033[0;0m')
                    for k in range(3):
                        val = self.pegar_jogador_posicao(j, i + k)
                        texto.append(val + " ") if val != None else texto.append('\033[1;31m' + "• " + '\033[0;0m')

                texto.append('\033[1;31m' + "|\n" + '\033[0;0m')
            texto.append(comeco)
            
        return ''.join(texto)

    def copy(self):
        return copy.deepcopy(self)