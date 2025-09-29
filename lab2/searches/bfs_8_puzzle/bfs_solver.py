from collections import deque
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from solver_base import SolverBase, PuzzleState


class BFSSolver(SolverBase):
    """Breadth-First Search solver for 15-puzzle"""

    def solve(self):
        """Solve the puzzle using BFS"""
        start_time = time.time()

        if not self.is_solvable():
            print("Puzzle is not solvable!")
            return False

        if self.initial_state.is_goal(self.board_size):
            print("Puzzle is already solved!")
            return True

        # Initialize frontier and explored set
        frontier = deque([self.initial_state])
        explored = set()

        while frontier:
            # Update max frontier size for statistics
            self.max_frontier_size = max(self.max_frontier_size, len(frontier))

            current_state = frontier.popleft()

            # Check if we've explored this state before
            if current_state in explored:
                continue

            explored.add(current_state)
            self.nodes_explored += 1

            # Get all possible next states
            neighbors = current_state.get_neighbors(self.board_size)

            for neighbor in neighbors:
                if neighbor not in explored:
                    if neighbor.is_goal(self.board_size):
                        # Solution found!
                        self.solution_path = neighbor.path
                        self.solve_time = time.time() - start_time
                        return True

                    frontier.append(neighbor)

        # No solution found
        self.solve_time = time.time() - start_time
        return False


# Test function
def test_bfs():
    import sys
    import os

    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
    from model import Puzzle

    print("=== BFS Solver Test ===")

    # Create a simple 3x3 puzzle for faster testing
    puzzle = Puzzle(3)
    print("Initial puzzle state:")
    print(puzzle)
    print()

    solver = BFSSolver(puzzle)

    print("Checking if puzzle is solvable...")
    if solver.is_solvable():
        print("Puzzle is solvable! Solving with BFS...")
        success = solver.solve()
        solver.print_solution()
    else:
        print("Puzzle is not solvable!")


if __name__ == "__main__":
    test_bfs()
