# AI Lab: Search Algorithms for 8/15-Puzzle

## Lab Overview

This AI laboratory project implements and compares various search algorithms to solve the sliding puzzle problem (8-puzzle and 15-puzzle). The project demonstrates fundamental concepts in Artificial Intelligence including uninformed search strategies, informed search strategies, and heuristic functions.

## Learning Objectives

- Understand the difference between uninformed and informed search strategies
- Compare algorithm performance in terms of optimality, completeness, and efficiency
- Implement various search algorithms from scratch
- Analyze the trade-offs between time and space complexity
- Experience interactive AI problem-solving through visual interfaces

## Project Structure

```
15_puzzle/
├── model.py                    # Core puzzle representation
├── solver_base.py             # Base classes and utilities
├── play.py                    # Main interactive interface
├── README.md                  # This documentation
├── searches/                  # Algorithm implementations
│   ├── bfs_8_puzzle/         # Breadth-First Search
│   │   ├── bfs.py            # Visual BFS interface
│   │   └── bfs_solver.py     # BFS algorithm implementation
│   ├── dfs_8_puzzle/         # Depth-First Search
│   │   ├── dfs.py            # Visual DFS interface
│   │   └── dfs_solver.py     # DFS algorithm implementation
│   ├── depth_li_8_puzzle/    # Depth Limited Search
│   │   ├── dls.py            # Visual DLS interface
│   │   └── depth_limited_solver.py # DLS algorithm implementation
│   ├── astar_8_puzzle/       # A* Search
│   │   └── astar_solver.py   # A* algorithm implementation
│   ├── greedy_8_puzzle/      # Greedy Best-First Search
│   │   └── greedy_best_first_solver.py
│   ├── uniform_8_puzzle/     # Uniform Cost Search
│   │   └── uniform_cost_solver.py
│   └── ids_8_puzzle/         # Iterative Deepening Search
│       └── iterative_deepening_solver.py
└── __pycache__/              # Python cache files
```

## Implemented Algorithms

### Uninformed Search Strategies

#### 1. Breadth-First Search (BFS)

- **Properties**: Complete | Optimal | Time: O(b^d) | Space: O(b^d)
- **Interface**: `searches/bfs_8_puzzle/bfs.py`
- **Algorithm**: `searches/bfs_8_puzzle/bfs_solver.py`
- **Description**: Explores all nodes at depth d before exploring nodes at d+1. Guarantees shortest solution but uses significant memory.

#### 2. Depth-First Search (DFS)

- **Properties**: Incomplete | Non-optimal | Time: O(b^m) | Space: O(bm)
- **Interface**: `searches/dfs_8_puzzle/dfs.py`
- **Algorithm**: `searches/dfs_8_puzzle/dfs_solver.py`
- **Description**: Explores as far as possible along each branch. Memory efficient but may not find solution within reasonable depth.

#### 3. Depth Limited Search (DLS)

- **Properties**: Complete\* | Non-optimal | Time: O(b^l) | Space: O(bl)
- **Interface**: `searches/depth_li_8_puzzle/dls.py`
- **Algorithm**: `searches/depth_li_8_puzzle/depth_limited_solver.py`
- **Description**: DFS with a predetermined depth limit. Complete if solution exists within limit.
- **Features**: Adjustable depth limit (+ and - keys)

#### 4. Uniform Cost Search (UCS)

- **Properties**: Complete | Optimal | Time: O(b^d) | Space: O(b^d)
- **Interface**: `searches/uniform_8_puzzle/ucs.py`
- **Algorithm**: `searches/uniform_8_puzzle/uniform_cost_solver.py`
- **Description**: Expands the least-cost node first. Equivalent to BFS for unit step costs.

#### 5. Iterative Deepening Search (IDS)

- **Properties**: Complete | Optimal | Time: O(b^d) | Space: O(bd)
- **Interface**: `searches/ids_8_puzzle/ids.py`
- **Algorithm**: `searches/ids_8_puzzle/iterative_deepening_solver.py`
- **Description**: Combines benefits of BFS and DFS by gradually increasing depth limit.
- **Features**: Adjustable max depth limit (+ and - keys)

### Informed Search Strategies

#### 6. Greedy Best-First Search

- **Properties**: Incomplete | Non-optimal | Time: O(b^m) | Space: O(b^m)
- **Interface**: `searches/greedy_8_puzzle/greedy.py`
- **Algorithm**: `searches/greedy_8_puzzle/greedy_best_first_solver.py`
- **Heuristics**: Manhattan Distance, Misplaced Tiles
- **Description**: Expands the node that appears closest to goal. Fast but not guaranteed to find optimal solution.
- **Features**: Switch between heuristics (M/T keys)

