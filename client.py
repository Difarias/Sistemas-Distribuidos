import Pyro4, os

def main():
    uri      = "PYRO:jogo_quatro_linhas@192.168.0.104:9090"
    servidor = Pyro4.Proxy(uri)

    nome_jogador = input("Selecione um caractere para te representar: ")[:1] 
    print(servidor.registrar_jogador(nome_jogador))

    tabuleiro_anterior   = None  # Armazena o estado anterior do tabuleiro
    controladorTabuleiro = 0

    while servidor.retorna_estado_atual():
        tabuleiro, jogador_atual, jogadores = servidor.obter_estado_jogo()

        # Verifica se houve uma mudança no tabuleiro
        if tabuleiro != tabuleiro_anterior:
            print(servidor.exibir_tabuleiro())
            tabuleiro_anterior = tabuleiro

        if jogadores[jogador_atual] == nome_jogador:
            while True:
                try:
                    coluna = int(input("Digite o número da coluna para soltar o seu disco (1-7): "))
                    if coluna < 1 or coluna > 7:
                        raise ValueError
                    break
                except ValueError:
                    print("Selecione uma entrada válida.")

            mensagem = servidor.jogar(coluna, nome_jogador)
            
            if "venceu" in mensagem:
                controladorTabuleiro = 1
                print(servidor.exibir_tabuleiro())
                print(mensagem)
                break
        else:
            if jogadores[1 - jogador_atual] != nome_jogador:
                print("Aguardando a jogada do oponente...")

    if controladorTabuleiro == 0:
        print(servidor.exibir_tabuleiro())

    print("Fim de jogo")

if __name__ == "__main__":
    main()