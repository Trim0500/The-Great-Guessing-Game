from Game import Game
from StringDatabase import StringDatabase
from datetime import datetime
import re
import os

class Guess:
    """
    Class that acts as the game manager of the guessing game.

    Fields:
        _game_mode = The mode in which the program will run.
            play = word is hidden.\n
            test = word is exposed.
        _string_database = An instance of the StringDatabase class that contains the list of words that may be used.\n
        _current_game_index = The number index of the current game. Starts at 1.\n
        _game_list = A list of Game class instances that represents the stats of each game played.
    """
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
        """
        Method that will create a new game into the list of games.
        """
        self._current_game_index += 1

        selected_word = self._string_database.get_new_game_word()
        self._game_list.append(Game(self._current_game_index, selected_word))

    def display_guess_stat_screen(self):
        """
        Method that will display the current status of a game in the program.
        If the game modes is set to test, the selected word will be exposed.
        Will prompt the user to enter an option using a single letter.
        """
        print("++\n++ The great guessing game\n++\n")

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
        """
        Method that will start the guessing game from the driver program.
        """
        self.init_new_game()

        self.display_guess_stat_screen()
    
    def print_feedback(self,
                       option_selected: int,
                       word_guess_result: bool = False,
                       num_letters_in_word: int = 0,
                       game_index: int = 0):
        """
        Method that will print out the feedback of a word guess, a letter guess or a surrender.
        Will clear the current screen to show the feedback when an input is detected.

        Args:
            option_selected: Integer that represents which menu option was selected which affects the message.
            word_guess_result: Boolean for the word guess option that represents if the guess was correct.
            num_letter_guessed: Integer for the letter guess option that represents how many letters were in the word.
            game_index: Integer that represents the index of the current game to look up in the game list.
        """
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
        
        os.system("clear")

        self.display_guess_stat_screen()
        
    def run_word_guess(self):
        """
        Method that will take an input from the user to see if the guess was correct. Makes a new game if the guess is correct.
        """
        keyboard_word_guess = input("\nMake your guess: ").strip().lower()
        while len(re.findall("[0-9]+", keyboard_word_guess)) != 0:
            keyboard_word_guess = input("Invalid input, please re-enter: ").strip().lower()
        
        is_correct = self._game_list[self._current_game_index - 1].check_word_guess(keyboard_word_guess)
        if(is_correct):
            self.init_new_game()

        self.print_feedback(1, is_correct)

    def show_current_word(self):
        """
        Method that will reveal the word to the user given that they choose the tell me option.
        Closes a game and creates a new one.
        """
        self._game_list[self._current_game_index - 1].end_game(False)

        self.init_new_game()
        
        self.print_feedback(2, game_index=self._current_game_index - 2)
    
    def run_letter_guess(self):
        """
        Method that will take in an input from the user to run a letter guess. 
        """
        keyboard_word_guess = input("\nEnter a letter: ").strip().lower()
        while len(keyboard_word_guess) > 1 or len(re.findall("[0-9]", keyboard_word_guess)):
            keyboard_word_guess = input("Invalid input, please re-enter: ").strip().lower()
        
        num_letters_in_word = self._game_list[self._current_game_index - 1].check_letter_guess(keyboard_word_guess)
        self.print_feedback(3, num_letters_in_word=num_letters_in_word)

    def show_final_result_and_quit(self):
        """
        Method that will print out the stats of the games played. A game that was not finished will not have the stats printed.
        """
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

