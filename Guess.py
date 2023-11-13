from Game import Game
from StringDatabase import StringDatabase
from datetime import datetime
import re
import os

class Guess:
    _game_mode: str = ""
    _string_database: StringDatabase = None
    _current_game_index: int = 0
    _game_list: list[Game] = []

    def get_game_mode(self):
        return self._game_mode
    
    def set_game_mode(self, game_mode: str):
        self._game_mode = game_mode

    def get_string_database(self):
        return self._string_database
    
    def set_string_database(self, string_database: StringDatabase):
        self._string_database = string_database
    
    def get_current_game_index(self):
        return self._current_game_index
    
    def set_current_game_index(self, index: int):
        self._current_game_index = index

    def get_game_list(self):
        return self._game_list
    
    def set_game_list(self, game_list: list[Game]):
        self._game_list = game_list

    def __init__(self, mode: str):
      self._game_mode = mode
      self._string_database = StringDatabase("four_letters.txt")
      self._current_game_index = 0

    def init_new_game(self):
        self._current_game_index += 1

        selected_word = self._string_database.get_new_game_word()
        self._game_list.append(Game(self._current_game_index, selected_word))

    def display_guess_stat_screen(self):
        if self._game_mode == "test":
            print("Selected Word: " + self._game_list[self._current_game_index - 1].get_selected_word())

        print("Current Guess: " + self._game_list[self._current_game_index - 1].get_guess_state())
        print("Letters guessed: ", end="")
        letters_guessed = self._game_list[self._current_game_index - 1].get_letters_guessed()
        for i in range(0, len(letters_guessed)):
            print(letters_guessed[i], end=" ")
        print("\n")
        print("g = guess, t = tell me, l for a letter, and q to quit\n")

        keyboard_input = input("Enter option: ").strip().lower()
        while keyboard_input != "g" and keyboard_input != "t" and keyboard_input != "l" and keyboard_input != "q":
            keyboard_input = input("Invalid input, please re-enter:").strip().lower()
        
        if keyboard_input == "g":
            self.run_word_guess()
        elif keyboard_input == "t":
            self.show_current_word()
        elif keyboard_input == "l":
            self.run_letter_guess()
        else:
            self.show_final_result_and_quit()

    def start_game(self):
        print("++\n++ The great guessing game\n++\n")

        self.init_new_game()

        self.display_guess_stat_screen()
    
    def print_feedback(self, option_selected, word_guess_result = False, num_letters_in_word = 0, game_index = 0):
        print("\n@@\n@@ FEEDBACK: ", end="")
        if option_selected == 1:
            if word_guess_result:
                print("You're right, Einstein!\n@@\n")
            else:
                print("Try again, loser!\n@@\n")
        elif option_selected == 2:
            print("You really should have guessed this...'" + self._game_list[game_index].get_selected_word() + "'\n@@\n")
        elif option_selected == 3:
            if num_letters_in_word > 0:
                print("Woo hoo, you found " + str(num_letters_in_word) + " letters\n@@\n")
            else:
                print("Not a single match, genius\n@@\n")
        
        keyboard_input = input("Press any key to continue...")
        
        os.system("cls")

        self.display_guess_stat_screen()
        
    def run_word_guess(self):
        keyboard_word_guess = input("\nMake your guess: ").strip().lower()
        while len(re.findall("[0-9]+", keyboard_word_guess)) != 0:
            keyboard_word_guess = input("Invalid input, please re-enter: ").strip().lower()
        
        is_correct = self._game_list[self._current_game_index - 1].check_word_guess(keyboard_word_guess)
        if(is_correct):
            self.init_new_game()

        self.print_feedback(1, is_correct)

    def show_current_word(self):
        self._game_list[self._current_game_index - 1].end_game(False)

        self.init_new_game()
        
        self.print_feedback(2, game_index=self._current_game_index - 2)
    
    def run_letter_guess(self):
        keyboard_word_guess = input("\nEnter a letter: ").strip().lower()
        while len(keyboard_word_guess) > 1 or len(re.findall("[0-9]", keyboard_word_guess)):
            keyboard_word_guess = input("Invalid input, please re-enter: ").strip().lower()
        
        num_letters_in_word = self._game_list[self._current_game_index - 1].check_letter_guess(keyboard_word_guess)
        self.print_feedback(3, num_letters_in_word=num_letters_in_word)

    def show_final_result_and_quit(self):
        print("\n++\n++ Game Report\n++\n")
        print("Game\t\tWord\t\tStatus\t\tBad Guesses\tMissed Letters\tScore")
        print("----\t\t----\t\t------\t\t-----------\t--------------\t-----")
        
        final_score = 0.0
        for i in range(0, len(self._game_list)):
            if not self._game_list[i].get_status().__eq__("Incomplete"):
                print(self._game_list[i].display_game_stats())

                final_score += self._game_list[i].get_score()
        
        print("\nFinal Score: " + str(round(final_score, 2)))

        exit()

