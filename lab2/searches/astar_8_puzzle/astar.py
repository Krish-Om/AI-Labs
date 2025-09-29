import pygame
import sys
import time
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import model
from astar_solver import AStarSolver

pygame.init()
BOARD_SIZE = 3

# Global variables for A* solution
solution_path = []
current_step = 0
solving = False
auto_play = False
last_move_time = 0
original_puzzle_state = None
heuristic_type = "manhattan"  # Default heuristic


# UI
size = width, height = 480, 480
screen = pygame.display.set_mode((size), pygame.NOFRAME)
FPS = 60

# FONTS
tileFont = pygame.font.SysFont("", 72)

color = (80, 20, 30)
borderColor = (50, 0, 20)
tileColor = (162, 5, 44)
fontColor = (255, 255, 255)
blankTileColor = (60, 0, 30)


def gameLoop():
    global solution_path, current_step, solving, auto_play, last_move_time, original_puzzle_state, heuristic_type

    clock = pygame.time.Clock()
    puzzle = model.Puzzle(boardSize=BOARD_SIZE)

    print("\n 8-Puzzle with A* Search Solver")
    print("Controls:")
    print("  A: Run A* search")
    print("  H: Toggle heuristic (Manhattan/Misplaced)")
    print("  SPACE: Show next move in solution")
    print("  S: Auto play the moves")
    print("  R: Shuffle puzzle")
    print("  ESC: Quit")
    print("  Click: Manual move")
    print(f"\n Current heuristic: {heuristic_type.title()}")
    print()

    while True:
        current_time = time.time()

        for event in pygame.event.get():
            handleInput(event, puzzle)

        # Handle auto-play
        if auto_play and solution_path and current_step < len(solution_path):
            if current_time - last_move_time > 0.5:  # 0.5 second delay between moves
                executeNextMove(puzzle)
                last_move_time = current_time

        drawPuzzle(puzzle)
        pygame.display.flip()
        clock.tick(FPS)


def handleInput(event, puzzle):
    global solution_path, current_step, solving, auto_play, original_puzzle_state, heuristic_type

    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            puzzle.shuffle()
            resetSolution()
            print("Puzzle shuffled!")
            printPuzzleState(puzzle)
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_a:
            # Run A* search
            if puzzle.checkWin():
                print("Puzzle is already solved! Press 'R' to shuffle and try again.")
            else:
                runAStarSearch(puzzle)
        elif event.key == pygame.K_h:
            # Toggle heuristic
            heuristic_type = (
                "misplaced" if heuristic_type == "manhattan" else "manhattan"
            )
            print(f"Switched to {heuristic_type.title()} heuristic")
            resetSolution()
        elif event.key == pygame.K_SPACE:
            # Show next move
            if solution_path and current_step < len(solution_path):
                executeNextMove(puzzle)
            else:
                print("No solution loaded or solution complete!")
        elif event.key == pygame.K_s:
            # Toggle auto-play
            if solution_path:
                auto_play = not auto_play
                if auto_play:
                    print(
                        "Auto-play ENABLED - moves will execute automatically every 0.5 seconds"
                    )
                else:
                    print("Auto-play DISABLED - use SPACE to execute moves manually")
            else:
                print("No solution loaded! Press 'A' to run A* Search first.")
    elif event.type == pygame.MOUSEBUTTONUP:
        # Manual move (only if not in solution mode)
        if not solving and not solution_path:
            pos = pygame.mouse.get_pos()
            puzzleCoord = (
                pos[1] * puzzle.boardSize // height,
                pos[0] * puzzle.boardSize // width,
            )

            dir = (
                puzzleCoord[0] - puzzle.blankPos[0],
                puzzleCoord[1] - puzzle.blankPos[1],
            )

            if dir == puzzle.RIGHT:
                if puzzle.move(puzzle.RIGHT):
                    print("Manual move: RIGHT")
                    printPuzzleState(puzzle)
            elif dir == puzzle.LEFT:
                if puzzle.move(puzzle.LEFT):
                    print("Manual move: LEFT")
                    printPuzzleState(puzzle)
            elif dir == puzzle.DOWN:
                if puzzle.move(puzzle.DOWN):
                    print("Manual move: DOWN")
                    printPuzzleState(puzzle)
            elif dir == puzzle.UP:
                if puzzle.move(puzzle.UP):
                    print("Manual move: UP")
                    printPuzzleState(puzzle)


