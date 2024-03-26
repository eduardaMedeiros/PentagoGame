import re

class Pentago:
    def __init__(self):
        self.branco_venceu = False
        self.preto_venceu = False

        self.utilidade_ganhador = 1000
        self.utilidade_perdedor = -1000

        self.venceu = False
        self.empatou = False

        self.primeira_jogada_turno = True

        self.blocos = []

        for i in range(4):
            posicoes = [None] * 9 
            self.blocos.append(posicoes)

    def jogar(self, jogada):
        def convert(linha, coluna):
            return linha * 3 + coluna
        
        parametros = re.split(' |/', jogada)

        bloco = int(parametros[0]) - 1
        posicao = int(parametros[1]) - 1

        bloco_rotacao = int(parametros[2][0]) - 1
        direcao_rotacao = parametros[2][1]

        if self.primeira_jogada_turno:
            jogador = "⚪"
        else:
            jogador = "⚫"

        if self.blocos[bloco][posicao] != None and direcao_rotacao.upper() != "l" and direcao_rotacao.upper() != "r":
            print("Movimento inválido")
        else:
            self.blocos[bloco][posicao] = jogador
            self.verifica_ganhador()
            
            temp = [None] * 9
            
            for linha in range(3):
                for coluna in range(3):
                    if direcao_rotacao.upper() == "l":
                        temp[convert(2 - coluna, linha)] = self.blocos[bloco_rotacao][convert(linha, coluna)] 
                    else:
                        temp[convert(coluna, 2 -linha)] = self.blocos[bloco_rotacao][convert(linha, coluna)]
        
            self.blocos[bloco_rotacao] = temp
            self.verifica_ganhador()
            self.primeira_jogada_turno = not self.primeira_jogada_turno

    def jogadas_potenciais(self):
        jogadas = []

        for bloco in range(4):
            for posicao in range(9):
                for rbloco in range(4):
                    if(self.blocos[bloco][posicao] == None):
                        jogadas.append(str(bloco + 1) + "/" + str(posicao + 1) + " " + str(rbloco + 1) + "L")
                        jogadas.append(str(bloco + 1) + "/" + str(posicao + 1) + " " + str(rbloco + 1) + "R")
        
        return jogadas
    
    def utilidade(self):
        branca, preta = self.calcula_utilidade()
        return branca if self.primeira_jogada_turno else preta
    
    def utilidades(self):
        branca, preta = self.calcula_utilidade()
        return branca + preta
    
    def calcula_utilidade(self):
        def convert(linha, coluna):
            def convert_inner(linha, coluna):
                return linha * 3 + coluna

            posicao = convert_inner(linha % 3, coluna % 3)
            bloco = 2 * int(coluna / 3) + int(linha / 3)

            return bloco, posicao
        
        qtd_brancas = 0
        qtd_pretas = 0

        brancas_meio = 0
        pretas_meio = 0

        #horizontal
        for r in range(6):
            brancas = 0
            pretas = 0
            for c in range(6):
                bloco, posicao = convert(r, c)
                if (self.blocos[bloco][posicao] == "⚪"):
                    if ((r == 1 or r == 4) and (c == 1 or c == 4)):
                        brancas_meio += 1
                    brancas += 1
                    pretas = 0
                elif (self.blocos[bloco][posicao] == "⚫"):
                    if ((r == 1 or r == 4) and (c == 1 or c == 4)):
                        pretas_meio += 1
                    pretas += 1
                    brancas = 0
                else:
                    brancas = 0
                    pretas = 0

            qtd_brancas = max(qtd_brancas, brancas)
            qtd_pretas = max(qtd_pretas, pretas)

        #vertical
        for c in range(6):
            brancas = 0
            pretas = 0
            for r in range(6):
                bloco, posicao = convert(r, c)
                if (self.blocos[bloco][posicao] == "⚪"):
                    brancas += 1
                    pretas = 0
                elif (self.blocos[bloco][posicao] == "⚫"):
                    pretas += 1
                    brancas = 0
                else:
                    brancas = 0
                    pretas = 0

            qtd_brancas = max(qtd_brancas, brancas)
            qtd_pretas = max(qtd_pretas, pretas)

        #diagonal
        for d in range(2):
            for i in range(6):
                brancas = 0
                pretas = 0

                for j in range(6 - i):
                    bloco, posicao = convert(j + i, j) if d == 0 else convert(j, j + i)
                    if (self.blocos[bloco][posicao] == "⚪"):
                        brancas += 1
                        pretas = 0
                    elif (self.blocos[bloco][posicao] == "⚫"):
                        pretas += 1
                        brancas = 0
                    else:
                        brancas = 0
                        pretas = 0

                    qtd_brancas = max(qtd_brancas, brancas)
                    qtd_pretas = max(qtd_pretas, pretas)
        
        #canto esquerdo e direito
        for d in range(2):
            for i in range(6):
                brancas = 0
                pretas = 0

                for j in range(6 - i):
                    bloco, posicao = convert(5 - (j + i), j) if d == 0 else convert(5 - j, j + i)
                    if (self.blocos[bloco][posicao] == "⚪"):
                        brancas += 1
                        pretas = 0
                    elif (self.blocos[bloco][posicao] == "⚫"):
                        pretas += 1
                        brancas = 0
                    else:
                        brancas = 0
                        pretas = 0

                    qtd_brancas = max(qtd_brancas, brancas)
                    qtd_pretas = max(qtd_pretas, pretas)
        
        return qtd_brancas * 5 + brancas_meio if (qtd_brancas < 5) else self.utilidade_ganhador, \
               -qtd_pretas * 5 - pretas_meio if  (qtd_pretas < 5) else self.utilidade_perdedor

    def verifica_ganhador(self):
        branco, preto = self.calcula_utilidade()

        if branco == self.utilidade_ganhador:
            self.branco_venceu = True
        
        if preto == self.utilidade_ganhador:
            self.preto_venceu = True
        
        if self.branco_venceu and self.preto_venceu:
            self.empatou = True
        elif self.branco_venceu or self.preto_venceu:
            self.venceu = True

    def pegar_jogador_posicao(self, bloco, posicao):
        return self.blocos[bloco][posicao]
    
    def __str__(self):
        comeco = "+-------+-------+\n"
        texto = [comeco]

        for bloco in range(2, 5, 2) :
            for i in range(0, 7, 3) :
                for j in range (bloco - 2, bloco):
                    texto.append("| ")
                    for k in range(3):
                        val = self.pegar_jogador_posicao(j, i + k)
                        texto.append(val) if val != None else texto.append(". ")
                
                texto.append("|\n")
            
            texto.append(comeco)
        return ''.join(texto)


        

    

    





        