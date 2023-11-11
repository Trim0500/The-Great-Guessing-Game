if __name__ == "__main__":
    import sys
    from Guess import Guess

    gameMode = sys.argv[1]
    if gameMode.lower() != "play" and gameMode.lower() != "test":
        print("Not a valid game mode, exiting...")

        exit()
    else:
        guessing_game = Guess(gameMode)
        guessing_game.start_game()
