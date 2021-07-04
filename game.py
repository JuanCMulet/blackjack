import random
import sys
import numpy as np
import time
import os
import json


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open("highscores.json") as f:
    highscores = json.load(f)

hs = []

for a,b in highscores.items():
    hs.append([a,b])


cardList = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] # Las 13 cartas de cada color
deck = [] # El mazo lo inicializamos vacío
player = [] 
computer = []
player_hand = ""
computer_hand = ""
score = 0
turn = 1


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


# Controla quien gana o si hay empate
def check_winner():
    global turn
    global score
    if check_value(computer) > check_value(player):
        print("### ¡HOUSE WINS! ###\n###   GAME OVER  ###")
        time.sleep(3)
        clear()
        restart()
    elif check_value(computer) == check_value(player):
        print("### ¡IT'S A TIE! ###\n###   NO WINNER  ###")
        time.sleep(3)
        clear()
        turn += 1
        new_game()
    else:
        print("### ¡YOU ROLLED HIGHER! ###\n###       YOU WIN       ###")
        time.sleep(3)
        clear()
        turn += 1
        score += 1
        new_game()

# Hace jugar al Croupier de forma automática,
# Según las reglas, el Croupier debe frenar una vez que tenga 17 o más.
def computer_play():
    play = True
    if check_value(computer) >= 17:
            play = False
    while play:
        hit_computer()
        clear()
        print("### Round",turn,"| Score:",score,"###\n"+computer_hand+"  "+str(check_value(computer))+"\n"+player_hand+"  "+str(check_value(player)))
        if check_value(computer) >= 17:
            play = False

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
                print("### Round",turn,"| Score:",score,"###\n"+computer_hand+"  "+str(check_value(computer))+"\n"+player_hand+"  "+str(check_value(player)))
                x = False
            elif a == "2":
                clear()
                print("### Round",turn,"| Score:",score,"###\n"+computer_hand+"  "+str(check_value(computer))+"\n"+player_hand+"  "+str(check_value(player)))
                x = False
                play = False     
        if check_value(player) > 21:
            play = False

# Chequeamos si el Croupier o el Jugador tiene blackjack
def check_bj():
    global turn
    global score
    if check_value(computer) == 21:
        if check_value(player) == 21:
            clear()
            print("### Round",turn,"| Score:",score,"###\n"+computer_hand+"\n"+player_hand)
            print("Double Black Jack! It's a tie")
            time.sleep(3)
            clear()
            turn += 1
            new_game()
        else:
            clear()
            print("### Round",turn,"| Score:",score,"###\n"+computer_hand+"\n"+player_hand)
            print("Croupier has 21 Black Jack! The House wins!")
            time.sleep(3)
            clear()
            restart()
    else:
        if check_value(player) == 21:
            clear()
            print("### Round",turn,"| Score:",score,"###\n"+computer_hand+"\n"+player_hand)
            print("You have 21 Black Jack! You Win!")
            time.sleep(3)
            clear()
            turn += 1
            score += 1
            new_game()

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

# Chequea que el mazo tenga suficientes cartas, sino crea uno nuevo.
def check_deck():
    if len(deck) <= 20:
        for x in range(4):
            for x in cardList:
                deck.append(x)
        random.shuffle(deck)
        

def new_game():
    global player
    global computer
    global turn
    global score
    player = [] 
    computer = []
    check_deck()
    hit_player()
    hit_computer()
    hit_player()
    hit_computer()
    print("### Round",turn,"| Score:",score,"###\nCroupier's hand: ?? | "+computer[1],"\n"+player_hand+"  "+str(check_value(player)))
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
        turn += 1
        score += 1
        new_game()
    else:
        check_winner()


def show_highscores():
    clear()
    x = highscores.items()
    print("\n\n### Highscores ###")
    for a,b in x:
        print("   ",a+":", b)
    print("\nPress (1) to go back or (0) to exit")
    menu2()

def set_highscore():
    global score
    global hs
    global highscores
    if len(hs) < 10:
        if score == 0:
            print("You didn't reach a highscore this time, better luck next one!")
        else:
            hs.append([input("You got a highscore! Type your name: "),score])
    else:
        if score < hs[9][1] or score == 0:
            print("You didn't reach a highscore this time, better luck next one!")
        else:
            hs[9] = [input("You got a highscore! Type your name: "),score]
    highscores = {k:v for k,v in hs}
    highscores = dict(sorted(highscores.items(), key=lambda item: item[1], reverse=True))
    with open("highscores.json", "w") as t:
        json.dump(highscores, t)
    

def restart():
    global score
    global turn
    set_highscore()
    score = 0
    turn = 1
    print("\n### Would you like to play again? ###\n| Press '1' to go back to main menu  |")
    print("| Press '0' to exit                  |\n#################################\n")
    menu2()

def menu():
    a = None
    while True:
        if a == "1":
            clear()
            new_game()
            break
        elif a == "2":
            show_highscores()
            pass
        elif a == "0":
            exit()
        a = input()

def menu2():
    a = None
    while True:
        if a == "1":
            clear()
            main()
            break
        elif a == "0":
            exit()
        a = input()

def clear():
    if os.name == 'nt': # para windows
        _ = os.system('cls')
    else: # para mac y linux
        _ = os.system('clear')

def main():
    print("\n\n### ¡Welcome to John's Casino! ###\n| Press '1' to start a new game   |")
    print("| Press '2' to see the highscores |")
    print("| Press '0' to exit               |\n#################################\n")
    menu()

main()
