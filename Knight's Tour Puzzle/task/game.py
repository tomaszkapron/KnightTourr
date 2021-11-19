import math
from dataclasses import dataclass


class KnightGame:
    """
            example of board:
         ---------------------
        5| __ __ __ __ __ __ |
        4| __ __  5 __  3 __ |
        3| __  5 __ __ __  3 |
        2| __ __ __  X __ __ |
        1| __  2 __ __ __  1 |
         ---------------------
            1  2  3  4  5  6
        -----------------> y
    """
    DIGITS_IN_BOARD_LINE = 20  # constant used for drawing board
    BOARD_SIZE = 8  # defines size of the chess board
    board_size_x = 0
    board_size_y = 0
    NUM_OF_CHECKS = board_size_y * board_size_x
    END_OF_GAME = False
    GAME_POSSIBLE = True
    WANT_PLAY_YOURSELF = False

    EMPTY_SQUARE_SIZE = int()  # keeps number of digits in empty squares
    EMPTY_SQUARE = str()  # for example '___' or '__'
    KNIGHT = str()  # knight reprezentation for example '_X'
    POSIBLE_KNIGHT = str()  # posible move repr for example '_O'
    position = list()  # keeps position of the knight as a list [x, y]
    board = list()
    possible_moves_list = list()  # keeps positions of possible moves; used to clean the board out of it
    solve_moves_list = list()  # keeps moves list + num of possible moves
    squares_visited = 0

    solver_dict = {}  # dict containing moves. Key is the number of steps visited.
    soler_squares_visited = 1

    def __init__(self):
        self.take_board_size()
        self.create_board()
        self.take_input_position()
        self.take_input_solve()
        self.check_posible_moves(solving=True)
        self.update_solver_list()
        self.solve(self.soler_squares_visited)

        self.move_horse()
        self.check_posible_moves()
        self.display_board()

    def take_board_size(self):
        while True:
            try:
                print("Enter your board dimensions:")
                board_x, board_y = map(int, input().split(' '))
                if board_x > 0 and board_y > 0:
                    self.board_size_x = board_x
                    self.board_size_y = board_y
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid dimensions!")

    def create_board(self):
        self.EMPTY_SQUARE_SIZE = len(str(self.board_size_x * self.board_size_y))
        self.EMPTY_SQUARE = '_' * self.EMPTY_SQUARE_SIZE
        self.KNIGHT = ' ' * (self.EMPTY_SQUARE_SIZE - 1) + 'X'
        self.POSIBLE_KNIGHT = self.generate_figure('K')
        self.board = [[self.EMPTY_SQUARE for _ in range(self.board_size_x)]
                      for _ in range(self.board_size_y)]

    def generate_figure(self, name):
        """:return for example ' K' according to board size"""
        # TODO if len(name) > 1 adjust num of spaces
        return ' ' * (self.EMPTY_SQUARE_SIZE - 1) + str(name)

    def take_input_position(self):
        while True:
            try:
                print("Enter the knight's starting position:")
                y, x = map(int, input().split(' '))
                if self.check_if_on_board(x - 1, y - 1):
                    self.position = [x - 1, y - 1]
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid position!")

    def check_if_on_board(self, x, y):
        return 0 <= y < self.board_size_x and \
               0 <= x < self.board_size_y

    def display_board(self):
        print(f' {(self.board_size_x * (self.EMPTY_SQUARE_SIZE + 1) + 3) * "-"}')
        for i in range(self.board_size_y - 1, -1, -1):
            print(f"{i + 1}| ", end='')
            for n in range(self.board_size_x):
                print(f"{self.board[i][n]} ", end='')
            print('|')
        print(f' {(self.board_size_x * (self.EMPTY_SQUARE_SIZE + 1) + 3) * "-"}')
        column_string = '  ' + ''.join([' ' * self.EMPTY_SQUARE_SIZE +
                                        str(i) for i in range(1, self.board_size_x + 1)])
        print(column_string)

    def move_horse(self, move=None):
        """
        func changes position of a horse, and leave trace ' *' on board
        :param move: if given means it's not a first move
        :return:
        """
        if move:
            self.board[self.position[0]][self.position[1]] = self.generate_figure('*')
            self.position = move
        self.board[self.position[0]][self.position[1]] = self.KNIGHT
        self.squares_visited += 1

    def put_on_board(self, sign):
        self.board[self.position[0]][self.position[1]] = self.generate_figure(sign)

    def check_move(self, x, y):
        """

        :param x:
        :param y:
        :return: True if move is possible
        """
        if self.check_if_on_board(self.position[0] + x, self.position[1] + y):
            return self.board[self.position[0] + x][self.position[1] + y] == self.EMPTY_SQUARE
        else:
            return False

    def check_posible_moves(self, solving: bool=False):
        """
        check's all 8 posibilities for a knight move
        :return:
        """
        num_of_moves = 0
        all_possibilities = [[2, 1], [2, -1], [1, 2], [1, -2], [-1, 2],
                             [-1, -2], [-2, 1], [-2, -1]]
        for possibility in all_possibilities:
            if self.check_move(possibility[0], possibility[1]):
                # TODO: maybe some list comperhension
                for pos in all_possibilities:
                    if self.check_move(possibility[0] + pos[0], possibility[1] + pos[1]):
                        num_of_moves += 1

                self.possible_moves_list.append(
                    [self.position[0] + possibility[0], self.position[1] + possibility[1]])

                self.solve_moves_list.append(SingleMove([possibility[0], possibility[1]], num_of_moves))

                if not solving:
                    self.board[self.position[0] + possibility[0]][self.position[1] + possibility[1]] = \
                        self.generate_figure(num_of_moves)

                num_of_moves = 0

    def take_next_move(self):
        while True:
            try:
                print("Enter your next move:")
                y, x = map(int, input().split(' '))
                mov = [x - 1, y - 1]
                if mov in self.possible_moves_list:
                    self.move(mov)
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid move!", end=' ')

    def move(self, move):
        self.possible_moves_list.remove(move)
        self.clean_board_from_possible_moves()
        self.move_horse(move)

    def clean_board_from_possible_moves(self):
        for move in self.possible_moves_list:
            self.board[move[0]][move[1]] = self.EMPTY_SQUARE
        self.possible_moves_list = list()

    def check_if_end(self):
        if not len(self.possible_moves_list):
            if self.check_win():
                print("What a great tour! Congratulations!")
            else:
                print("No more possible moves!")
                print(f"Your knight visited {self.squares_visited} squares!")
            self.END_OF_GAME = True

    def check_win(self):
        for row in self.board:
            for pole in row:
                if pole == self.EMPTY_SQUARE:
                    return False
        return True

    def take_input_solve(self):
        while True:
            try:
                decision = input("Do you want to try the puzzle? (y/n):")
                if decision == 'y':
                    self.WANT_PLAY_YOURSELF = True
                    break
                elif decision == 'n':
                    self.WANT_PLAY_YOURSELF = False
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid input!", end=' ')

    # TODO create solver class
    def solve(self, squares_visited):
        """
        recursion func solving game
        :return:
        """
        if self.check_win():
            self.GAME_POSSIBLE = True
        elif len(self.solver_dict[1].possible_move_list) == 0:
            self.GAME_POSSIBLE = False
        elif len(self.solver_dict[squares_visited].possible_move_list) > 0:
            self.position[0] += self.solver_dict[squares_visited].possible_move_list[0].move[0]
            self.position[1] += self.solver_dict[squares_visited].possible_move_list[0].move[1]
            self.put_on_board(squares_visited)
            self.soler_squares_visited += 1
            self.solve_moves_list = []
            self.check_posible_moves(solving=True)
            self.update_solver_list()
            self.display_board()  # for debugging
            self.solve(self.soler_squares_visited)
        else:
            self.board[self.position[0]][self.position[1]] = self.EMPTY_SQUARE
            self.soler_squares_visited -= 1
            self.position = self.solver_dict[squares_visited].position
            self.display_board()  # for debuging
            del self.solver_dict[squares_visited].possible_move_list[0]
            self.solve(self.soler_squares_visited)



    def update_solver_list(self):
        self.solve_moves_list.sort(key=lambda x: x.possibilities, reverse=True)  # possible bug
        self.solver_dict[self.soler_squares_visited] = Moves(self.position, self.solve_moves_list)


@dataclass
class Moves:
    position: list
    possible_move_list: list


@dataclass
class SingleMove:
    move: list
    possibilities: int


if __name__ == '__main__':
    game = KnightGame()

    while not game.END_OF_GAME and game.GAME_POSSIBLE and game.WANT_PLAY_YOURSELF:
        game.take_next_move()
        game.check_posible_moves()
        game.display_board()
        game.check_if_end()