#### 7. A\* Search

- **Properties**: Complete | Optimal | Time: O(b^d) | Space: O(b^d)
- **Interface**: `searches/astar_8_puzzle/astar.py`
- **Algorithm**: `searches/astar_8_puzzle/astar_solver.py`
- **Heuristics**: Manhattan Distance, Misplaced Tiles
- **Description**: Uses f(n) = g(n) + h(n) to find optimal solution. Combines actual cost with heuristic estimate.
- **Features**: Switch between heuristics (M/T keys)

#### 8. Bidirectional Search

- **Properties**: Complete | Optimal | Time: O(b^d/2) | Space: O(b^d/2)
- **Interface**: `searches/bidirection_8_puzzle/bidirectional.py`
- **Algorithm**: `searches/bidirection_8_puzzle/bidirectional_solver.py`
- **Description**: Searches simultaneously from start and goal states, meeting in the middle.
- **Features**: Visualize bidirectional expansion

#### 9. Hill Climbing Search

- **Properties**: Incomplete | Non-optimal | Time: O(∞) | Space: O(b)
- **Interface**: `searches/hill_climb_8_puzzle/hill_climbing.py`
- **Algorithm**: `searches/hill_climb_8_puzzle/hill_climbing_solver.py`
- **Heuristics**: Manhattan Distance, Misplaced Tiles
- **Description**: Local search algorithm that moves to better neighbors. Uses random restarts to escape local optima.
- **Features**: Adjustable max restarts (+/- keys), heuristic switching

## Interactive Visual Interfaces

### Available Visual Games:

| Algorithm         | Launch Command                                          | Key Controls                               |
| ----------------- | ------------------------------------------------------- | ------------------------------------------ |
| **BFS**           | `python searches/bfs_8_puzzle/bfs.py`                   | `B` - Run BFS                              |
| **DFS**           | `python searches/dfs_8_puzzle/dfs.py`                   | `D` - Run DFS                              |
| **DLS**           | `python searches/depth_li_8_puzzle/dls.py`              | `L` - Run DLS, `+/-` - Adjust depth        |
| **UCS**           | `python searches/uniform_8_puzzle/ucs.py`               | `U` - Run UCS                              |
| **IDS**           | `python searches/ids_8_puzzle/ids.py`                   | `I` - Run IDS, `+/-` - Adjust max depth    |
| **Greedy**        | `python searches/greedy_8_puzzle/greedy.py`             | `G` - Run Greedy, `M/T` - Switch heuristic |
| **A\***           | `python searches/astar_8_puzzle/astar.py`               | `A` - Run A\*, `M/T` - Switch heuristic    |
| **Bidirectional** | `python searches/bidirection_8_puzzle/bidirectional.py` | `B` - Run Bidirectional                    |
| **Hill Climbing** | `python searches/hill_climb_8_puzzle/hill_climbing.py`  | `H` - Run Hill Climbing, `+/-` - Restarts  |

### Universal Controls:

- `SPACE` - Execute next move in solution
- `BACKSPACE` - Previous move in solution
- `R` - Reset puzzle to initial state
- `N` - Generate new puzzle
- Solution navigation when algorithm completes

## Getting Started

### Prerequisites

```bash
# Required packages
conda activate your_environment  # or venv activation
pip install pygame  # For visual interfaces
```

### Quick Start

1. **Test a solver:**

```bash
cd "searches/bfs_8_puzzle"
python bfs_solver.py
```

2. **Launch visual interface:**

```bash
cd "searches/bfs_8_puzzle"
python bfs.py
```

3. **Compare algorithms:**

```bash
# Run each solver and compare performance
python searches/bfs_8_puzzle/bfs_solver.py
python searches/greedy_8_puzzle/greedy_best_first_solver.py
python searches/astar_8_puzzle/astar_solver.py
python searches/hill_climb_8_puzzle/hill_climbing_solver.py
```

4. **Try all visual interfaces:**

```bash
# Test each algorithm's visual interface
python searches/bidirection_8_puzzle/bidirectional.py
python searches/greedy_8_puzzle/greedy.py
python searches/astar_8_puzzle/astar.py
python searches/hill_climb_8_puzzle/hill_climbing.py
```

## Algorithm Performance Analysis

### Typical Performance on 3x3 Puzzle:

