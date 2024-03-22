import Pyro4

def main():
    uri = "PYRO:connect_four_game@192.168.0.104:9090"
    server = Pyro4.Proxy(uri)
    player_name = input("Enter your name: ")
    print(server.register_player(player_name))

    prev_board = None  # Armazena o estado anterior do tabuleiro

    while True:
        board, current_player, players = server.get_game_state()

        # Verifica se houve uma mudança no tabuleiro
        if board != prev_board:
            print(server.display_board())
            prev_board = board

        if players[current_player] == player_name:
            column = int(input("Enter the column number to drop your disc (1-7): "))
            message = server.play(column, player_name)
            
            if "wins" in message:
                print(server.display_board())
                print(message)
                break
        else:
            if players[1 - current_player] != player_name:
                print("Waiting for opponent's move...")

if __name__ == "__main__":
    main()
