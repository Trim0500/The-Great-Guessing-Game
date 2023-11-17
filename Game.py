class Game:
    """
    Class that represents a game played and the associated stats that are generated.

    Fields:
        _game_index: Integer that represents the index of of the game.
        _selected_word: String that represents the randomly selected word chosen from the string database.
        _guess_state: String that represents the progress of the discovery process of the selected word.
                        A - represents a letter that has yet to be found.
        _letters_guessed: A list comprising of the individual letters the user guessed with.
        _status: String that represents the completness of the game.
                    Success = User found the word
                    Gave Up = User failed to find the word
                    Incomplete = Inconclusive results
        _num_bad_guesses: Integer that represents the number of times an incorrect guess was made by the user.
        _num_missed_letters: Integer that represents the number of letters that aren't in the word when guessed by the user.
        _score: Double precision float that represents the accumulated score the user has attributed to the game.
        _letter_frequency_dict: Dictionary that represents the frequency percentages tied to letters when evaluating score.        
    """
    _game_index: int = 0
    _selected_word: str = ""
    _guess_state: str = ""
    _letters_guessed: list[str] = []
    _status: str = ""
    _num_bad_guesses: int = 0
    _num_missed_letters: int = 0
    _score: float = 0.0
    _letter_frequency_dict: dict[str, float] = {}

    def get_game_index(self):
        return self._game_index
    
    def set_game_index(self, index: int):
        self._game_index = index

    def get_selected_word(self):
        return self._selected_word
    
    def set_selected_word(self, selected_word: str):
        self._selected_word = selected_word

    def get_guess_state(self):
        return self._guess_state
    
    def set_guess_state(self, guess_state: str):
        self._guess_state = guess_state

    def get_letters_guessed(self):
        return self._letters_guessed
    
    def set_letters_guessed(self, letters_guessed: list[str]):
        self._letters_guessed = letters_guessed

    def get_status(self):
        return self._status
    
    def set_status(self, status: str):
        self._status = status

    def get_num_bad_gusses(self):
        return self._num_bad_guesses
    
    def set_num_bad_guesses(self, num_bad_guesses: int):
        self._num_bad_guesses = num_bad_guesses

    def get_num_missed_letters(self):
        return self._num_missed_letters
    
    def set_num_missed_letters(self, num_missed_letters: int):
        self._num_missed_letters = num_missed_letters

    def get_score(self):
        return self._score
    
    def set_score(self, score: float):
        self._score = score

    def __init__(self, index: int, selected_word: str):
        self._game_index = index
        self._selected_word = selected_word
        self._guess_state = "-" * len(selected_word)
        self._letters_guessed = []
        self._status = "Incomplete"
        self._num_bad_guesses = 0
        self._num_missed_letters = 0
        self._score = 0.0
        self._letter_frequency_dict = {
            "a": 8.17,
            "b": 1.49,
            "c": 2.78,
            "d": 4.25,
            "e": 12.7,
            "f": 2.23,
            "g": 2.02,
            "h": 6.09,
            "i": 6.97,
            "j": 0.15,
            "k": 0.77,
            "l": 4.03,
            "m": 2.41,
            "n": 6.75,
            "o": 7.51,
            "p": 1.93,
            "q": 0.1,
            "r": 5.99,
            "s": 6.33,
            "t": 9.06,
            "u": 2.76,
            "v": 0.98,
            "w": 2.36,
            "x": 0.15,
            "y": 1.97,
            "z": 0.07,
        }

    def end_game(self, success: bool):
        """
        Method that closes a game down. Evaluates the remaining non-visible letters in the word as as boons or penaltiies
        based on the result of the game. Also evaluates the number of bad guesses and missed letter guesses as penaties to
        the overall score. The exact values of the letters are retrieved from the associated frequency dictionary and bad
        guesses shave off 10% of the current score.

        Args:
            success: Boolean representing a successful guess or a surrender.
        """
        total_guess_score_value = 0.0

        for i in range(0, len(self._guess_state)):
            if self._guess_state[i] == "-":
                guess_score_value = self._letter_frequency_dict[self._selected_word[i]]
                total_guess_score_value += guess_score_value

        if success:
            self._status = "Success"
            self._score += total_guess_score_value
        else:
            self._status = "Gave Up"
            self._score -= total_guess_score_value

        total_num_letters_guessed = len(self._letters_guessed)
        if total_num_letters_guessed != 0:
            letter_guess_frequency_penalty = 0.0

            for i in range(0, len(self._letters_guessed)):
                letter_guess_frequency_penalty += self._letter_frequency_dict[self._letters_guessed[i]]
            
            letter_guess_frequency_penalty /= total_num_letters_guessed
            self._score -= letter_guess_frequency_penalty

        if self._num_bad_guesses != 0:
            self._score -= abs(self._score * 0.1 * self._num_bad_guesses)

    def check_word_guess(self, keyboard_guess: str):
        """
        Method to evaluate if a user's word guess matches the selected word for the current game. Case insensitive.

        Args:
            keyboard_guess: String that represents the user's input

        Returns:
            Bool that represents the status of the word guess.
        """
        isCorrect = self._selected_word.lower().__eq__(keyboard_guess)
        if isCorrect:
            self.end_game(isCorrect)
        else:
            self._num_bad_guesses += 1

        return isCorrect

    def check_letter_guess(self, letter: str):
        """
        Method to evaluate if the user's letter guess is found in the selected word in the game. Case insensitive and can
        pick up on multiple positions the letter is found in.

        Args:
            letter: String that represents the user's inputted letter

        Returns: 
            Integer that represents the number of letters that were found in the word form the guess.
        """
        num_letters_in_word = 0

        for i in range(0, len(self._selected_word)):
            match = self._selected_word[i] == letter
            if match:
                num_letters_in_word += 1

                buffer = ""

                if i == 0:
                    buffer += letter
                    buffer += self._guess_state[1:]
                elif i == len(self._selected_word) - 1:
                    buffer += self._guess_state[0:-1]
                    buffer += letter
                else:
                    buffer += self._guess_state[0:i]
                    buffer += letter
                    buffer += self._guess_state[i + 1:]

                self._guess_state = buffer

        if num_letters_in_word == 0:
            self._num_missed_letters += 1
        
        self._letters_guessed.append(letter)

        return num_letters_in_word
    
    def display_game_stats(self):
        """
        Method that will display a formatted string of the current game's stats up to the point of invocation.

        Returns:
            String that is formmated to display the games stats.
        """
        display_template = "{0}\t\t{1}\t\t{2}\t\t{3}\t\t{4}\t\t{5:.2f}"
        
        return display_template.format(self._game_index,
                                       self._selected_word,
                                       self._status,
                                       self._num_bad_guesses,
                                       self._num_missed_letters,
                                       self._score)
