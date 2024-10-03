import os
import time
import numpy as np


class Application:
    """
    Main application class
    """

    def __init__(self):
        self.framerate: int = 30
        self.frametime: float = 1 / self.framerate

        self.width: int = os.get_terminal_size().columns // 2
        self.height: int = os.get_terminal_size().lines

        self.board: np.ndarray | None = None

        self.initialize()

    def initialize(self):
        """
        Initialize the application
        """

        self.board = np.zeros([self.width, self.height], dtype=np.bool_)  # init board with 0's

        os.system("cls" if os.name == "nt" else "clear")  # init ANSI escape codes and clear terminal
        print("\033[?25l", end="", flush=True)  # make cursor invisible

    def draw_board(self):
        """
        Prints the board to the terminal
        """

        output = "\033[H"  # set cursor pos to 0,0
        old_val = -1
        for y in range(self.height):
            for x in range(self.width):
                if (cur_val := self.board[x][y]) != old_val:
                    old_val = cur_val
                    output += "\033[47m" if cur_val else "\033[40m"
                output += "  "
        print(output, end="", flush=True)

    def run(self):
        """
        Runs the application
        """

        while True:
            self.draw_board()
            time.sleep(self.frametime)


def main():
    app = Application()
    app.run()


if __name__ == '__main__':
    main()
