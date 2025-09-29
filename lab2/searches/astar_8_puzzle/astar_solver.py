import heapq
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from solver_base import SolverBase, PuzzleState


class AStarSolver(SolverBase):
    """A* Search solver for 8-puzzle using f(n) = g(n) + h(n)"""

    def __init__(self, puzzle, heuristic_type="manhattan"):
        super().__init__(puzzle)
        self.heuristic_type = heuristic_type

    def solve(self):
        """Solve the puzzle using A* Search"""
        start_time = time.time()

        if not self.is_solvable():
            print("Puzzle is not solvable!")
            return False

        if self.initial_state.is_goal(self.board_size):
            print("Puzzle is already solved!")
            return True

        # Priority queue: (f_value, counter, state)
        # f(n) = g(n) + h(n) where g(n) is cost and h(n) is heuristic
        counter = 0
        initial_g = 0  # Cost from start to initial state
        initial_h = self.heuristic(self.initial_state)
        initial_f = initial_g + initial_h

        frontier = [(initial_f, counter, self.initial_state)]
        heapq.heapify(frontier)
        explored = set()
        g_costs = {self.initial_state: 0}  # Track g(n) values

        while frontier:
            # Update max frontier size
            self.max_frontier_size = max(self.max_frontier_size, len(frontier))

            current_f, _, current_state = heapq.heappop(frontier)

            # Skip if already explored
            if current_state in explored:
                continue

            explored.add(current_state)
            self.nodes_explored += 1

            # Check if goal reached
            if current_state.is_goal(self.board_size):
                self.solution_path = current_state.path
                self.solve_time = time.time() - start_time
                return True

            # Expand neighbors
            neighbors = current_state.get_neighbors(self.board_size)
            for neighbor in neighbors:
                if neighbor not in explored:
                    # Calculate g(n) for neighbor (cost from start)
                    g_neighbor = g_costs[current_state] + 1

                    # Only add if we haven't seen this state or found better path
                    if neighbor not in g_costs or g_neighbor < g_costs[neighbor]:
                        g_costs[neighbor] = g_neighbor
                        h_neighbor = self.heuristic(neighbor)
                        f_neighbor = g_neighbor + h_neighbor

                        counter += 1
                        heapq.heappush(frontier, (f_neighbor, counter, neighbor))

        # No solution found
        self.solve_time = time.time() - start_time
        return False

    def heuristic(self, state):
        """Calculate heuristic value for the state"""
        if self.heuristic_type == "manhattan":
            return self._manhattan_distance(state)
        elif self.heuristic_type == "misplaced":
            return self._misplaced_tiles(state)
        else:
            return self._manhattan_distance(state)  # Default to Manhattan

    def _manhattan_distance(self, state):
        """Calculate Manhattan distance heuristic"""
        distance = 0
        board = state.board

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] != 0:  # Skip blank tile
                    value = board[i][j]
                    # Calculate goal position for this value
                    goal_row = (value - 1) // self.board_size
                    goal_col = (value - 1) % self.board_size
                    # Add Manhattan distance
                    distance += abs(i - goal_row) + abs(j - goal_col)

        return distance

    def _misplaced_tiles(self, state):
        """Calculate number of misplaced tiles heuristic"""
        misplaced = 0
        board = state.board

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] != 0:  # Skip blank tile
                    value = board[i][j]
                    # Calculate goal position for this value
                    goal_row = (value - 1) // self.board_size
                    goal_col = (value - 1) % self.board_size

                    if i != goal_row or j != goal_col:
                        misplaced += 1

        return misplaced

    def set_heuristic(self, heuristic_type):
        """Set the heuristic type"""
        if heuristic_type in ["manhattan", "misplaced"]:
            self.heuristic_type = heuristic_type


# Test function
def test_astar():
    import sys
    import os

    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
    from model import Puzzle

    print("=== A* Search Test ===")

    # Create a simple 3x3 puzzle for testing
    puzzle = Puzzle(3)
    print("Initial puzzle state:")
    print(puzzle)
    print()

    # Test with Manhattan distance heuristic
    print("Testing with Manhattan distance heuristic...")
    solver_manhattan = AStarSolver(puzzle, "manhattan")
    if solver_manhattan.is_solvable():
        print("Puzzle is solvable! Solving with A* (Manhattan)...")
        success = solver_manhattan.solve()
        solver_manhattan.print_solution()
    else:
        print("Puzzle is not solvable!")

    print("\n" + "=" * 50 + "\n")

    # Test with misplaced tiles heuristic
    print("Testing with misplaced tiles heuristic...")
    solver_misplaced = AStarSolver(puzzle, "misplaced")
    if solver_misplaced.is_solvable():
        print("Puzzle is solvable! Solving with A* (Misplaced)...")
        success = solver_misplaced.solve()
        solver_misplaced.print_solution()
    else:
        print("Puzzle is not solvable!")


if __name__ == "__main__":
    test_astar()
