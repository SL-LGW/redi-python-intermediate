import requests
import random
from itertools import cycle, islice
import os


current_czar = None
player_list = []
white_card_submission = []


class Player:

    def __init__(self, player):
        self.player = player
        self.hand = []
        self.points = 0

    def draw_white_card(self):
        draw_count = 0
        if not self.hand:
            draw_count = 10
        elif current_black_card["pick"] == 1:
            draw_count = 1
        elif current_black_card["pick"] == 2:
            draw_count = 2
        draw = random.sample(white_cards, draw_count)
        for i in draw:
            self.hand.append(i["text"])
            white_cards.remove(i)
        return self.hand

    def submit_white_card(self):
        print("Your Hand")
        count = 0
        for card in self.hand:
            print(f"{count}: {card}")
            count += 1
        if current_black_card["pick"] == 1:
            # print(current_black_card) # for testing
            while True:
                try:
                    submit_index = int(input("Please choose a card to submit (enter number): "))
                    while submit_index >= 10 or submit_index < 0:
                        raise IndexError
                    break
                except:
                    print("Invalid input. Try again.")
            print()
            print('-' * 26)
            print()
            print(f"Your submission: {self.hand[submit_index]}")
            white_card_submission.append((self.player, self.hand[submit_index]))
            self.hand.remove(self.hand[submit_index])
        elif current_black_card["pick"] == 2:
            # print(current_black_card) # for testing
            while True:
                try:
                    submit_index = int(input("Please choose the first card (enter number): "))
                    while submit_index >= 10 or submit_index < 0:
                        raise IndexError
                    break
                except:
                    print("Invalid input. Try again.")
            print()
            print('-' * 26)
            print()
            print(f"Your first submission: {self.hand[submit_index]}")
            while True:
                try:
                    submit_index_2 = int(input("Please choose the second card (enter number): "))
                    while submit_index_2 >= 10 or submit_index_2 < 0:
                        raise IndexError
                    break
                except:
                    print("Invalid input. Try again.")
            print()
            print('-' * 26)
            print()
            print(f"Your second submission: {self.hand[submit_index_2]}")
            my_submission = []
            my_submission.append(self.hand[submit_index])
            my_submission.append(self.hand[submit_index_2])
            white_card_submission.append((self.player, my_submission))
            if submit_index > submit_index_2:
                self.hand.remove(self.hand[submit_index])
                self.hand.remove(self.hand[submit_index_2])
            elif submit_index_2 > submit_index:
                self.hand.remove(self.hand[submit_index_2])
                self.hand.remove(self.hand[submit_index])
        print()
        print('-' * 26)
        print()

    def add_point(self):
        points_to_add = current_black_card["pick"]
        self.points += points_to_add


class Czar(Player):

    def __init__(self, czar):
        super().__init__(self)
        self.czar = czar

    def draw_black_card(self):
        global current_black_card, current_black_card_text
        current_black_card = random.choice(black_cards)
        black_cards.remove(current_black_card)
        current_black_card_text = current_black_card["text"]
        print(f"Current black card: {current_black_card_text}")
        print()
        print('-' * 26)
        print()

    def display_card_candidates(self):
        global submission_count
        input(f"{player_list[current_czar_index].player}, time to pick the round winner. Press Enter to see cards.")
        print()
        print('-' * 26)
        print()
        print(f"Current black card: {current_black_card_text}")
        submission_count = 0
        for submission in white_card_submission:
            if current_black_card["pick"] == 1:
                print(f"{submission_count}: {submission[1]}")
            elif current_black_card["pick"] == 2:
                print(f"{submission_count}: {submission[1][0]}, {submission[1][1]}")
            submission_count += 1

    def choose_winning_card(self):
        global winning_index, white_card_submission
        while True:
            try:
                winning_index = int(input("Choose the winner of this round (enter number): "))
                if winning_index > submission_count-1 or winning_index < 0:
                    raise IndexError
                break
            except:
                print("Invalid input. Try again.")
        print()
        print('-' * 26)
        print()
        print(f"Round winner: {white_card_submission[winning_index]}")
        print()
        print('-' * 26)
        print()
        print("Current points:")
        for person in player_list:
            if person.player == white_card_submission[winning_index][0]:
                person.add_point()
            print(person.player, person.points)
        white_card_submission = []


def welcome():
    print()
    print('-' * 26)
    print()
    print("Welcome to Python Against Humanity, a ReDI project.")
    print("Based on Cards Against Humanity, a party game for horrible people.")
    print()
    print('-' * 26)
    print()
    print("Disclaimer: Cards Against Humanity allows the open use of their cards, as long as you don't make money off of it.")
    print("            For more information, visit their website at https://www.cardsagainsthumanity.com/#downloads")
    print()
    print('-' * 26)
    print()
    print("Warning: This game is generally considered to be offensive. We mean no offense.")
    print("         If you'd like to minimize any offensiveness, we recommend choosing the Family Edition.")
    print()
    print('-' * 26)
    print()


