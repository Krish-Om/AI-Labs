import time
from collections import deque
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from solver_base import SolverBase, PuzzleState
import copy


class BidirectionalSolver(SolverBase):
    """Bidirectional Search solver for 8-puzzle"""

    def solve(self):
        """Solve the puzzle using Bidirectional Search"""
        start_time = time.time()

        if not self.is_solvable():
            print("Puzzle is not solvable!")
            return False

        if self.initial_state.is_goal(self.board_size):
            print("Puzzle is already solved!")
            return True

        # Create goal state
        goal_board = self._create_goal_state()
        goal_state = PuzzleState(goal_board, self._find_blank_position(goal_board))

        # Initialize frontiers for both directions
        forward_frontier = deque([self.initial_state])
        backward_frontier = deque([goal_state])

        # Explored sets for both directions
        forward_explored = {self.initial_state: self.initial_state}
        backward_explored = {goal_state: goal_state}

        while forward_frontier or backward_frontier:
            # Update max frontier size
            self.max_frontier_size = max(
                self.max_frontier_size, len(forward_frontier) + len(backward_frontier)
            )

            # Expand forward search
            if forward_frontier:
                current_forward = forward_frontier.popleft()

                # Check if we've met the backward search
                if current_forward in backward_explored:
                    # Found intersection - construct solution
                    self._construct_bidirectional_path(
                        current_forward, backward_explored[current_forward]
                    )
                    self.solve_time = time.time() - start_time
                    return True

                self.nodes_explored += 1
                neighbors = current_forward.get_neighbors(self.board_size)

                for neighbor in neighbors:
                    if neighbor not in forward_explored:
                        forward_explored[neighbor] = neighbor
                        forward_frontier.append(neighbor)

            # Expand backward search
            if backward_frontier:
                current_backward = backward_frontier.popleft()

                # Check if we've met the forward search
                if current_backward in forward_explored:
                    # Found intersection - construct solution
                    self._construct_bidirectional_path(
                        forward_explored[current_backward], current_backward
                    )
                    self.solve_time = time.time() - start_time
                    return True

                self.nodes_explored += 1
                neighbors = current_backward.get_neighbors(self.board_size)

                for neighbor in neighbors:
                    if neighbor not in backward_explored:
                        backward_explored[neighbor] = neighbor
                        backward_frontier.append(neighbor)

        # No solution found
        self.solve_time = time.time() - start_time
        return False

    def _create_goal_state(self):
        """Create the goal state board"""
        goal_board = []
        num = 1
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                if i == self.board_size - 1 and j == self.board_size - 1:
                    row.append(0)  # Blank tile at bottom-right
                else:
                    row.append(num)
                    num += 1
            goal_board.append(row)
        return goal_board

    def _find_blank_position(self, board):
        """Find position of blank tile (0) in board"""
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def _construct_bidirectional_path(self, forward_state, backward_state):
        """Construct the solution path from bidirectional meeting point"""
        # Forward path from start to meeting point
        forward_path = forward_state.path

        # Backward path from meeting point to goal (need to reverse)
        backward_path = backward_state.path
        backward_path.reverse()

        # Reverse the direction of backward moves
        direction_reversal = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT",
        }

        reversed_backward = [direction_reversal[move] for move in backward_path]

        # Combine paths
        self.solution_path = forward_path + reversed_backward


# Test function
def test_bidirectional():
    import sys
    import os

    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
    from model import Puzzle

    print("=== Bidirectional Search Test ===")

    # Create a simple 3x3 puzzle for testing
    puzzle = Puzzle(3)
    print("Initial puzzle state:")
    print(puzzle)
    print()

    solver = BidirectionalSolver(puzzle)

    print("Checking if puzzle is solvable...")
    if solver.is_solvable():
        print("Puzzle is solvable! Solving with Bidirectional Search...")
        success = solver.solve()
        solver.print_solution()
    else:
        print("Puzzle is not solvable!")


if __name__ == "__main__":
    test_bidirectional()
