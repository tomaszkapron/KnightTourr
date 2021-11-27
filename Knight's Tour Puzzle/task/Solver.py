from dataclasses import dataclass

# TODO: ADD coping


class Solver:

    def __init__(self, knight_game):
        self.kg = knight_game

    def solve(self, squares_vis):
        if len(self.kg.solver_dict[squares_vis].possible_move_list) > 0:
            self.kg.position[0] += self.kg.solver_dict[squares_vis].possible_move_list[0].move[0]
            self.kg.position[1] += self.kg.solver_dict[squares_vis].possible_move_list[0].move[1]

            self.kg.soler_squares_visited += 1
            self.kg.put_on_board(self.kg.soler_squares_visited)

            self.kg.solve_moves_list = []
            self.kg.check_posible_moves(solving=True)
            self.update_solver_list()
        else:
            self.kg.board[self.kg.position[0]][self.kg.position[1]] = self.kg.EMPTY_SQUARE
            self.kg.soler_squares_visited -= 1
            x = self.kg.solver_dict[self.kg.soler_squares_visited].position[0]
            y = self.kg.solver_dict[self.kg.soler_squares_visited].position[1]
            self.kg.position = [x, y]
            del self.kg.solver_dict[self.kg.soler_squares_visited].possible_move_list[0]

    def solving(self):
        self.kg.check_posible_moves(solving=True)
        self.update_solver_list()

        while True:
            if self.kg.check_win():
                self.kg.GAME_POSSIBLE = True
                break
            elif len(self.kg.solver_dict[1].possible_move_list) == 0:
                self.kg.GAME_POSSIBLE = False
                break
            self.solve(self.kg.soler_squares_visited)

    def update_solver_list(self):
        self.kg.solve_moves_list.sort(key=lambda x: x.possibilities, reverse=True)
        x = self.kg.position[0]
        y = self.kg.position[1]
        self.kg.solver_dict[self.kg.soler_squares_visited] = Moves([x, y], self.kg.solve_moves_list)


@dataclass
class Moves:
    position: list
    possible_move_list: list
