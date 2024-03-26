import pentago_game as pg

def iniciar(pentago):
  while (not pentago.venceu and not pentago.empatou):
    print(pentago)

    player = "Jogador 1 (⚪)" if pentago.primeira_jogada_turno else "Jogador 2 (⚫)"
    print(player, ": Escolha seu movimento <B/P BD>:", end="")
    
    jogada = input()
    pentago.jogar(jogada)

    print(pentago)

    if (pentago.empatou):
        print("Houve empate!")
    elif (pentago.branco_venceu):
        print("O branco ganhou!")
    else:
        print("O preto ganhou!")

print("Movimento: B/P BD")
print("B: Qual bloco será escolhido (1-4)")
print("P: A posição escolhida dentro daquele bloco (1-9)")
print("Exemplo:  1/5 1L")

pentago = pg.Pentago()
iniciar(pentago)
