import Pyro4
import sys

@Pyro4.expose
class ConnectFourGame:
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.current_player = 'X'
        self.display_board()

    def display_board(self):
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
                    sys.exit()

                self.toggle_player()
                self.display_board()
                return True
        return False

    def get_server_move(self):
        while True:
            try:
                column = int(input("Jogador 1 (O), digite o número da coluna (0-6) para fazer a jogada: "))
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
daemon = Pyro4.Daemon()
uri = daemon.register(ConnectFourGame)
print("URI do servidor:", uri)

# Aguardar por conexões
daemon.requestLoop()
