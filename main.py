import game as pg
import minimax as ia
import random

def iniciar(pentago, tipo):
    humano = True if random.randint(0, 1) == 1 else False
    ordem = ["Humano", "IA"] if humano else ["IA", "Humano"]

    pentago_ia = ia.IA(tipo)
    
    while (not pentago.venceu and not pentago.empatou):
        print(pentago)
        player = "Jogador 1 (" + '\033[37m' + '●' + '\033[0m' + ")" if pentago.primeira_jogada_turno else "Jogador 2 (" + '\033[30m' + '●' + '\033[0m' + ")"

        if((ordem[0] == "IA" and pentago.primeira_jogada_turno) or (ordem[1] == "IA" and not pentago.primeira_jogada_turno)):
            print("IA pensativa...")
            print(player, ": IA :", pentago_ia.jogar(pentago))
        else:
            print(player, ": Escolha seu movimento <B/P BD>: ")
            jogada = input()
            
            valido = pentago.validar_jogada(jogada)
            if valido:
                pentago.jogar(jogada)

    print(pentago)
    if (pentago.empatou):
        print("Houve empate!")
    elif (pentago.branco_venceu):
        print("O branco ganhou!")
    else:
        print("O preto ganhou!")

print("0 - Minimax")
print("1 - Alpha Beta")
print("Escolha o algoritmo: ", end="")

tipo = int(input())

pentago = pg.Pentago()
iniciar(pentago, tipo)