def drawPuzzle(puzzle):
    screen.fill(color)

    for i in range(puzzle.boardSize):
        for j in range(puzzle.boardSize):
            currentTileColor = tileColor
            numberText = str(puzzle[i][j])

            if puzzle[i][j] == 0:
                currentTileColor = borderColor
                numberText = ""

            rect = pygame.Rect(
                j * width // puzzle.boardSize,
                i * height // puzzle.boardSize,
                width // puzzle.boardSize,
                height // puzzle.boardSize,
            )

            pygame.draw.rect(screen, currentTileColor, rect)
            pygame.draw.rect(screen, borderColor, rect, 1)

            fontImg = tileFont.render(numberText, 1, fontColor)
            screen.blit(
                fontImg,
                (
                    j * width // puzzle.boardSize
                    + (width // puzzle.boardSize - fontImg.get_width()) // 2,
                    i * height // puzzle.boardSize
                    + (height // puzzle.boardSize - fontImg.get_height()) // 2,
                ),
            )

    # Show "SOLVED!" message when puzzle is completed
    if puzzle.checkWin():
        # Create semi-transparent overlay
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Create and display "SOLVED!" text
        solved_font = pygame.font.SysFont("", 96, bold=True)
        solved_text = solved_font.render("SOLVED!", True, (255, 255, 255))
        text_rect = solved_text.get_rect(center=(width // 2, height // 2))
        screen.blit(solved_text, text_rect)


def printPuzzleState(puzzle):
    """Print current puzzle state to console"""
    if puzzle.checkWin():
        print("\n" + "=" * 50)
        print(" PUZZLE SOLVED! ")
        print("=" * 50)
        print("Controls:")
        print("  A: Run A* search")
        print("  H: Toggle heuristic (Manhattan/Misplaced)")
        print("  SPACE: Show next move in solution")
        print("  S: Auto play the moves")
        print("  R: Shuffle puzzle")
        print("  ESC: Quit")
        print("  Click: Manual move")
        print("=" * 50)


def runAStarSearch(puzzle):
    """Run A* Search algorithm and store solution"""
    global solution_path, current_step, solving, original_puzzle_state, auto_play

    print("\n" + "=" * 50)
    print(f"Running A* Search with {heuristic_type.title()} heuristic...")
    print("=" * 50)

    # Store original puzzle state
    original_puzzle_state = {
        "board": [row[:] for row in puzzle.board],
        "blankPos": puzzle.blankPos,
    }

    printPuzzleState(puzzle)

    solving = True
    auto_play = False

    try:
        solver = AStarSolver(puzzle, heuristic_type=heuristic_type)

        # Check solvability
        if not solver.is_solvable():
            print(" Puzzle is not solvable!")
            solving = False
            return

        print(" Puzzle is solvable! Searching for solution...")

        # Solve with A* Search
        start_time = time.time()
        success = solver.solve()

        if success:
            solution_path = solver.solution_path
            current_step = 0

            print(f"\n A* SEARCH ANALYSIS:")
            print(f"    -Heuristic: {heuristic_type.title()}")
            print(f"    -Solution found!")
            print(f"    -Solution length: {len(solution_path)} moves")
            print(f"    -Nodes explored: {solver.nodes_explored}")
            print(f"    -Max frontier size: {solver.max_frontier_size}")
            print(f"    -Time taken: {solver.solve_time:.4f} seconds")

            print(f"\n Complete solution path:")
            print(f"   {' → '.join(solution_path)}")

            print(f"\n Controls:")
            print(
                f"   SPACE: Execute next move ({current_step + 1}/{len(solution_path)})"
            )
            print(f"   S: Toggle auto-play (currently {'ON' if auto_play else 'OFF'})")
            print(f"   H: Switch heuristic (current: {heuristic_type.title()})")
            print(f"   Current step: {current_step + 1}/{len(solution_path)}")

        else:
            print(" No solution found!")
            solution_path = []

    except Exception as e:
        print(f" A* Search Error: {e}")
        solution_path = []

    solving = False


def executeNextMove(puzzle):
    """Execute the next move in the solution"""
    global current_step, auto_play

    if not solution_path:
        print("No solution loaded!")
        return

    if current_step >= len(solution_path):
        print("Solution complete!")
        return

    move_str = solution_path[current_step]

    print(f"\n Executing move {current_step + 1}/{len(solution_path)}: {move_str}")

    # Map string moves to puzzle moves
    move_map = {
        "UP": model.Puzzle.UP,
        "DOWN": model.Puzzle.DOWN,
        "LEFT": model.Puzzle.LEFT,
        "RIGHT": model.Puzzle.RIGHT,
    }

    if move_str in move_map:
        success = puzzle.move(move_map[move_str])
        if success:
            current_step += 1

            if current_step < len(solution_path):
                print(
                    f"Next move: {solution_path[current_step]} (Press SPACE or wait for auto-play)"
                )
            else:
                print(" All moves executed! Solution complete!")
                auto_play = False
                # Check if puzzle is solved and show appropriate message
                printPuzzleState(puzzle)
        else:
            print(f" Failed to execute move: {move_str}")
    else:
        print(f" Unknown move: {move_str}")


def resetSolution():
    """Reset solution state"""
    global solution_path, current_step, solving, auto_play

    solution_path = []
    current_step = 0
    solving = False
    auto_play = False


if __name__ == "__main__":
    gameLoop()

    def draw_puzzle(surface, puzzle_obj, offset_x=50, offset_y=150):
        """Draw the puzzle board"""
        for i in range(puzzle_obj.boardSize):
            for j in range(puzzle_obj.boardSize):
                x = offset_x + j * TILE_SIZE
                y = offset_y + i * TILE_SIZE

                # Draw tile background
                if puzzle_obj.board[i][j] == 0:  # Empty tile
                    color = GRAY
                else:
                    color = PURPLE  # Different color for A*

                pygame.draw.rect(surface, color, (x, y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(surface, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 2)

                # Draw tile number
                if puzzle_obj.board[i][j] != 0:
                    text = font.render(str(puzzle_obj.board[i][j]), True, WHITE)
                    text_rect = text.get_rect(
                        center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2)
                    )
                    surface.blit(text, text_rect)

    def draw_info(surface):
        """Draw game information"""
        info_lines = [
            "8-Puzzle - A* Search",
            "",
            "Controls:",
            "A - Solve with A* Search",
            "M - Switch to Manhattan heuristic",
            "T - Switch to Misplaced Tiles heuristic",
            "R - Reset puzzle",
            "N - New puzzle",
            "",
            f"Current Heuristic: {heuristic_type.title()}",
            "",
        ]

        if solver:
            info_lines.extend(
                [
                    f"Solution found: {'Yes' if solved else 'No'}",
                    f"Solution steps: {len(solution_path)}",
                    f"Nodes explored: {solver.nodes_explored}",
                    f"Max frontier size: {solver.max_frontier_size}",
                    f"Time taken: {solver.solve_time:.3f}s",
                    "",
                    "A* uses f(n) = g(n) + h(n)",
                    "g(n) = cost from start",
                    "h(n) = heuristic estimate",
                    "",
                ]
            )

        if solved and solution_path:
            info_lines.extend(
                [
                    f"Current step: {current_step}/{len(solution_path)}",
                    "SPACE - Next step",
                    "BACKSPACE - Previous step",
                    "",
                ]
            )

        for i, line in enumerate(info_lines):
            color = BLACK
            if "Manhattan" in line and heuristic_type == "manhattan":
                color = ORANGE
            elif "Misplaced" in line and heuristic_type == "misplaced":
                color = ORANGE
            elif "f(n)" in line:
                color = PURPLE

            text = small_font.render(line, True, color)
            surface.blit(text, (400, 50 + i * 25))

    def apply_move(move):
        """Apply a move to the puzzle"""
        if move == "UP":
            puzzle.move_up()
        elif move == "DOWN":
            puzzle.move_down()
        elif move == "LEFT":
            puzzle.move_left()
        elif move == "RIGHT":
            puzzle.move_right()

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and not solving:
                    print(f"Starting A* Search with {heuristic_type} heuristic...")
                    solver = AStarSolver(puzzle, heuristic_type)
                    solving = True

                    if solver.solve():
                        print("Solution found!")
                        solved = True
                        solution_path = solver.solution_path[:]
                        current_step = 0
                        # Reset puzzle to initial state
                        puzzle.board = solver.initial_state.board
                        puzzle.blank_row, puzzle.blank_col = (
                            solver.initial_state.blank_pos
                        )
                    else:
                        print("No solution found!")
                        solved = False
                    solving = False

                elif event.key == pygame.K_m:
                    heuristic_type = "manhattan"
                    print("Switched to Manhattan distance heuristic")

                elif event.key == pygame.K_t:
                    heuristic_type = "misplaced"
                    print("Switched to Misplaced tiles heuristic")

                elif event.key == pygame.K_r and solved:
                    # Reset to initial state
                    puzzle.board = solver.initial_state.board
                    puzzle.blank_row, puzzle.blank_col = solver.initial_state.blank_pos
                    current_step = 0

                elif event.key == pygame.K_n:
                    # Create new puzzle
                    puzzle = Puzzle(3)
                    solver = None
                    solving = False
                    solved = False
                    solution_path = []
                    current_step = 0

                elif (
                    event.key == pygame.K_SPACE
                    and solved
                    and current_step < len(solution_path)
                ):
                    # Next step in solution
                    apply_move(solution_path[current_step])
                    current_step += 1

                elif event.key == pygame.K_BACKSPACE and solved and current_step > 0:
                    # Previous step in solution
                    current_step -= 1
                    # Reset to initial state and replay moves
                    puzzle.board = solver.initial_state.board
                    puzzle.blank_row, puzzle.blank_col = solver.initial_state.blank_pos
                    for i in range(current_step):
                        apply_move(solution_path[i])

        # Draw everything
        screen.fill(WHITE)
        draw_puzzle(screen, puzzle)
        draw_info(screen)

        # Show solving status
        if solving:
            text = font.render(f"Solving with A* ({heuristic_type})...", True, RED)
            screen.blit(text, (50, 50))
        elif solved:
            text = font.render("Optimal solution found!", True, GREEN)
            screen.blit(text, (50, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