| Algorithm         | Avg. Solution Length  | Nodes Explored  | Memory Usage | Time Complexity         | Optimality  |
| ----------------- | --------------------- | --------------- | ------------ | ----------------------- | ----------- |
| **BFS**           | Optimal (20-30 moves) | High (30k+)     | High         | Slow for deep solutions | Optimal     |
| **DFS**           | Variable              | Low-Medium      | Low          | May timeout             | Non-optimal |
| **DLS**           | Variable              | Medium          | Low          | Depends on limit        | Non-optimal |
| **UCS**           | Optimal (20-30 moves) | High (30k+)     | High         | Similar to BFS          | Optimal     |
| **IDS**           | Optimal (20-30 moves) | High (30k+)     | Low          | Slower than BFS         | Optimal     |
| **Greedy**        | Non-optimal (40-90)   | Low (1k-2k)     | Low          | Very fast               | Non-optimal |
| **A\***           | Optimal (20-30 moves) | Low (500-1k)    | Medium       | Fast                    | Optimal     |
| **Bidirectional** | Optimal (20-30 moves) | Medium (5k-10k) | Medium       | Faster than BFS         | Optimal     |
| **Hill Climbing** | Variable/None         | Low             | Very Low     | Fast but often fails    | Incomplete  |

### When to Use Each Algorithm:

- **Need optimal solution**: BFS, UCS, A\*, IDS, Bidirectional
- **Need fast solution**: Greedy Best-First, A\*
- **Limited memory**: DFS, DLS, Hill Climbing
- **Educational comparison**: Try all algorithms on same puzzle
- **Learning heuristics**: Greedy, A\*, Hill Climbing
- **Best performance**: A\* with Manhattan distance

## Heuristic Functions

### Manhattan Distance (Recommended)

```python
distance = sum(|current_row - goal_row| + |current_col - goal_col|)
```

- More informative than misplaced tiles
- Admissible (never overestimates)
- Better performance with A\* and Greedy

### Misplaced Tiles Count

```python
count = number_of_tiles_not_in_correct_position
```

- Simple and fast to compute
- Admissible but less informative
- Good for basic implementations

## Lab Experiments

### Experiment 1: Algorithm Comparison

1. Generate the same random puzzle
2. Run BFS, DFS, DLS, and A\*
3. Compare: solution length, nodes explored, time taken
4. **Question**: Which provides the best balance of optimality and efficiency?

### Experiment 2: Heuristic Analysis

1. Run A\* with Manhattan Distance
2. Run A\* with Misplaced Tiles
3. **Question**: How much does heuristic quality affect performance?

### Experiment 3: Depth Limit Tuning

1. Run DLS with limits: 10, 15, 20, 25, 30
2. Record success rate and performance
3. **Question**: What's the minimum depth limit for consistent solutions?

### Experiment 4: Puzzle Complexity

1. Test on puzzles requiring 10, 20, 30+ moves
2. Observe how each algorithm scales
3. **Question**: Which algorithms become impractical first?

## Technical Implementation Notes

### Solvability Detection

- Uses inversion counting algorithm
- Even grids: considers blank position
- Odd grids: checks inversion parity
- Prevents unsolvable puzzle attempts

### State Representation

- 2D board stored as list of lists
- Blank tile represented as 0
- States converted to tuples for hashing
- Path tracking with move sequences

### Memory Optimization

- Explored states stored in sets (O(1) lookup)
- Frontier implemented with appropriate data structures:
  - BFS: deque (FIFO)
  - DFS: stack (LIFO)
  - A\*/Greedy: priority queue (heapq)

## Expected Learning Outcomes

After completing this lab, students should understand:

1. **Search Strategy Trade-offs**: Complete vs optimal vs efficient
2. **Heuristic Design**: Properties of good heuristic functions
3. **Algorithm Selection**: Choosing appropriate algorithm for constraints
4. **Performance Analysis**: Measuring and comparing algorithm efficiency
5. **Implementation Skills**: Practical AI algorithm programming

## Troubleshooting

### Common Issues:

**Pygame not found:**

```bash
pip install pygame
conda install pygame  # if using conda
```

**Python path issues:**

- Ensure you're running from correct directory
- Check that `model.py` and `solver_base.py` are accessible

**Performance issues:**

- Use 3x3 puzzles for testing
- Limit depth for DFS/DLS algorithms
- Try Greedy search for quick results

## References & Further Reading

- Russell, S. & Norvig, P. "Artificial Intelligence: A Modern Approach"
- Algorithms textbook: Search strategies and heuristic functions
- Original 15-puzzle by Noyes Chapman (1880)

---

### Lab Assignment Ideas:

1. **Performance Report**: Compare all algorithms on 10 random puzzles
2. **Heuristic Design**: Implement and test a new heuristic function
3. **Optimization Challenge**: Improve one algorithm's performance
4. **Visualization**: Create graphs showing performance trends
5. **Extension**: Implement bidirectional search or IDA\*

Happy Problem Solving!
