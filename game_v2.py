import requests
import json
import random
from itertools import cycle, islice


def jprint(obj):
    if response.status_code == 200:
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)


# consider putting this in a function
params_black = {"packs": "CAH: Family Edition (Free Print & Play Public Beta)", "color": "black"}
params_white = {"packs": "CAH: Family Edition (Free Print & Play Public Beta)", "color": "white"}

response = requests.get("https://restagainsthumanity.com/api/v2/cards", params=params_black)
black_cards = response.json()["black"]

response = requests.get("https://restagainsthumanity.com/api/v2/cards", params=params_white)
white_cards = response.json()["white"]

# consider writing global variables in all caps
while True:
    try:
        player_count = int(input("Enter the number of players (min: 4): "))
        if player_count < 4:
            raise ValueError
        break
    except:
        print("Invalid input. Try again.")

player_name_count = player_count
player_index_range = list(range(0, player_count))
player_list = []
player_index = None
current_czar = None
current_czar_index = None
current_black_card = None
current_black_card_text = None
white_card_submission = []
winning_index = None


class Player:

    def __init__(self, player):
        self.player = player
        self.hand = []  # display hand
        self.won_cards = []  # show list of won black cards
        self.points = 0  # display current points

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
        count = 0
        for card in self.hand:
            print(f"{count}: {card}")
            count += 1
        if current_black_card["pick"] == 1:
            while True:
                try:
                    submit_index = int(input("Please choose your card (enter number): "))
                    while submit_index >= 10 or submit_index < 0:
                        raise IndexError
                    break
                except:
                    print("Invalid input. Try again.")
            print(f"Your submission: {self.hand[submit_index]}")
            white_card_submission.append((self.player, self.hand[submit_index]))
            self.hand.remove(self.hand[submit_index])
        elif current_black_card["pick"] == 2:
            while True:
                try:
                    submit_index = int(input("Please choose your first card (enter number): "))
                    while submit_index >= 10 or submit_index < 0:
                        raise IndexError
                    break
                except:
                    print("Invalid input. Try again.")
            print(f"Your first submission: {self.hand[submit_index]}")
            while True:
                try:
                    submit_index_2 = int(input("Please choose your second card (enter number): "))
                    while submit_index_2 >= 10 or submit_index_2 < 0:
                        raise IndexError
                    break
                except:
                    print("Invalid input. Try again.")
            print(f"Your second submission: {self.hand[submit_index_2]}")
            my_submission = []
            my_submission.append(self.hand[submit_index])
            self.hand.remove(self.hand[submit_index])
            my_submission.append(self.hand[submit_index_2])
            self.hand.remove(self.hand[submit_index_2])
            white_card_submission.append((self.player, my_submission))
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
        global current_black_card
        current_black_card = random.choice(black_cards)
        black_cards.remove(current_black_card)
        global current_black_card_text
        current_black_card_text = random.choice(black_cards)["text"]
        print(f"Current black card: {current_black_card_text}")
        print()
        print('-' * 26)
        print()

    # Test black card has been removed
    # try:
    #     black_cards.index(current_black_card) # Should return "ValueError: {} is not in list"
    # except:

    def display_card_candidates(self):
        input(f"{player_list[current_czar_index].player}, time to pick the round winner. Press Enter to see cards.")
        print(f"Current black card: {current_black_card_text}")
        global submission_count
        submission_count = 0
        for submission in white_card_submission:
            if current_black_card["pick"] == 1:
                print(f"{submission_count}: {submission[1]}")
            elif current_black_card["pick"] == 2:
                print(f"{submission_count}: {submission[1]}, {submission[2]}")
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

        print(f"Winner: {white_card_submission[winning_index]}")
        print()
        print('-' * 26)
        print()
        print("Current points:")
        for person in player_list:
            if person.player == white_card_submission[winning_index][0]:
                person.add_point()
            print(person.player, person.points)
        white_card_submission = []
        print()
        print('-' * 26)
        print()


def player_setup():
    global player_name_count
    while player_name_count > 0:
        while True:
            a = input("Enter player name: ")
            if not a or any(person.player == a for person in player_list):
                if not a:
                    print("Blank input. Try again.")
                if any(person.player == a for person in player_list):
                    print("Already exists. Try a different name.")
            else:
                break
        a = Player(a)
        player_list.append(a)
        player_name_count -= 1
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
        print(f"Current Czar: {player_list[current_czar_index].player}")
    else:
        current_czar_index = next(islice(cycle(player_index_range), current_czar_index+1, None))
        current_czar = Czar(player_list[current_czar_index])
        print(f"Current Czar: {player_list[current_czar_index].player}")
    player_index = next(islice(cycle(player_index_range), current_czar_index + 1, None))


def run_round():
    global player_index, current_czar_index, player_list
    while player_index != current_czar_index:
        input(f"{player_list[player_index].player}, it's your turn. Press Enter to see your hand.")
        print(f"Current czar: {player_list[current_czar_index].player}")
        print(f"Current black card: {current_black_card_text}")
        player_list[player_index].submit_white_card()
        player_list[player_index].draw_white_card()
        if current_black_card["pick"] == 1:
            print(f"New card in your hand: {player_list[player_index].hand[-1]}")
        if current_black_card["pick"] == 2:
            print(f"New cards in your hand: {player_list[player_index].hand[-2]}, {player_list[player_index].hand[-1]}")
        player_index = next(islice(cycle(player_index_range), player_index+1, None))
        print()
        print('-' * 26)
        print()


player_setup()

# round mechanics (is not looping until point limit)
while True:
    if any(person.points == 2 for person in player_list):
        break
    pick_current_czar()
    current_czar.draw_black_card()
    run_round()
    current_czar.display_card_candidates()
    current_czar.choose_winning_card()