def card_setup():
    global black_cards, white_cards, response, pack_selection
    while True:
        try:
            pack_selection = int(input("Play with the Family Edition (1) or the full selection (2)? Enter number: "))
            if pack_selection == 1:
                params_black = {"packs": "CAH: Family Edition (Free Print & Play Public Beta)", "color": "black"}
                params_white = {"packs": "CAH: Family Edition (Free Print & Play Public Beta)", "color": "white"}
            elif pack_selection == 2:
                params_black = {"color": "black"}
                params_white = {"color": "white"}
            else:
                raise ValueError
            break
        except:
            print("Invalid input. Try again.")
    response = requests.get("https://restagainsthumanity.com/api/v2/cards", params=params_black)
    black_cards = response.json()["black"]
    response = requests.get("https://restagainsthumanity.com/api/v2/cards", params=params_white)
    white_cards = response.json()["white"]
    print()
    print('-' * 26)
    print()


def set_points_to_win():
    global points_to_win
    while True:
        try:
            points_to_win = int(input(f"Set min number of points to win (min: 1): "))
            if points_to_win < 1:
                raise ValueError
            break
        except:
            print("Invalid input. Try again.")
    print()
    print('-' * 26)
    print()


def player_setup():
    global player_count, player_name_countdown, player_index_range, player_list
    while True:
        try:
            player_count = int(input("Enter the number of players (min: 4): "))
            if player_count < 4:
                raise ValueError
            break
        except:
            print("Invalid input. Try again.")
    print()
    print('-' * 26)
    print()
    player_name_countdown = player_count
    player_index_range = list(range(0, player_count))
    while player_name_countdown > 0:
        while True:
            a = input("Enter player name: ")
            if not a or any(person.player == a for person in player_list) or a.isspace() is True:
                if not a:
                    print("Blank input. Try again.")
                elif any(person.player == a for person in player_list):
                    print("Already exists. Try a different name.")
                elif a.isspace() is True:
                    print("Cannot have only spaces. Try again.")
            else:
                break
        a = Player(a)
        player_list.append(a)
        player_name_countdown -= 1
        a.draw_white_card()
    print()
    print('-' * 26)
    print()


def pick_current_czar():
    global current_czar, current_czar_index, player_index
    if isinstance(current_czar, Czar) is False:
        count = 0
        for person in player_list:
            print(f"{count}: {person.player}")
            count += 1
        while True:
            try:
                current_czar_index = int(input("Choose the first czar (enter number): "))
                if current_czar_index > player_count-1 or current_czar_index < 0:
                    raise IndexError
                break
            except:
                print("Invalid input. Try again.")
        current_czar = Czar(player_list[current_czar_index])
        print()
        print('-' * 26)
        print()
        print(f"Current Czar: {player_list[current_czar_index].player}")
    else:
        current_czar_index = next(islice(cycle(player_index_range), current_czar_index+1, None))
        current_czar = Czar(player_list[current_czar_index])
        print()
        print('-' * 26)
        print()
        print(f"Current Czar: {player_list[current_czar_index].player}")
    player_index = next(islice(cycle(player_index_range), current_czar_index + 1, None))


def run_round():
    global player_index, current_czar_index, player_list
    while player_index != current_czar_index:
        input(f"{player_list[player_index].player}, it's your turn. Press Enter to see your hand.")
        os.system('cls')
        print()
        print('-' * 26)
        print()
        print(f"Current player: {player_list[player_index].player}")
        print()
        print('-' * 26)
        print()
        print(f"Current czar: {player_list[current_czar_index].player}")
        print(f"Current black card: {current_black_card_text}")
        print()
        print('-' * 26)
        print()
        player_list[player_index].submit_white_card()
        player_list[player_index].draw_white_card()
        if current_black_card["pick"] == 1:
            print(f"New card in your hand: {player_list[player_index].hand[-1]}")
        if current_black_card["pick"] == 2:
            print(f"New cards in your hand: {player_list[player_index].hand[-2]}, {player_list[player_index].hand[-1]}")
        print()
        print('-' * 26)
        print()
        input("Press Enter to end your turn.")
        player_index = next(islice(cycle(player_index_range), player_index+1, None))
        os.system('cls')
        print()
        print('-' * 26)
        print()


def loop_round():
    global game_winner
    while True:
        if any(person.points >= points_to_win for person in player_list):
            for person in player_list:
                if person.points >= points_to_win:
                    game_winner = person.player
            print()
            print('-' * 26)
            print()
            print(f"{game_winner} won the game!")
            print()
            print('-' * 26)
            print()
            break
        pick_current_czar()
        current_czar.draw_black_card()
        run_round()
        current_czar.display_card_candidates()
        current_czar.choose_winning_card()
