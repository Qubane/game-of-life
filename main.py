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

        self.board: np.ndarray = np.zeros([self.width, self.height], dtype=np.bool_)

    def run(self):
        """
        Runs the application
        """

        while True:
            time.sleep(self.frametime)


def main():
    app = Application()
    app.run()


if __name__ == '__main__':
    main()
