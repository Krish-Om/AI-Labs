import copy
from collections import deque
import heapq
import time
from model import Puzzle


class PuzzleState:
    """Represents a state in the puzzle search space"""

    def __init__(self, board, blank_pos, path=None, cost=0, depth=0):
        self.board = board
        self.blank_pos = blank_pos
        self.path = path if path else []
        self.cost = cost
        self.depth = depth
        self.board_tuple = self._board_to_tuple()

    def _board_to_tuple(self):
        """Convert board to tuple for hashing"""
        return tuple(tuple(row) for row in self.board)

    def __hash__(self):
        return hash(self.board_tuple)

    def __eq__(self, other):
        return self.board_tuple == other.board_tuple

    def __lt__(self, other):
        """For priority queue comparison"""
        return self.cost < other.cost

    def get_neighbors(self, board_size):
        """Get all valid neighboring states"""
        neighbors = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # UP, DOWN, LEFT, RIGHT
        direction_names = ["UP", "DOWN", "LEFT", "RIGHT"]

        for i, (dr, dc) in enumerate(directions):
            new_blank_r = self.blank_pos[0] + dr
            new_blank_c = self.blank_pos[1] + dc

            # Check bounds
            if 0 <= new_blank_r < board_size and 0 <= new_blank_c < board_size:
                # Create new board state
                new_board = copy.deepcopy(self.board)

                # Swap blank with adjacent tile
                new_board[self.blank_pos[0]][self.blank_pos[1]] = new_board[
                    new_blank_r
                ][new_blank_c]
                new_board[new_blank_r][new_blank_c] = 0

                new_path = self.path + [direction_names[i]]
                new_state = PuzzleState(
                    new_board,
                    (new_blank_r, new_blank_c),
                    new_path,
                    self.cost + 1,
                    self.depth + 1,
                )
                neighbors.append(new_state)

        return neighbors

    def is_goal(self, board_size):
        """Check if this state is the goal state"""
        for i in range(board_size):
            for j in range(board_size):
                expected_value = i * board_size + j + 1
                if i == board_size - 1 and j == board_size - 1:
                    expected_value = 0  # Bottom right should be blank
                if self.board[i][j] != expected_value:
                    return False
        return True


class SolverBase:
    """Base class for puzzle solvers"""

    def __init__(self, puzzle):
        self.initial_state = PuzzleState(copy.deepcopy(puzzle.board), puzzle.blankPos)
        self.board_size = puzzle.boardSize
        self.nodes_explored = 0
        self.max_frontier_size = 0
        self.solution_path = []
        self.solve_time = 0

    def solve(self):
        """Override this method in subclasses"""
        raise NotImplementedError("Subclasses must implement solve method")

    def is_solvable(self):
        """Check if the puzzle is solvable using inversion count"""
        # Convert board to 1D array excluding blank
        flat_board = []
        blank_row = 0

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.initial_state.board[i][j] == 0:
                    blank_row = i
                else:
                    flat_board.append(self.initial_state.board[i][j])

        # Count inversions
        inversions = 0
        for i in range(len(flat_board)):
            for j in range(i + 1, len(flat_board)):
                if flat_board[i] > flat_board[j]:
                    inversions += 1

        # For 4x4 grid (15-puzzle):
        # - If blank is on even row counting from bottom, inversions must be odd
        # - If blank is on odd row counting from bottom, inversions must be even
        if self.board_size % 2 == 0:  # Even grid size
            blank_row_from_bottom = self.board_size - blank_row
            if blank_row_from_bottom % 2 == 0:  # Even row from bottom
                return inversions % 2 == 1
            else:  # Odd row from bottom
                return inversions % 2 == 0
        else:  # Odd grid size
            return inversions % 2 == 0

    def print_solution(self):
        """Print the solution path and statistics"""
        if self.solution_path:
            print(f"Solution found in {len(self.solution_path)} moves!")
            print(f"Path: {' -> '.join(self.solution_path)}")
        else:
            print("No solution found!")

        print(f"Nodes explored: {self.nodes_explored}")
        print(f"Max frontier size: {self.max_frontier_size}")
        print(f"Time taken: {self.solve_time:.4f} seconds")
        print()


def manhattan_distance(board, board_size):
    """Calculate Manhattan distance heuristic"""
    distance = 0
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] != 0:
                target_value = board[i][j]
                target_row = (target_value - 1) // board_size
                target_col = (target_value - 1) % board_size
                distance += abs(i - target_row) + abs(j - target_col)
    return distance


def misplaced_tiles(board, board_size):
    """Calculate number of misplaced tiles heuristic"""
    misplaced = 0
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] != 0:
                expected_value = i * board_size + j + 1
                if i == board_size - 1 and j == board_size - 1:
                    expected_value = 0
                if board[i][j] != expected_value:
                    misplaced += 1
    return misplaced
