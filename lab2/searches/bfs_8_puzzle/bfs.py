import pygame
import sys
import time
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import model
from bfs_solver import BFSSolver

pygame.init()
BOARD_SIZE = 3

# Global variables for BFS solution
solution_path = []
current_step = 0
solving = False
auto_play = False
last_move_time = 0
original_puzzle_state = None


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
    global solution_path, current_step, solving, auto_play, last_move_time, original_puzzle_state

    clock = pygame.time.Clock()
    puzzle = model.Puzzle(boardSize=BOARD_SIZE)

    print("\n 8-Puzzle with BFS Solver")
    print("Controls:")
    print("  B: Run BFS search")
    print("  SPACE: Show next move in solution")
    print("  A: Auto play the moves")
    print("  R: Shuffle puzzle")
    print("  ESC: Quit")
    print("  Click: Manual move")
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
    global solution_path, current_step, solving, auto_play, original_puzzle_state

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
        elif event.key == pygame.K_b:
            # Run BFS search
            if puzzle.checkWin():
                print("Puzzle is already solved! Press 'R' to shuffle and try again.")
            else:
                runBFS(puzzle)
        elif event.key == pygame.K_SPACE:
            # Show next move
            if solution_path and current_step < len(solution_path):
                executeNextMove(puzzle)
            else:
                print("No solution loaded or solution complete!")
        elif event.key == pygame.K_a:
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
                print("No solution loaded! Press 'B' to run BFS first.")
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
        print("  B: Run BFS search")
        print("  SPACE: Show next move in solution")
        print("  A: Auto play the moves")
        print("  R: Shuffle puzzle")
        print("  ESC: Quit")
        print("  Click: Manual move")
        print("=" * 50)


def runBFS(puzzle):
    """Run BFS algorithm and store solution"""
    global solution_path, current_step, solving, original_puzzle_state, auto_play

    print("\n" + "=" * 50)
    print("Running BFS (Breadth-First Search)...")
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
        solver = BFSSolver(puzzle)

        # Check solvability
        if not solver.is_solvable():
            print(" Puzzle is not solvable!")
            solving = False
            return

        print(" Puzzle is solvable! Searching for solution...")

        # Solve with BFS
        start_time = time.time()
        success = solver.solve()

        if success:
            solution_path = solver.solution_path
            current_step = 0

            print(f"\n BFS ANALYSIS:")
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
            print(f"   A: Toggle auto-play (currently {'ON' if auto_play else 'OFF'})")
            print(f"   Current step: {current_step + 1}/{len(solution_path)}")

        else:
            print(" No solution found!")
            solution_path = []

    except Exception as e:
        print(f" BFS Error: {e}")
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
