import os
import time
import numpy as np
from argparse import ArgumentParser


class Application:
    """
    Main application class
    """

    def __init__(
            self,
            framerate: float = 30,
            debug_info: bool = False):
        self.framerate: float = framerate
        self.frame_time: float = 1 / self.framerate
        self.frame_start: float = 0
        self.frame_delta: float = 0

        self.debug_info: bool = debug_info

        self.width: int = os.get_terminal_size().columns // 2
        self.height: int = os.get_terminal_size().lines - int(debug_info)

        self.board: np.ndarray | None = None
        self.gol_rules: np.vectorize = np.vectorize(lambda cur, old: int(cur == 3 or (cur == 4 and old == 1)))

        self.initialize()

    def initialize(self):
        """
        Initialize the application
        """

        self.board = np.zeros([self.width, self.height], dtype=np.uint8)  # init board with 0's

        os.system("cls" if os.name == "nt" else "clear")  # init ANSI escape codes and clear terminal
        print("\033[?25l", end="", flush=True)  # make cursor invisible

    def draw_board(self):
        """
        Prints the board to the terminal
        """

        output = "\033[H"  # set cursor pos to 0,0
        old_val = -1
        for y in range(self.height):
            if y > 0:
                output += "\n"
            for x in range(self.width):
                if (cur_val := self.board[x][y]) != old_val:
                    old_val = cur_val
                    output += "\033[47m" if cur_val else "\033[40m"
                output += "  "
        if self.debug_info:
            output += self.get_debug()
        print(output, end="", flush=True)

    def get_debug(self):
        """
        Draws just the debug information
        """

        # \033[{self.height+1};0H - set cursor to bottom of terminal
        # \033[0m - reset all color modifiers
        # \033[0K - clear from cursor to end of line

        return (f"\033[{self.height+1};0H\033[0m\033[0K"
                f"sft: {self.frame_delta * 1000:.2f} ms")

    def step_simulation(self):
        """
        Step GoL simulation
        """

        rolls = [
            (1,  1), (0,  1), (-1,  1),
            (1,  0), (0,  0), (-1,  0),
            (1, -1), (0, -1), (-1, -1)]
        rolled_arrays = map(
            lambda x: np.roll(np.copy(self.board), x, axis=(1, 0)),
            rolls)
        self.board = self.gol_rules(sum(rolled_arrays), self.board)

    def plot_random(self, infill: float):
        """
        Just adds random cells on the board
        """

        x, y = 0, 0
        for i in range(int(self.width * self.height * infill)):
            # don't plot already placed points
            while self.board[x][y] == 1:
                x, y = np.random.randint(0, self.width), np.random.randint(0, self.height)
            self.board[x][y] = 1

    def run(self):
        """
        Runs the application
        """

        self.plot_random(infill=0.1)
        while True:
            self.frame_start = time.perf_counter()
            self.draw_board()
            self.step_simulation()
            self.frame_delta = time.perf_counter() - self.frame_start
            time.sleep(max(.0, self.frame_time - self.frame_delta))


def parse_args():
    """
    Parses command line arguments
    """

    parser = ArgumentParser(
        prog="game of life",
        description="just a game of life")

    parser.add_argument(
        "-f", "--framerate",
        help="set simulation framerate (smaller = slower)",
        type=float,
        default=15.)
    parser.add_argument(
        "-d", "--debug",
        help="display debug information",
        action="store_true",
        default=False)

    return parser.parse_args()


def main():
    args = parse_args()
    app = Application(
        framerate=args.framerate,
        debug_info=args.debug)
    app.run()


if __name__ == '__main__':
    main()
