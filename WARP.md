# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

AI-Labs is a comprehensive collection of artificial intelligence laboratory experiments implemented in Python, covering fundamental AI concepts from search algorithms to machine learning techniques. The repository is structured as a series of educational labs, each focusing on specific AI methodologies.

## Development Environment Setup

### Dependencies Management
This project uses `uv` as the Python dependency manager with dependencies defined in `pyproject.toml`.

```bash
# Install dependencies using uv
uv sync

# Add new dependencies
uv add package-name

# Activate virtual environment
uv shell
```

### Required Dependencies
The project includes scientific computing and AI libraries:
- **Core**: `numpy`, `pandas`, `scipy`, `matplotlib`
- **Machine Learning**: `scikit-learn`, `scikit-fuzzy` 
- **Interactive**: `jupyter`, `ipykernel`
- **Games/Visualization**: `pygame`
- **Graph Processing**: `networkx`

## Lab Architecture and Components

### Lab Structure
Each lab follows a consistent structure with specific focus areas:

```
lab{N}/
├── {algorithm}.ipynb          # Jupyter notebook implementation
├── Lab{N}_{Topic}_Report.pdf  # Technical report
├── Lab{N}_{Topic}_Report.tex  # LaTeX source
├── *.py                      # Python modules (if applicable)
├── *.csv                     # Parameter/data files
└── README.md                 # Lab-specific documentation
```

### Lab Topics and Implementations

#### Lab 1: Snake AI Agents
- PDF documentation only
- Focus on autonomous game-playing agents

#### Lab 2: Search Algorithms (8/15-Puzzle)
- **Core Components**:
  - `model.py`: Puzzle representation and game mechanics
  - `solver_base.py`: Base classes, PuzzleState, heuristic functions
  - `play.py`: Interactive interface for algorithm testing
- **Algorithms**: BFS, DFS, DLS, UCS, IDS, Greedy, A*, Bidirectional, Hill Climbing
- **Interactive gameplay**: Pygame-based visual interfaces for each algorithm
- **Architecture**: Object-oriented design with state representation, search strategies, and heuristic evaluation

#### Lab 3: Genetic Algorithms
- `Genetic_Algorithm.ipynb`: Quadratic equation solving using GA
- **Key Features**: Roulette wheel selection, single-point crossover, bit-flip mutation
- Binary representation with configurable integer/fraction bits

#### Lab 4: Fuzzy Logic
- `fuzzy_logic.ipynb`: Fuzzy logic system implementation
- Uses `scikit-fuzzy` for fuzzy set operations

#### Lab 5: Multi-Layer Perceptron (MLP)
- `MLP.ipynb`: Neural network implementation from scratch
- Parameter configuration via `parameters.csv`

#### Lab 6: Recurrent Neural Networks (RNN)
- `RNN_anam.ipynb`: RNN implementation and analysis
- Focus on sequence processing and temporal dependencies

#### Lab 7: Naive Bayes Classification
- `naive_bayes.ipynb`: Custom implementation of Naive Bayes classifier
- Includes accuracy metrics and probability calculations

#### Lab 8: Logic Programming
- `logic_lab.ipynb`: Logical reasoning and inference systems

## Common Development Commands

### Running Jupyter Notebooks
```bash
# Start Jupyter Lab (recommended for development)
uv run jupyter lab

# Start classic Jupyter Notebook
uv run jupyter notebook

# Run specific notebook
uv run jupyter nbconvert --execute --to notebook {notebook}.ipynb
```

### Lab 2 Search Algorithms (Special Commands)
```bash
# Run individual search algorithm solvers
uv run python lab2/searches/bfs_8_puzzle/bfs_solver.py
uv run python lab2/searches/astar_8_puzzle/astar_solver.py
uv run python lab2/searches/greedy_8_puzzle/greedy_best_first_solver.py

# Launch visual/interactive interfaces
uv run python lab2/searches/bfs_8_puzzle/bfs.py
uv run python lab2/searches/astar_8_puzzle/astar.py
uv run python lab2/play.py

# Test puzzle solver interactively
cd lab2 && uv run python play.py
```

### Python Script Execution
```bash
# Run Python modules from project root
uv run python lab2/model.py
uv run python lab2/solver_base.py

# Execute with proper module path
cd lab2 && uv run python -c "from model import Puzzle; p = Puzzle(3); print(p)"
```

### LaTeX Document Compilation
```bash
# Compile LaTeX reports (requires LaTeX installation)
cd lab{N} && pdflatex Lab{N}_{Topic}_Report.tex

# Clean LaTeX auxiliary files
rm *.aux *.log *.fdb_latexmk *.fls *.out *.synctex.gz
```

## Code Architecture Patterns

### Search Algorithm Framework (Lab 2)
- **State Representation**: `PuzzleState` class encapsulates board state, path, cost, and depth
- **Base Solver Pattern**: `SolverBase` provides common functionality for all search algorithms
- **Strategy Pattern**: Each algorithm implements specific search strategy while inheriting common methods
- **Heuristic Functions**: Modular heuristic implementations (Manhattan distance, misplaced tiles)

### Machine Learning Architecture (Labs 3-8)
- **Notebook-based Development**: Each lab uses Jupyter notebooks for experimentation and visualization
- **Parameter Configuration**: External CSV files for algorithm parameters and experimental settings
- **Class-based Implementation**: Object-oriented approach for algorithm implementations (e.g., `GeneticAlgorithm`, `NaiveBayes`)
- **Visualization Integration**: Matplotlib integration for performance analysis and result visualization

## Lab-Specific Guidance

### Lab 2 Development Notes
- **Solvability**: Always check puzzle solvability using inversion counting before running algorithms
- **Memory Usage**: BFS and UCS require significant memory for large search spaces
- **Performance Testing**: Use 3x3 puzzles for initial testing, 4x4 for performance analysis
- **Visual Debugging**: Interactive interfaces help understand algorithm behavior

### Machine Learning Labs (3-8)
- **Parameter Tuning**: Each lab has specific parameter files that should be modified for experimentation
- **Reproducibility**: Set random seeds for consistent results across runs
- **Documentation**: Each notebook includes theoretical background and implementation details
- **Report Generation**: LaTeX sources are provided for formal report compilation

### Development Best Practices for this Codebase
- Use `uv shell` to activate the virtual environment before development
- Run Jupyter notebooks for interactive development and testing
- For Lab 2, test search algorithms on simple 3x3 puzzles first
- Parameter files (CSV) should be modified to experiment with different algorithm configurations
- LaTeX reports provide comprehensive documentation of theoretical foundations

## File Extensions and Tooling
- **`.ipynb`**: Jupyter notebooks - primary development interface
- **`.py`**: Python modules for reusable components and standalone scripts  
- **`.tex`**: LaTeX sources for academic reports
- **`.csv`**: Parameter and data configuration files
- **`.pdf`**: Generated reports and documentation

## Dependencies for Visual Components
- **pygame**: Required for Lab 2 interactive puzzle interfaces
- **matplotlib**: Essential for all labs for plotting and visualization
- **ipykernel**: Needed for Jupyter notebook execution in virtual environment

This codebase represents educational AI implementations with emphasis on understanding algorithmic behavior, experimental parameter tuning, and academic documentation standards.