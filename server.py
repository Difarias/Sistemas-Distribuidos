import Pyro4, os

@Pyro4.expose
class QuatroLinhas:
    def __init__(self):
        #Inicializa o tabuleiro de jogo, jogadores, arquivo log e o controle do jogo
        self.tabuleiro       = [[' ']*7 for _ in range(6)]
        self.jogadores       = [None, None]
        self.jogador_atual   = 0
        self.controladorJogo = True
        self.arquivo_log     = open("log.txt", "w")  # Abre o arquivo de log

    def registrar_acao_jogador(self, nome_jogador, acao):
        #Registrará no arquivo de log, as ações feitas durante o jogo por cada jogador.
        self.arquivo_log.write(f"{nome_jogador} -> {acao}\n")
        self.arquivo_log.flush() 

    def fechar_arquivo(self):
        self.arquivo_log.close()

    def exibir_tabuleiro(self):
        #Limpará a tela e desenhará o tabuleiro     
        os.system('cls' if os.name == 'nt' else 'clear') 
        resultado  = ""
        resultado += "\n  1   2   3   4   5   6   7\n"
        for linha in self.tabuleiro:
            resultado += "| " + " | ".join(linha) + " |\n"
            resultado += "+---+---+---+---+---+---+---+\n"
        return resultado
    
    def retorna_estado_atual(self):
        #Retorna o estado atual do jogo, se houve vencedor ou não.
        return self.controladorJogo

    def fazer_jogada(self, coluna, jogador):
        os.system('cls' if os.name == 'nt' else 'clear') 
        coluna -= 1
        #Percorre as linhas da coluna de baixo para cima, verificando se a posição escolhida está vazia
        for linha in range(5, -1, -1):
            if self.tabuleiro[linha][coluna] == ' ':
                #Insere o caractere do jogador na posição
                self.tabuleiro[linha][coluna] = jogador
                self.registrar_acao_jogador(jogador, f' inseriu disco na linha {linha+1} e coluna {coluna+1}') 
                return True
        #Retorna False se a coluna estiver cheia
        return False

    def verificar_vencedor(self, jogador):
        #Verifica as vitórias na horizontal
        for linha in range(6):
            for coluna in range(4):
                if self.tabuleiro[linha][coluna] == self.tabuleiro[linha][coluna+1] == self.tabuleiro[linha][coluna+2] == self.tabuleiro[linha][coluna+3] == jogador:
                    self.registrar_acao_jogador(jogador, f'venceu na horizontal') 
                    return True

        #Verifica as vitórias na vertical
        for linha in range(3):
            for coluna in range(7):
                if self.tabuleiro[linha][coluna] == self.tabuleiro[linha+1][coluna] == self.tabuleiro[linha+2][coluna] == self.tabuleiro[linha+3][coluna] == jogador:
                    self.registrar_acao_jogador(jogador, f'venceu na vertical') 
                    return True

        #Verifica as vitórias na diagonal
        for linha in range(3):
            for coluna in range(4):
                #Verifica as vitórias na diagonal ascendente
                if self.tabuleiro[linha][coluna] == self.tabuleiro[linha+1][coluna+1] == self.tabuleiro[linha+2][coluna+2] == self.tabuleiro[linha+3][coluna+3] == jogador:
                    self.registrar_acao_jogador(jogador, f'venceu na diagonal ascendente') 
                    return True

                #Verifica as vitórias na diagonal descendente
                if self.tabuleiro[linha][coluna+3] == self.tabuleiro[linha+1][coluna+2] == self.tabuleiro[linha+2][coluna+1] == self.tabuleiro[linha+3][coluna] == jogador:
                    self.registrar_acao_jogador(jogador, f'venceu na diagonal descendente') 
                    return True
        
        #Retorna False se não houver um vencedor
        return False

    def jogar(self, coluna, jogador):
        if self.fazer_jogada(coluna, jogador):
            if self.verificar_vencedor(jogador):
                #Define o controle do jogo como False se houver um vencedor
                self.controladorJogo = False
                return f"O jogador {jogador} venceu!"
            
            #Alterna para o próximo jogador
            self.jogador_atual = 1 - self.jogador_atual
            return "É a vez do próximo jogador."
        else:
            return "A coluna está cheia. Escolha outra coluna."

    def registrar_jogador(self, nome_jogador):
        # Registra um jogador no jogo
        for i in range(len(self.jogadores)):
            if self.jogadores[i] is None:
                self.jogadores[i] = nome_jogador
                self.registrar_acao_jogador(nome_jogador, " inserido...")
                return f"Jogador {i+1} conectado como {nome_jogador}."
        return "Todos os slots de jogadores estão cheios. Não é possível conectar."

    def obter_estado_jogo(self):
        #Retorna as informações no momento.
        return self.tabuleiro, self.jogador_atual, self.jogadores

def main():
    #Configura o servidor para escutar em um endereço IP e porta específicos
    endereco_ip = "192.168.35.118" 
    porta = 9090

    #Inicializa o daemon do Pyro4 e registra a instância do jogo
    daemon = Pyro4.Daemon(host=endereco_ip, port=porta)
    jogo_quatro_linhas = QuatroLinhas()
    uri = daemon.register(jogo_quatro_linhas, "jogo_quatro_linhas")

    print("Servidor em Execução...")
    print("URI do servidor:", uri)

    try:
        daemon.requestLoop()
    finally:
        # No final, fecha o arquivo de texto
        jogo_quatro_linhas.fechar_arquivo()

if __name__ == "__main__":
    main()