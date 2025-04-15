# Step 1: Read puzzle and construct 9x9 grid and domain matrix
# Step 2: Apply initial constraint propagation by removing known values
#         from peers (row, column, block)
# Step 3: Use MRV (Minimum Remaining Values) to select next cell with fewest options
# Step 4: Use recursive backtracking with forward checking:
#         - Try each value in domain
#         - Apply forward check: remove value from peers’ domains
#         - If failure, undo changes (backtrack)
# Step 5: If grid is fully assigned (no sets left), solution is found
# ALSO IVE ADDED TIME FUNCTONALITY TO CHECK TIME CONSUMED
# IMPORTED ORTOOLS FOR FUNCTIONS

import time
from ortools.sat.python import cp_model

def read_puzzle_file(path="puzzle.txt"):
    puzzle_data = ""
    with open(path, "r") as file:
        for line in file:
            puzzle_data += line.strip().replace("|", "")
    return puzzle_data

puzzle_string = read_puzzle_file()

### --- MY SOLUTION ---
import copy

def prepare_your_solver_data(puzzle_string):
    grid = [[0 for _ in range(9)] for _ in range(9)]
    domain_grid = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]

    index = 0
    for row in range(9):
        for col in range(9):
            grid[row][col] = int(puzzle_string[index])
            if grid[row][col] != 0:
                domain_grid[row][col] = 0
            index += 1

    return grid, domain_grid

def pick_next_variable(domains):
    smallest = 9
    chosen = None
    for i in range(9):
        for j in range(9):
            if isinstance(domains[i][j], set) and 0 < len(domains[i][j]) < smallest:
                smallest = len(domains[i][j])
                chosen = (i, j)
    return chosen

def is_filled(domains):
    for row in domains:
        for entry in row:
            if isinstance(entry, set):
                return False
    return True

def apply_forward_check(board, domains, row, col, number):
    affected = []
    saved_domain = domains[row][col]

    board[row][col] = number
    domains[row][col] = 0

    for i in range(9):
        if isinstance(domains[row][i], set) and number in domains[row][i]:
            domains[row][i].remove(number)
            affected.append((row, i, number))
        if isinstance(domains[i][col], set) and number in domains[i][col]:
            domains[i][col].remove(number)
            affected.append((i, col, number))

    start_r = (row // 3) * 3
    start_c = (col // 3) * 3
    for r in range(start_r, start_r + 3):
        for c in range(start_c, start_c + 3):
            if isinstance(domains[r][c], set) and number in domains[r][c]:
                domains[r][c].remove(number)
                affected.append((r, c, number))

    return affected, saved_domain

def revert_changes(board, domains, changes, row, col, old_domain):
    board[row][col] = 0
    domains[row][col] = old_domain
    for r, c, val in changes:
        if isinstance(domains[r][c], set):
            domains[r][c].add(val)

def solve_your(grid, domains):
    if is_filled(domains):
        return True

    next_var = pick_next_variable(domains)
    if not next_var:
        return False

    r, c = next_var
    options = domains[r][c]

    for val in sorted(options):
        changes, old_dom = apply_forward_check(grid, domains, r, c, val)
        conflict = any(isinstance(domains[i][j], set) and len(domains[i][j]) == 0
                       for i in range(9) for j in range(9))

        if not conflict and solve_your(grid, domains):
            return True

        revert_changes(grid, domains, changes, r, c, old_dom)

    return False


### --- OR-Tools Solver ---
def run_ortools_solver(puzzle_string):
    model = cp_model.CpModel()
    cell = {(i, j): model.NewIntVar(1, 9, f'cell_{i}_{j}') for i in range(9) for j in range(9)}

    for i in range(9):
        model.AddAllDifferent([cell[(i, j)] for j in range(9)])
        model.AddAllDifferent([cell[(j, i)] for j in range(9)])
    for bi in range(3):
        for bj in range(3):
            block = [cell[(bi * 3 + i, bj * 3 + j)] for i in range(3) for j in range(3)]
            model.AddAllDifferent(block)
    for i in range(9):
        for j in range(9):
            val = int(puzzle_string[i * 9 + j])
            if val != 0:
                model.Add(cell[(i, j)] == val)

    solver = cp_model.CpSolver()
    start_time = time.time()
    status = solver.Solve(model)
    end_time = time.time()

    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        print("✅ OR-Tools Solver: Solved")
    else:
        print("❌ OR-Tools Solver: No Solution")
    print(f"⏱️ OR-Tools Time: {end_time - start_time:.5f} seconds\n")


### --- Classic Backtracking Solver ---
def run_classic_backtracking_solver(puzzle_string):
    M = 9
    grid = [[0 for _ in range(9)] for _ in range(9)]
    idx = 0
    for i in range(9):
        for j in range(9):
            grid[i][j] = int(puzzle_string[idx])
            idx += 1

    def is_valid(grid, row, col, num):
        for x in range(9):
            if grid[row][x] == num or grid[x][col] == num:
                return False
        startRow = row - row % 3
        startCol = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + startRow][j + startCol] == num:
                    return False
        return True

    def backtrack(grid, row, col):
        if row == M - 1 and col == M:
            return True
        if col == M:
            row += 1
            col = 0
        if grid[row][col] > 0:
            return backtrack(grid, row, col + 1)
        for num in range(1, M + 1):
            if is_valid(grid, row, col, num):
                grid[row][col] = num
                if backtrack(grid, row, col + 1):
                    return True
                grid[row][col] = 0
        return False

    start_time = time.time()
    result = backtrack(grid, 0, 0)
    end_time = time.time()

    if result:
        print("✅ Classic Backtracking Solver: Solved")
    else:
        print("❌ Classic Backtracking Solver: No Solution")
    print(f"⏱️ Classic Solver Time: {end_time - start_time:.5f} seconds\n")


### running all of the solutions
print("▶️ Running Your Solved example:")
grid, domain_grid = prepare_your_solver_data(puzzle_string)
start_time = time.time()
if solve_your(grid, domain_grid):
    print("✅ Your Solver: Solved")
else:
    print("❌ Your Solver: No Solution")
end_time = time.time()
print(f"⏱️ Your Solver Time: {end_time - start_time:.5f} seconds\n")

print("▶️ Running OR-Tools Solver:")
run_ortools_solver(puzzle_string)

print("▶️ Running Classic Backtracking Solver:")
run_classic_backtracking_solver(puzzle_string)
