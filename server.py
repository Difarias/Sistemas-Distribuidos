import Pyro4, os

@Pyro4.expose
class QuatroLinhas:
    def __init__(self):
        self.board = [[' ']*7 for _ in range(6)]
        self.players = [None, None]
        self.current_player = 0

    def display_board(self):
        os.system('cls' if os.name == 'nt' else 'clear') 
        result = ""
        result += "\n  1   2   3   4   5   6   7\n"
        result += "+---+---+---+---+---+---+---+\n"
        for row in self.board:
            result += "| " + " | ".join(row) + " |\n"
            result += "+---+---+---+---+---+---+---+\n"
        return result

    def make_move(self, column, player):
        column -= 1
        for row in range(5, -1, -1):
            if self.board[row][column] == ' ':
                self.board[row][column] = player
                return True
        return False

    def check_winner(self, player):
        for row in range(6):
            for col in range(4):
                if self.board[row][col] == self.board[row][col+1] == self.board[row][col+2] == self.board[row][col+3] == player:
                    return True

        for row in range(3):
            for col in range(7):
                if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col] == player:
                    return True

        for row in range(3):
            for col in range(4):
                if self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3] == player:
                    return True

                if self.board[row][col+3] == self.board[row+1][col+2] == self.board[row+2][col+1] == self.board[row+3][col] == player:
                    return True

        return False

    def play(self, column, player):
        if self.make_move(column, player):
            if self.check_winner(player):
                return f"Player {player} wins!"
            self.current_player = 1 - self.current_player
            return "Next player's turn."
        else:
            return "Column is full. Choose another column."

    def register_player(self, player_name):
        for i in range(len(self.players)):
            if self.players[i] is None:
                self.players[i] = player_name
                return f"Player {i+1} connected as {player_name}."
        return "All player slots are full. Cannot connect."

    def get_game_state(self):
        return self.board, self.current_player, self.players


def main():
    ip_address = "192.168.0.104" 
    port = 9090

    daemon = Pyro4.Daemon(host=ip_address, port=port)
    connect_four_game = QuatroLinhas()
    uri = daemon.register(connect_four_game, "connect_four_game")

    print("Servidor em Execução...")
    print("URI do servidor:", uri)

    daemon.requestLoop()

if __name__ == "__main__":
    main()
