import Pyro4, os

def main():
    #URI do servidor onde o jogo está sendo executado
    uri      = "PYRO:jogo_quatro_linhas@192.168.35.118:9090"

    #Criado um proxy para se comunicar com o servidor remoto usando a URI
    servidor = Pyro4.Proxy(uri)

    #Solicita ao jogador que selecione um caractere para representá-lo no jogo
    nome_jogador = input("Selecione um caractere para te representar: ")[:1] #Limita a 1 caractere para ser salvo

    #Registra o jogador no servidor e exibe uma mensagem de confirmação
    print(servidor.registrar_jogador(nome_jogador))

    tabuleiro_anterior   = None  #Armazena o estado anterior do tabuleiro
    controladorTabuleiro = 0

    while servidor.retorna_estado_atual():
        #Obtém o estado atual do jogo do servidor 
        tabuleiro, jogador_atual, jogadores = servidor.obter_estado_jogo()

        #Verifica se houve uma mudança no tabuleiro
        if tabuleiro != tabuleiro_anterior:
            print(servidor.exibir_tabuleiro())
            tabuleiro_anterior = tabuleiro

        #Verifica se é a vez do jogador atual
        if jogadores[jogador_atual] == nome_jogador:
            while True:
                try:
                    #Solicita ao jogador que escolha uma coluna para jogar
                    coluna = int(input("Digite o número da coluna para soltar o seu disco (1-7): "))
                    if coluna < 1 or coluna > 7:
                        raise ValueError
                    break
                except ValueError:
                    print("Selecione uma entrada válida.")

            #Faz a jogada no servidor e verifica se o jogador venceu
            mensagem = servidor.jogar(coluna, nome_jogador)
            
            if "venceu" in mensagem:
                controladorTabuleiro = 1
                print(servidor.exibir_tabuleiro())
                print(mensagem)
                break
        else:
            if jogadores[1 - jogador_atual] != nome_jogador:
                print("Aguardando a jogada do oponente...")

    #Se o jogo terminou sem vitória, exibe o tabuleiro final
    if controladorTabuleiro == 0:
        print(servidor.exibir_tabuleiro())

    print("Fim de jogo")

if __name__ == "__main__":
    main()