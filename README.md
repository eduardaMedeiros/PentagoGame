## Pentago Game
Pentago é um jogo de estratégia para dois jogadores. O tabuleiro consiste em quatro subtabuleiros 3x3 que podem ser girados. Os jogadores se revezam colocando esferas de sua cor em qualquer subtabuleiro. O objetivo é alinhar cinco esferas de sua cor, verticalmente, horizontalmente ou diagonalmente, considerando que a rotação dos subtabuleiros pode alterar drasticamente o estado do jogo.

## Implementação
Se trata de uma engine de games de IA que jogam de forma inteligente contra um humano utilizando minimax e poda alfa beta

## Como jogar?
O jogador é escolhido aleatoriamente para ir primeiro ou segundo contra a IA.

Durante cada jogada, o jogador deve inserir suas ações no formato "b/p bd" (sem aspas).

"b/p" define o bloco e a localização dentro desse bloco, "bd" define um bloco e a direção para rotacioná-lo.

b: o bloco escolhido, de 1 a 4
<img src="resources/img-blocos.png" alt="Numeração dos Blocos">

p: a localização escolhida dentro do bloco, de 1 a 9.
<img src="resources/img-blocos.png" alt="Posições dos Blocos">

d: a direção para rotacionar o bloco b

    R: sentido horário 90 graus (direita)
    L: sentido anti-horário 90 graus (esquerda)

## Créditos:
Projeto realizado por:
- Carolina Gimenez
- Eduarda Medeiros