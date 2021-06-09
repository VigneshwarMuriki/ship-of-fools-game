import random


class ShipOfFoolsGame:
    """Each player will get 3 rolls
       and if a person gets ship,captain
       and crew then the score will be
       the number which is on the remaining
       two dice.
       There are number of cases where a person
       may get ship,captain and crew in a single attempt
       or in multiple attempts. If a person doesn't get ship,
       captain and crew in 3 rolls, then the next person rolls
       and the cycle repeats.
       After getting ship,captain and crew, if the value on the
       unbanked dice is greater than 3, then those dice will
       also get banked and those which are unbanked are rolled again
       Here we set the winning score to 21.
       Inorder to roll the dice we call the DiceCup class.
    """
    def __init__(self):
        self._cup = DiceCup()
        self.__WINNING_SCORE = 21

    def round(self):
        has_ship = False
        has_captain = False
        has_crew = False
        cargo = 0
        for _ in range(3):
            self._cup.roll()
            scores = []
            for i in range(5):
                scores.append(self._cup.index(i))
            print(scores)
            if not has_ship:
                for i in range(5):
                    if self._cup.index(i) == 6:
                        has_ship = True
                        self._cup.bank(i)
                        break

            if has_ship and not has_captain:
                for i in range(5):
                    if not self._cup.is_banked(i):
                        if self._cup.index(i) == 5:
                            has_captain = True
                            self._cup.bank(i)
                            break

            if has_ship and has_captain and not has_crew:
                for i in range(5):
                    if not self._cup.is_banked(i):
                        if self._cup.index(i) == 4:
                            has_crew = True
                            self._cup.bank(i)
                            break

            if has_ship and has_captain and has_crew:
                if _+1 == 3:
                    for i in range(5):
                        if not self._cup.is_banked(i):
                            cargo += self._cup.index(i)
                else:
                    for i in range(5):
                        if not self._cup.is_banked(i):
                            if self._cup.index(i) > 3:
                                cargo += self._cup.index(i)
                                self._cup.bank(i)

        self._cup.release_all()
        return cargo

    @property
    def get_winning_score(self):
        return self.__WINNING_SCORE


class Die:
    """
       We initially set the the value of each die
       to zero. Using roll function we roll the die
       to get a random value from 1 to 6.
    """
    def __init__(self):
        self.__value = 0

    def get_value(self):
        return self.__value

    def roll(self):
        self.__value = random.randint(1, 6)


class DiceCup():
    """
       Initially we set the banked dice to boolean value False.
       We create 5 die objects from Die class and to put them in the
       DiceCup. While rolling if we get ship,captain and crew then the
       index of banked die will be set to boolean value True. If we don't
       get ship,captain and crew then the dice have to be rolled again.
    """
    def __init__(self):
        self.banked = [False, False, False, False, False]
        self.__dice = [Die() for i in range(5)]

    def index(self, index):
        return self.__dice[index].get_value()

    def bank(self, index):
        self.banked[index] = True

    def is_banked(self, index):
        return self.banked[index]

    def release(self, index):
        self.banked[index] = False

    def release_all(self):
        for i in range(5):
            self.banked[i] = False

    def roll(self):
        for i in range(5):
            if self.banked[i] is False:
                self.__dice[i].roll()


class Player:
    """
       Before the commencement of the game, the players' scores
       set to intial value zero. If a player gets 6,5,4 in 3 rolls
       then the score will be the value on remaining 2 dice or else
       the score will be zero and the player has to roll the dice
       again
    """
    def __init__(self,name):
        self.set_name(name)
        self._score = 0

    def set_name(self, namestring):
        self._name = namestring

    def current_score(self):
        return self._score

    def reset_score(self):
        self._score = 0

    def play_round(self, game):
        print(self._name, "started playing")
        x = game.round()
        print(self._name, "'s cargo in this round is", x)
        self._score += x

    def get_name(self):
        return self._name


class PlayRoom:
    """Here we take the input fro the user to start
       the game and append those players using a list.
       Initially we set the scores of players to zero.
       The number of rounds does not matter. For a player
       to win he/she should have winning score of 21 and greater
       and the player will be declared as the winner.
    """
    def __init__(self):
        self._players = []

    def set_game(self,game):
        self._game=game

    def add_player(self,players):
        self._players.append(players)

    def reset_scores(self):
        for i in self._players:
            i.reset_score()

    def play_round(self):
        for i in self._players:
            if not self.game_finished():
                i.play_round(self._game)

    def game_finished(self):
        for i in self._players:
            if i.current_score() > self._game.get_winning_score:
                return True
        return False

    def print_scores(self):
        print("scores are")
        for i in self._players:
            print(i.get_name(), ":", i.current_score())

    def print_winner(self):
        for i in self._players:
            if i.current_score() > self._game.get_winning_score:
                print(i.get_name(), "won")
                break

if __name__ == "__main__":
    """
       In the main function we enter the number of players
       and append those players using a for loop. The game
       has to continue until a player reaches a minimum score
       of 21 or greater and then he/she will be declared as winner
    """
    room = PlayRoom()
    room.set_game(ShipOfFoolsGame())
    room.add_player(Player("Viggi"))
    room.add_player(Player("Sunila"))
    room.reset_scores()
    

    r = 1
    while(not room.game_finished()):
        print("round", r, "started")
        room.play_round()
        room.print_scores()
        r += 1
    room.print_winner()
    room.reset_scores()
