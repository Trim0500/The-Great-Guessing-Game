import random

class StringDatabase:
    """
    Class that represents the pseudo-database of words to use for the games. The file directory is meant to point to a
    file that exists in the same folder as the class itself.

    Fields:
        _file_directory: String that represents the relative directory to use to open a file to read the words from.
        _string_list: A list of strings to be able to select the word for a game instance at random.
    """
    _file_directory: str = ""
    _string_list: list[str] = []

    def get_file_directory(self):
        return self._file_directory
    
    def set_file_directory(self, directory: str):
        self._file_directory = directory

    def get_string_list(self):
        return self._string_list
    
    def set_string_list(self, strong_list: list[str]):
        self._file_directory = strong_list

    def __init__(self, directory):
        self._file_directory = directory

        with open(self._file_directory, "r") as file:
            lines = file.readlines()
            for line in lines:
                seperated_words = line.split(" ")
                for word in seperated_words:
                    if word[-1] == "\n":
                        word = word[0:-1]
                    self._string_list.append(word)

    def get_new_game_word(self):
        """
        Method that will generate a random index to select the word from the list of strings.

        Returns:
            String that represents the randomly selected word to be set as the word to guess for a game instance.
        """
        random_int_limit = len(self._string_list)
        random_index = random.randint(0, random_int_limit - 1)
        selected_word = self._string_list[random_index]

        return selected_word
        