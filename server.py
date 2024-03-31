import Pyro4, os

@Pyro4.expose
class QuatroLinhas:
    def __init__(self):
        self.tabuleiro = [[' ']*7 for _ in range(6)]
        self.jogadores = [None, None]
        self.jogador_atual = 0
        self.controladorJogo   = True

    def exibir_tabuleiro(self):     
        os.system('cls' if os.name == 'nt' else 'clear') 
        resultado = ""
        resultado += "\n  1   2   3   4   5   6   7\n"
        for linha in self.tabuleiro:
            resultado += "| " + " | ".join(linha) + " |\n"
            resultado += "+---+---+---+---+---+---+---+\n"
        return resultado
    
    def retorna_estado_atual(self):
        return self.controladorJogo

    def fazer_jogada(self, coluna, jogador):
        os.system('cls' if os.name == 'nt' else 'clear') 
        coluna -= 1
        for linha in range(5, -1, -1):
            if self.tabuleiro[linha][coluna] == ' ':
                self.tabuleiro[linha][coluna] = jogador
                return True
        return False

    def verificar_vencedor(self, jogador):
        for linha in range(6):
            for coluna in range(4):
                if self.tabuleiro[linha][coluna] == self.tabuleiro[linha][coluna+1] == self.tabuleiro[linha][coluna+2] == self.tabuleiro[linha][coluna+3] == jogador:
                    return True

        for linha in range(3):
            for coluna in range(7):
                if self.tabuleiro[linha][coluna] == self.tabuleiro[linha+1][coluna] == self.tabuleiro[linha+2][coluna] == self.tabuleiro[linha+3][coluna] == jogador:
                    return True

        for linha in range(3):
            for coluna in range(4):
                if self.tabuleiro[linha][coluna] == self.tabuleiro[linha+1][coluna+1] == self.tabuleiro[linha+2][coluna+2] == self.tabuleiro[linha+3][coluna+3] == jogador:
                    return True

                if self.tabuleiro[linha][coluna+3] == self.tabuleiro[linha+1][coluna+2] == self.tabuleiro[linha+2][coluna+1] == self.tabuleiro[linha+3][coluna] == jogador:
                    return True

        return False

    def jogar(self, coluna, jogador):
        if self.fazer_jogada(coluna, jogador):
            if self.verificar_vencedor(jogador):
                self.controladorJogo = False
                return f"O jogador {jogador} venceu!"
            self.jogador_atual = 1 - self.jogador_atual
            return "É a vez do próximo jogador."
        else:
            return "A coluna está cheia. Escolha outra coluna."

    def registrar_jogador(self, nome_jogador):
        for i in range(len(self.jogadores)):
            if self.jogadores[i] is None:
                self.jogadores[i] = nome_jogador
                return f"Jogador {i+1} conectado como {nome_jogador}."
        return "Todos os slots de jogadores estão cheios. Não é possível conectar."

    def obter_estado_jogo(self):
        return self.tabuleiro, self.jogador_atual, self.jogadores

def main():
    endereco_ip = "192.168.0.104" 
    porta = 9090

    daemon = Pyro4.Daemon(host=endereco_ip, port=porta)
    jogo_quatro_linhas = QuatroLinhas()
    uri = daemon.register(jogo_quatro_linhas, "jogo_quatro_linhas")

    print("Servidor em Execução...")
    print("URI do servidor:", uri)

    daemon.requestLoop()

if __name__ == "__main__":
    main()