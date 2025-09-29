import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from solver_base import SolverBase, PuzzleState


class DFSSolver(SolverBase):
    """Depth-First Search solver for 15-puzzle"""

    def __init__(self, puzzle, max_depth=50):
        super().__init__(puzzle)
        self.max_depth = max_depth

    def solve(self):
        """Solve the puzzle using DFS with depth limit to prevent infinite loops"""
        start_time = time.time()

        if not self.is_solvable():
            print("Puzzle is not solvable!")
            return False

        if self.initial_state.is_goal(self.board_size):
            print("Puzzle is already solved!")
            return True

        # Initialize stack and explored set
        stack = [self.initial_state]
        explored = set()

        while stack:
            # Update max frontier size for statistics
            self.max_frontier_size = max(self.max_frontier_size, len(stack))

            current_state = stack.pop()

            # Check depth limit
            if current_state.depth > self.max_depth:
                continue

            # Check if we've explored this state before
            if current_state in explored:
                continue

            explored.add(current_state)
            self.nodes_explored += 1

            # Check if goal
            if current_state.is_goal(self.board_size):
                self.solution_path = current_state.path
                self.solve_time = time.time() - start_time
                return True

            # Get all possible next states and add to stack (in reverse order for consistent behavior)
            neighbors = current_state.get_neighbors(self.board_size)
            neighbors.reverse()  # Reverse to maintain consistent exploration order

            for neighbor in neighbors:
                if neighbor not in explored and neighbor.depth <= self.max_depth:
                    stack.append(neighbor)

        # No solution found within depth limit
        self.solve_time = time.time() - start_time
        return False


# Test function
def test_dfs():
    import sys
    import os

    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
    from model import Puzzle

    print("=== DFS Solver Test ===")

    # Create a simple 3x3 puzzle for testing
    puzzle = Puzzle(3)
    print("Initial puzzle state:")
    print(puzzle)
    print()

    solver = DFSSolver(puzzle, max_depth=30)  # Limit depth to prevent long runs

    print("Checking if puzzle is solvable...")
    if solver.is_solvable():
        print("Puzzle is solvable! Solving with DFS...")
        success = solver.solve()
        solver.print_solution()

        if not success:
            print(
                f"DFS could not find solution within depth limit of {solver.max_depth}"
            )
    else:
        print("Puzzle is not solvable!")


if __name__ == "__main__":
    test_dfs()
