# Lab 2: AI Search Algorithms for 8-Puzzle Problem

## Overview

This lab implements and compares eight different search algorithms for solving the 8-puzzle problem:

### Uninformed Search Algorithms
1. **Breadth-First Search (BFS)** - Explores states level by level, guarantees optimal solution
2. **Depth-First Search (DFS)** - Explores depth-first, memory efficient but not optimal
3. **Depth-Limited Search (DLS)** - DFS with depth limit to prevent infinite loops
4. **Iterative Deepening Search (IDS)** - Combines BFS optimality with DFS space efficiency
5. **Uniform Cost Search (UCS)** - Explores cheapest nodes first
6. **Bidirectional Search** - Searches from both initial and goal states simultaneously

### Informed Search Algorithms
7. **Greedy Best-First Search** - Uses heuristics to guide search toward goal
8. **A* Search** - Optimal search combining path cost and heuristic estimate

## Files Structure

```
lab2/
├── lab/
│   ├── Lab2_AI_Search_Algorithms.tex    # LaTeX source file
│   ├── Lab2_AI_Search_Algorithms.pdf    # Compiled report (10 pages)
│   └── README.md                        # This file
└── searches/                            # Implementation directory
    ├── bfs_8_puzzle/
    │   ├── Start_state.png
    │   └── End_state.png
    ├── greedy_8_puzzle/
    │   ├── Start_state_man.png
    │   └── End_state_man.png
    └── astar_8_puzzle/
        ├── Start_state_man.png
        └── End_state_man.png
```

## Report Contents

The comprehensive 10-page report includes:

1. **Introduction** - Overview of 8-puzzle problem and AI search algorithms
2. **Problem Definition** - State representation, goal configuration, and constraints
3. **Algorithm Implementations** - Detailed code and explanations for all 8 algorithms
4. **Experimental Results** - Performance comparison and analysis
5. **Discussion and Conclusion** - Key findings and algorithmic trade-offs

## Key Features

- **Modular Architecture**: Common base class for consistent measurement
- **Visual State Tracking**: PNG images showing initial and goal states
- **Performance Metrics**: Nodes explored, space complexity, optimality analysis
- **Heuristic Functions**: Manhattan distance and misplaced tiles heuristics
- **Comprehensive Analysis**: Theoretical and empirical performance comparison

## Algorithm Comparison Summary

| Algorithm | Complete | Optimal | Time Complexity | Space Complexity |
|-----------|----------|---------|----------------|------------------|
| BFS | Yes | Yes | O(b^d) | O(b^d) |
| DFS | No | No | O(b^m) | O(bm) |
| DLS | No | No | O(b^l) | O(bl) |
| IDS | Yes | Yes | O(b^d) | O(bd) |
| UCS | Yes | Yes | O(b^d) | O(b^d) |
| Bidirectional | Yes | Yes | O(b^(d/2)) | O(b^(d/2)) |
| Greedy | No | No | O(b^m) | O(b^m) |
| A* | Yes | Yes* | O(b^d) | O(b^d) |

*A* is optimal with admissible heuristics

## Usage

To compile the LaTeX report:
```bash
pdflatex Lab2_AI_Search_Algorithms.tex
```

The report provides both theoretical foundations and practical insights into AI search algorithms, making it valuable for understanding algorithm selection and optimization in constraint satisfaction problems.

## Educational Value

This implementation serves as an excellent educational tool demonstrating:
- Search algorithm behavior and characteristics
- Trade-offs between optimality, completeness, and efficiency  
- Impact of heuristic functions on informed search performance
- Practical considerations for algorithm selection in AI applications