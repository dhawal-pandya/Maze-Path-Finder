import curses
# curses is built-in in Linux and MacOS, but for windows you'll need to 
# "pip3 install windows-curses" or "pip install windows-curses" 
import queue
import time

## Maze 1
# maze = [
#     ["#", "#", "#", "#", "#", "#", "#", "#", "#"],
#     ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
#     ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
#     ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
#     ["#", " ", "#", " ", "#", "#", "#", " ", "#"],
#     ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
#     ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
#     ["X", " ", "#", " ", " ", " ", " ", " ", "O"],
#     ["#", "#", "#", "#", "#", "#", "#", "#", "#"]
# ]

## Maze 2 (For a longer terminal)
# maze = [
#     ["#", "#", "#", "#", "#", "#", "#", "#", "#"],
#     ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
#     ["#", " ", "#", "#", "#", "#", "#", " ", "#"],
#     ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
#     ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
#     ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
#     ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
#     ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
#     ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
#     ["#", " ", "#", " ", "#", " ", " ", " ", "#"],
#     ["#", " ", "#", " ", "#", "#", "#", "#", "#"],
#     ["X", " ", "#", " ", " ", " ", " ", " ", "O"],
#     ["#", "#", "#", "#", "#", "#", "#", "#", "#"]
# ]

## Maze3 (For a big terminal)
maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#","#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", " ", "#","#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", " ","#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", "#", " ","#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", " ","#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", " ", " ", "#", " ", "#", " ", "#", " ", "#","#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#", "#", "#", " ", "#", " ", "#", " ", " ","#"],
    ["#", " ", "#", " ", " ", " ", " ", "#", " ", " ", " ", " ", "#", " ", "#", "#", "#","#"],
    ["#", " ", "#", " ", " ", "#", " ", "#", " ", "#", " ", " ", "#", " ", " ", " ", " ","#"],
    ["#", " ", "#", "#", "#", "#", " ", "#", " ", "#", " ", " ", "#", " ", " ", "#", " ","#"],
    ["#", " ", " ", " ", " ", "#", " ", "#", " ", "#", " ", " ", " ", " ", "#", " ", " ","#"],
    ["#", " ", "#", " ", " ", "#", "#", "#", " ", "#", " ", " ", "#", " ", " ", "#", " ","#"],
    ["#", " ", "#", " ", " ", " ", " ", " ", " ", "#", " ", " ", "#", " ", " ", "#", " ","#"],
    ["#", " ", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", " ","#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ","#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "X", "#", "#", "#", "#","#"]
]


def print_maze(maze, stdscr, path=[]):
    MAGENTA = curses.color_pair(1)
    CYAN = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*3, "X", CYAN)
            else:
                stdscr.addstr(i, j*3, value, MAGENTA)


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j

    return None


def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    visited = set()
    # also makes sure the path finder doesn't go round and round an unattached obstacle.

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.5) # it's in seconds
        stdscr.refresh()

        if maze[row][col] == end:
            return path

        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue # meaning: next for loop

            r, c = neighbor
            if maze[r][c] == "#":
                continue

            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor)


def find_neighbors(maze, row, col):
    neighbors = []

    if row > 0:  # UP
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):  # DOWN
        neighbors.append((row + 1, col))
    if col > 0:  # LEFT
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # RIGHT
        neighbors.append((row, col + 1))

    return neighbors


def main(stdscr):
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    find_path(maze, stdscr)
    stdscr.getch()


curses.wrapper(main)
# the Traceback error here is a bug in ncurses, you can find it in its documentation.
# https://docs.python.org/3/library/curses.html
# It is easily solved by increasing the size of the terminal to the appropritate size of the maze, a smaller than required terminal will err.