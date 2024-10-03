import os
import time
import numpy as np


class Application:
    """
    Main application class
    """

    def __init__(self, debug_info: bool = False):
        self.framerate: int = 4
        self.frametime: float = 1 / self.framerate
        self.cur_time: float = 0
        self.cur_frametime: float = 0

        self.debug_info: bool = debug_info

        self.width: int = os.get_terminal_size().columns // 2
        self.height: int = os.get_terminal_size().lines - int(debug_info)

        self.board: np.ndarray | None = None
        self.gol_rules: np.vectorize = np.vectorize(lambda x: int(x == 3 or x == 4))

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
            for x in range(self.width):
                if (cur_val := self.board[x][y]) != old_val:
                    old_val = cur_val
                    output += "\033[47m" if cur_val else "\033[40m"
                output += "  "
        if self.debug_info:
            output += self.get_debug_info()
        print(output, end="", flush=True)

    def get_debug_info(self) -> str:
        """
        Returns debug information about the renderer
        """

        return f"\033[0mft: {self.cur_frametime * 1000:.2f} ms"

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
        self.board = self.gol_rules(sum(rolled_arrays))

    def plot_random(self):
        """
        Just adds random cells on the board
        """

        for i in range(100):
            self.board[np.random.randint(0, self.width)][np.random.randint(0, self.height)] = 1

    def run(self):
        """
        Runs the application
        """

        self.plot_random()
        while True:
            self.cur_time = time.perf_counter()
            self.draw_board()
            self.step_simulation()
            self.cur_frametime = time.perf_counter() - self.cur_time
            time.sleep(max(.0, self.frametime - self.cur_frametime))


def main():
    app = Application(debug_info=True)
    app.run()


if __name__ == '__main__':
    main()
