import Pyro4
import sys, os, time

@Pyro4.expose
class ConnectFourGame:
    def __init__(self):
        self.restart_game()

    def restart_game(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.current_player = 'O'  # Jogador local (Jogador 1) começa com 'O'
        self.display_board()

    def display_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela mediante o sistema operacional
        output = ""
        for row in self.board:
            output += "|".join(row) + "\n"
        output += "-------------"
        print(output)
        sys.stdout.flush()
        return output

    def make_move(self, column):
        for row in range(5, -1, -1):
            if self.board[row][column] == ' ':
                self.board[row][column] = self.current_player

                if self.check_winner():
                    self.display_board()
                    print(f"Jogador {self.current_player} venceu!")
                    time.sleep(3)
                    self.restart_game()

                self.toggle_player()
                self.display_board()
                return True
        return False

    def get_server_move(self):
        while True:
            try:
                column = int(input("Jogador 2 (O), digite o número da coluna (0-6) para fazer a jogada: "))
                success = self.make_move(column)

                if success:
                    print("Movimento bem-sucedido!")
                    return
                else:
                    print("Coluna cheia. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número válido.")

    def toggle_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        for row in self.board:
            if 'XXXX' in ''.join(row) or 'OOOO' in ''.join(row):
                return True

        for col in range(7):
            if 'XXXX' in ''.join(row[col] for row in self.board) or 'OOOO' in ''.join(row[col] for row in self.board):
                return True

        for i in range(3):
            for j in range(4):
                if 'XXXX' in ''.join(self.board[i + k][j + k] for k in range(4)) or 'OOOO' in ''.join(self.board[i + k][j + k] for k in range(4)):
                    return True

                if 'XXXX' in ''.join(self.board[i + k][j + 3 - k] for k in range(4)) or 'OOOO' in ''.join(self.board[i + k][j + 3 - k] for k in range(4)):
                    return True

        return False

# Inicializar o servidor
ip_address = "192.168.0.104" 
port=9090

daemon = Pyro4.Daemon(host=ip_address, port=port)
uri = daemon.register(ConnectFourGame, "connect_four_game")

print("Servidor em Execução...")
print("URI do servidor:", uri)

# Aguardar por conexões
daemon.requestLoop()
