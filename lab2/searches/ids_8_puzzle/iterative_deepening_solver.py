import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from solver_base import SolverBase, PuzzleState


class IterativeDeepeningSolver(SolverBase):
    """Iterative Deepening Search solver for 15-puzzle"""

    def __init__(self, puzzle, max_depth=30):
        super().__init__(puzzle)
        self.max_depth = max_depth

    def solve(self):
        """Solve the puzzle using Iterative Deepening Search"""
        start_time = time.time()

        if not self.is_solvable():
            print("Puzzle is not solvable!")
            return False

        if self.initial_state.is_goal(self.board_size):
            print("Puzzle is already solved!")
            return True

        # Try increasing depth limits
        total_nodes = 0
        for depth in range(1, self.max_depth + 1):
            print(f"Trying depth limit: {depth}")

            # Reset counters for each depth iteration
            self.nodes_explored = 0

            # Perform depth-limited search with current depth
            result = self._depth_limited_search(self.initial_state, depth, set())
            total_nodes += self.nodes_explored

            if result:
                self.nodes_explored = total_nodes  # Update with total nodes explored
                self.max_frontier_size = depth  # Max depth reached
                self.solve_time = time.time() - start_time
                print(f"Solution found at depth {depth}!")
                return True

        # No solution found within max depth
        self.nodes_explored = total_nodes
        self.solve_time = time.time() - start_time
        print(f"No solution found within maximum depth of {self.max_depth}")
        return False

    def _depth_limited_search(self, state, limit, explored):
        """Recursive depth-limited search for one iteration"""
        self.nodes_explored += 1

        if state.is_goal(self.board_size):
            self.solution_path = state.path
            return True

        if limit <= 0:
            return False

        # Add current state to explored set
        explored.add(state)

        # Get all possible next states
        neighbors = state.get_neighbors(self.board_size)

        for neighbor in neighbors:
            if neighbor not in explored:
                # Avoid cycles by checking if we're going back to a previous state
                if len(state.path) == 0 or neighbor.path[-1] != self._opposite_move(
                    state.path[-1]
                ):
                    result = self._depth_limited_search(
                        neighbor, limit - 1, explored.copy()
                    )
                    if result:
                        return True

        return False

    def _opposite_move(self, move):
        """Return the opposite of a given move"""
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        return opposites.get(move, "")


# Test function
def test_iterative_deepening():
    import sys
    import os

    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
    from model import Puzzle

    print("=== Iterative Deepening Search Test ===")

    # Create a simple 3x3 puzzle for testing
    puzzle = Puzzle(3)
    print("Initial puzzle state:")
    print(puzzle)
    print()

    solver = IterativeDeepeningSolver(puzzle, max_depth=25)

    print("Checking if puzzle is solvable...")
    if solver.is_solvable():
        print("Puzzle is solvable! Solving with Iterative Deepening Search...")
        success = solver.solve()
        solver.print_solution()
    else:
        print("Puzzle is not solvable!")


if __name__ == "__main__":
    test_iterative_deepening()
