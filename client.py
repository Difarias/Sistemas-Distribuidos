import Pyro4
import sys

uri = input("Digite a URI do servidor: ")
game = Pyro4.Proxy(uri)

def display_board():
    print(game.display_board())

def make_move(column):
    success = game.make_move(column)
    if success:
        print("Movimento bem-sucedido!")
    else:
        print("Coluna cheia. Tente novamente.")
    display_board()

while True:
    try:
        display_board()

        column = int(input("Jogador 2 (X), digite o número da coluna (0-6) para fazer a jogada: "))
        make_move(column)

        if game.check_winner():
            display_board()
            print(f"Jogador 2 (X) venceu!")
            sys.exit()

        game.get_server_move()

    except Pyro4.errors.CommunicationError:
        print("Erro de comunicação com o servidor. Verifique a conexão.")
        sys.exit()

    except ValueError:
        print("Entrada inválida. Digite um número válido.")
