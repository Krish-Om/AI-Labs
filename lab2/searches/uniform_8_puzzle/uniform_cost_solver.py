import heapq
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from solver_base import SolverBase, PuzzleState


class UniformCostSolver(SolverBase):
    """Uniform Cost Search solver for 15-puzzle"""

    def solve(self):
        """Solve the puzzle using Uniform Cost Search (equivalent to BFS for this problem)"""
        start_time = time.time()

        if not self.is_solvable():
            print("Puzzle is not solvable!")
            return False

        if self.initial_state.is_goal(self.board_size):
            print("Puzzle is already solved!")
            return True

        # Initialize priority queue (min-heap) with cost as priority
        # Format: (cost, counter, state) - counter prevents comparison of states
        frontier = [(0, 0, self.initial_state)]
        explored = set()
        counter = 0

        while frontier:
            # Update max frontier size for statistics
            self.max_frontier_size = max(self.max_frontier_size, len(frontier))

            current_cost, _, current_state = heapq.heappop(frontier)

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

            # Get all possible next states
            neighbors = current_state.get_neighbors(self.board_size)

            for neighbor in neighbors:
                if neighbor not in explored:
                    counter += 1
                    # Each move has uniform cost of 1
                    heapq.heappush(frontier, (neighbor.cost, counter, neighbor))

        # No solution found
        self.solve_time = time.time() - start_time
        return False


# Test function
def test_uniform_cost():
    import sys
    import os

    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
    from model import Puzzle

    print("=== Uniform Cost Search Test ===")

    # Create a simple 3x3 puzzle for testing
    puzzle = Puzzle(3)
    print("Initial puzzle state:")
    print(puzzle)
    print()

    solver = UniformCostSolver(puzzle)

    print("Checking if puzzle is solvable...")
    if solver.is_solvable():
        print("Puzzle is solvable! Solving with Uniform Cost Search...")
        success = solver.solve()
        solver.print_solution()
    else:
        print("Puzzle is not solvable!")


if __name__ == "__main__":
    test_uniform_cost()
