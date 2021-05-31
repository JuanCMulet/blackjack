import random
import sys
import numpy as np
import time
from os import system, name


cardList = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] # Las 13 cartas de cada color
deck = [] # El mazo lo inicializamos vacío
player = [] 
computer = []
player_hand = ""
computer_hand = ""


# Calcula los posibles valores de A's y descarta los que superan 21
# El código del cálculo de Aces no lo hice yo sino que lo tomé de Toni Yiu (En colaboración con @DonBeham)
# el cual fue publicado acá: https://towardsdatascience.com/lets-play-blackjack-with-python-913ec66c732f
def get_ace_values(temp_list):
    sum_array = np.zeros((2**len(temp_list), len(temp_list)))
    # Este loop brinda las posibles permutaciones
    for i in range(len(temp_list)):
        n = len(temp_list) - i
        half_len = int(2**n * 0.5)
        for rep in range(int(sum_array.shape[0]/half_len/2)):
            sum_array[rep*2**n : rep*2**n+half_len, i]=1
            sum_array[rep*2**n+half_len : rep*2**n+half_len*2, i]=11
    # Solo retorna valores <= 21
    return list(set([int(s) for s in np.sum(sum_array, axis=1)\
                     if s<=21]))

# Convierte el número de A's en una lista de listas
def ace_values(num_aces):
    temp_list = []
    for i in range(num_aces):
        temp_list.append([1,11])
    return get_ace_values(temp_list)

# Calcula el valor de la mano
def check_value(hand):
    aces = 0
    total = 0
    for card in hand:
        if card == "A":
            aces += 1
        elif card == "J" or card == "Q" or card == "K":
            total += 10
        else:
            total += int(card)
    
    # Creamos los posibles valores de la mano si existen A's
    ace_value_list = ace_values(aces)
    final_totals = [i+total for i in ace_value_list if i+total<=21]
    
    if final_totals == []:
        return min(ace_value_list) + total
    else:
        return max(final_totals)

# Chequeamos si el Croupier o el Jugador tiene blackjack
def check_bj():
    if check_value(computer) == 21:
        if check_value(player) == 21:
            clear()
            print("### Game On! ###\n"+computer_hand+"\n"+player_hand)
            print("Double Black Jack! It's a tie")
            time.sleep(3)
            clear()
            restart()
        else:
            clear()
            print("### Game On! ###\n"+computer_hand+"\n"+player_hand)
            print("Croupier has 21 Black Jack! The House wins!")
            time.sleep(3)
            clear()
            restart()
    else:
        if check_value(player) == 21:
            clear()
            print("### Game On! ###\n"+computer_hand+"\n"+player_hand)
            print("You have 21 Black Jack! You Win!")
            time.sleep(3)
            clear()
            restart()

# Da una carta al Jugador
def hit_player():
    global player_hand
    player.append(deck.pop(0))
    player_hand = "Your hand: " + " | ".join(player)

# Da una carta al Croupier
def hit_computer():
    global computer_hand
    computer.append(deck.pop(0))
    computer_hand = "Croupier's hand: " + " | ".join(computer)

# Permite al Jugador decidir si toma más cartas o se queda
def hit_or_stay():
    play = True
    if check_value(player) > 21:
            play = False
    while play:
        x = True
        while x:
            a = input("What will you do? (1) Hit or (2) Stay?  ")
            if a == "1":
                hit_player()
                clear()
                print("### Game On! ###\n"+computer_hand+"  "+str(check_value(computer))+"\n"+player_hand+"  "+str(check_value(player)))
                x = False
            elif a == "2":
                clear()
                print("### Game On! ###\n"+computer_hand+"  "+str(check_value(computer))+"\n"+player_hand+"  "+str(check_value(player)))
                x = False
                play = False     
        if check_value(player) > 21:
            play = False

# Hace jugar al Croupier de forma automática,
# Según las reglas, el Croupier debe frenar una vez que tenga 17 o más.
def computer_play():
    play = True
    if check_value(computer) >= 17:
            play = False
    while play:
        hit_computer()
        clear()
        print("### Game On! ###\n"+computer_hand+"  "+str(check_value(computer))+"\n"+player_hand+"  "+str(check_value(player)))
        if check_value(computer) >= 17:
            play = False

# Controla quien gana o si hay empate
def check_winner():
    if check_value(computer) > check_value(player):
        print("### ¡HOUSE WINS! ###\n###   GAME OVER  ###")
        time.sleep(3)
        clear()
        restart()
    elif check_value(computer) == check_value(player):
        print("### ¡IT'S A TIE! ###\n###   NO WINNER  ###")
        time.sleep(3)
        clear()
        restart()
    else:
        print("### ¡YOU ROLLED HIGHER! ###\n###       YOU WIN       ###")
        time.sleep(3)
        clear()
        restart()

# Chequea que el mazo tenga suficientes cartas, sino crea uno nuevo.
def check_deck():
    if len(deck) <= 20:
        for x in range(4):
            for x in cardList:
                deck.append(x)
        random.shuffle(deck)

def restart():
    print("\n### Would you like to play again? ###\n| Press '1' to start a new game     |")
    print("| Press '2' to exit                 |\n#####################################\n")
    menu()

def new_game():
    global player
    global computer
    player = [] 
    computer = []
    check_deck()
    hit_player()
    hit_computer()
    hit_player()
    hit_computer()
    print("### Game On! ###\nCroupier's hand: ?? | "+computer[1],"\n"+player_hand+"  "+str(check_value(player)))
    check_bj()
    hit_or_stay()
    # Chequea si el Jugador se pasa de 21, luego chequea al Croupier
    if check_value(player) > 21:
        print("### ¡OVER 21, BUSTED! ###\n###     GAME OVER     ###")
        time.sleep(3)
        clear()
        restart()
    else:
        computer_play()
    if check_value(computer) > 21:
        print("### ¡OVER 21, HOUSE WAS BUSTED! ###\n###           YOU WIN           ###")
        time.sleep(3)
        clear()
        restart()
    else:
        check_winner()
    

def clear():
    if name == 'nt': # para windows
        _ = system('cls')
    else: # para mac y linux
        _ = system('clear')

def menu():
    a = None
    while True:
        if a == "1":
            clear()
            new_game()
            break
        elif a == "2":
            exit()
        a = input()


def main():
    print("\n\n### ¡Welcome to John's Casino! ###\n| Press '1' to start a new game |")
    print("| Press '2' to exit             |\n#################################\n")
    menu()

main()