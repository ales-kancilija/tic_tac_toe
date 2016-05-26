#!/usr/bin/python2

from logic import TicTacToe2Players
from logic import TicTacToeAi

playing = True

chosen = 0
playing_with_ai = False
while not chosen:
    choice = raw_input('Choose:\n[ 1 ]: Player vs Player\n[ 2 ]: Player vs AI\nWhich one?: ')
    if choice.strip() == '1':
        t3 = TicTacToe2Players()
        break
    elif choice.strip() == '2':
        t3 = TicTacToeAi()
        playing_with_ai = True
        break

turn_count = 0

while playing:
    game_over = False
    t3.initialize_table()
    while not game_over:
        turn_count += 1

        t3.display_instructions()
        t3.display_game()

        if playing_with_ai:
            player_input = t3.play_next_turn() if turn_count % 2 else t3.ai_turn()
        else:
            player_input = t3.play_next_turn()

        # Check if we have a winner or if we run out of free cells
        game_over = t3.has_winning_combination_or_game_over(player_input)

    if game_over:
        play_more = raw_input('Want to play another one? [Y / n]:')
        if play_more and play_more.lower()[0] == 'n':
            print 'Thanks for stopping by. Your result is:'
            t3.display_results()
            break
        print '=' * 100
