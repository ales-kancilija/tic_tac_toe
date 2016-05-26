from random import choice


class TicTacToeLogic(object):

    data_table = []
    SYMBOL_X = 'X'
    SYMBOL_O = 'O'

    def __init__(self):
        self.player_symbol = self.SYMBOL_O
        self.wins = {self.SYMBOL_X: 0, self.SYMBOL_O: 0}  #: wins for each player
        self.game_over = False
        self.initialize_table()
        self.combinations = {
            1: (1, 2, 3),
            2: (4, 5, 6),
            3: (7, 8, 9),
            4: (1, 4, 7),
            5: (2, 5, 8),
            6: (3, 6, 9),
            7: (1, 5, 9),
            8: (3, 5, 7),
        }
        self.combinations_per_field = {
            # <current_cell>: [<combination_including_this_cell>, ...]
            1: [self.combinations[1], self.combinations[4], self.combinations[7]],
            2: [self.combinations[1], self.combinations[5]],
            3: [self.combinations[1], self.combinations[6], self.combinations[8]],
            4: [self.combinations[2], self.combinations[4]],
            5: [self.combinations[2], self.combinations[5], self.combinations[7], self.combinations[8]],
            6: [self.combinations[2], self.combinations[6]],
            7: [self.combinations[4], self.combinations[8], self.combinations[3]],
            8: [self.combinations[5], self.combinations[3]],
            9: [self.combinations[7], self.combinations[6], self.combinations[3]],
        }  # little more code, but less checks per each input

    @staticmethod
    def __display_table(data=None):
        if not data:
            data = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
        for idx, row in enumerate(data):
            if idx:
                # from 2nd row onwards
                print '-' * 17
            print '  ' + '  |  '.join(row)

    def initialize_table(self):
        self.data_table = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    def display_instructions(self):
        print 'This is how cells are marked:'
        print
        self.__display_table()
        print

    def display_game(self):
        print 'This is how current game looks like:'
        print
        self.__display_table(self.data_table)
        print

    def update_table(self, player_input, player_symbol):
        idx = int(player_input) - 1
        self.data_table[idx // 3][idx % 3] = player_symbol

    def is_cell_empty(self, player_input):
        idx = int(player_input) - 1
        return not self.data_table[idx // 3][idx % 3].strip()

    def has_winning_combination_or_game_over(self, player_input):
        win = False
        for combination in self.combinations_per_field[int(player_input)]:
            # test each combination that include current cell number
            if all(map(lambda x: self.data_table[(x-1) // 3][(x-1) % 3] == self.player_symbol, combination)):
                # if all fields in current combination equal to current player_symbol
                win = True

        if win:
            self.wins[self.player_symbol] += 1
            print '*' * 100
            print 'Congrats! The winner of this round is: Player %s' % self.player_symbol
            self.display_game()
            self.display_results()
            print '*' * 100

            return True
        else:
            for row in self.data_table:
                for cell in row:
                    if not cell.strip():
                        # there's still at least 1 empty cell
                        return False
            print '-' * 100
            print 'Game over. No winner this round.'
            self.display_game()
            self.display_results()
            return True

    def display_results(self):
        print 'Player X vs. Player O ==>', self.wins[self.SYMBOL_X], 'vs.', self.wins[self.SYMBOL_O]

    def switch_player(self):
        self.player_symbol = self.SYMBOL_X if self.player_symbol == self.SYMBOL_O else self.SYMBOL_O


class TicTacToe2Players(TicTacToeLogic):

    def __init__(self):
        super(self.__class__, self).__init__()

    def play_next_turn(self):
        self.switch_player()

        # Select your cell
        while True:
            print 'Current player: ', self.player_symbol
            player_input = raw_input('Insert cell number for player %s: ' % self.player_symbol)
            if player_input.isdigit():
                player_input = int(player_input)
                if 1 <= player_input <= 9:
                    if self.is_cell_empty(player_input):
                        self.update_table(player_input, self.player_symbol)
                        return player_input
                    else:
                        print '==> Cell %s is already taken' % player_input
                else:
                    print '==> Number has to be greater of equal to 1 and lower of equal to 9'
            else:
                print '==> You have to enter a number between 1 and 9, of any empty cell'


class TicTacToeAi(TicTacToeLogic):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.last_player_input = None

    def get_random_empty_cell(self):
        empty_cells = [cell for cell in range(1, 10) if self.is_cell_empty(cell)]
        return choice(empty_cells)

    def play_next_turn(self):
        self.switch_player()

        # Select your cell
        while True:
            print 'Current player: ', self.player_symbol
            player_input = raw_input('Insert cell number for player %s: ' % self.player_symbol)
            if player_input.isdigit():
                player_input = int(player_input)
                if 1 <= player_input <= 9:
                    if self.is_cell_empty(player_input):
                        self.update_table(player_input, self.player_symbol)
                        self.last_player_input = player_input  # This line is new in Player_vs_AI
                        return player_input
                    else:
                        print '==> Cell %s is already taken' % player_input
                else:
                    print '==> Number has to be greater of equal to 1 and lower of equal to 9'
            else:
                print '==> You have to enter a number between 1 and 9, of any empty cell'

    def __find_symbols_in_combination(self, combination, symbol):
        return map(lambda x: self.data_table[(x - 1) // 3][(x - 1) % 3] == symbol, combination)

    def __find_only_empty_cell(self, player_symbol):
        for (combination_id, combination) in self.combinations.items():
            # test each combination that include current cell number
            sym_row = sum(self.__find_symbols_in_combination(combination, player_symbol))
            empty_cells = self.__find_symbols_in_combination(combination, ' ')
            if sym_row == 2 and sum(empty_cells) == 1:
                # 2 fields of opposite player signs and 1 empty field
                for idx, state in enumerate(empty_cells):
                    if state:
                        # return empty cell id
                        return combination[idx]
        # no critical/perfect situation
        return None

    def __find_critical_cell(self, current_player_symbol):
        opponent_player_symbol = self.SYMBOL_X if current_player_symbol == self.SYMBOL_O else self.SYMBOL_O

        # Check if there's a perfect move for current player
        cell = self.__find_only_empty_cell(current_player_symbol)

        if cell:
            return cell
        else:
            # Check if there's a winning next move for the opponent, that AI could beat
            return self.__find_only_empty_cell(opponent_player_symbol)

    def ai_turn(self):
        # switch symbols for current player
        self.switch_player()

        # find critical cell
        ai_choice = self.__find_critical_cell(self.player_symbol)  # find combination with 2 player signs

        if not ai_choice:
            print 'Computer\'s turn.. '
            if self.last_player_input:
                if self.is_cell_empty(5):
                    ai_choice = 5
                elif self.is_cell_empty(10 - self.last_player_input):
                    ai_choice = 10 - self.last_player_input  # Take the opposite field in table (mirrored over center)
                else:
                    ai_choice = self.get_random_empty_cell()
            else:
                ai_choice = 5

        # Update table
        self.update_table(ai_choice, self.player_symbol)
        print 'Computer has chosen:', ai_choice
        return ai_choice





