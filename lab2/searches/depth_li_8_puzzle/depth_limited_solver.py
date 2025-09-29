import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from solver_base import SolverBase, PuzzleState


class DepthLimitedSolver(SolverBase):
    """Depth-Limited Search solver for 15-puzzle"""

    def __init__(self, puzzle, depth_limit=20):
        super().__init__(puzzle)
        self.depth_limit = depth_limit

    def solve(self):
        """Solve the puzzle using Depth-Limited Search"""
        start_time = time.time()

        if not self.is_solvable():
            print("Puzzle is not solvable!")
            return False

        if self.initial_state.is_goal(self.board_size):
            print("Puzzle is already solved!")
            return True

        result = self._depth_limited_search(self.initial_state, self.depth_limit)
        self.solve_time = time.time() - start_time

        return result

    def _depth_limited_search(self, state, limit):
        """Recursive depth-limited search"""
        self.nodes_explored += 1
        # Update max frontier size (approximation for recursive calls)
        self.max_frontier_size = max(self.max_frontier_size, state.depth + 1)

        if state.is_goal(self.board_size):
            self.solution_path = state.path
            return True

        if limit <= 0:
            return False

        # Get all possible next states
        neighbors = state.get_neighbors(self.board_size)

        for neighbor in neighbors:
            # Avoid cycles by checking if we're going back to a previous state
            if len(state.path) == 0 or neighbor.path[-1] != self._opposite_move(
                state.path[-1]
            ):
                result = self._depth_limited_search(neighbor, limit - 1)
                if result:
                    return True

        return False

    def _opposite_move(self, move):
        """Return the opposite of a given move"""
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        return opposites.get(move, "")


# Test function
def test_depth_limited():
    import sys
    import os

    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
    from model import Puzzle

    print("=== Depth-Limited Search Test ===")

    # Create a simple 3x3 puzzle for testing
    puzzle = Puzzle(3)
    print("Initial puzzle state:")
    print(puzzle)
    print()

    # Test with different depth limits
    for depth_limit in [10, 15, 20, 25]:
        print(f"\nTrying with depth limit: {depth_limit}")
        solver = DepthLimitedSolver(puzzle, depth_limit)

        if solver.is_solvable():
            print("Puzzle is solvable! Solving with Depth-Limited Search...")
            success = solver.solve()
            solver.print_solution()

            if success:
                break
            else:
                print(f"No solution found within depth limit of {depth_limit}")
        else:
            print("Puzzle is not solvable!")
            break


if __name__ == "__main__":
    test_depth_limited()
