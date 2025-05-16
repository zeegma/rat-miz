import heapq
import time
import gui.colors as colors
from core.cell import Cell


def heuristic(a, b):
    """Calculate the heuristic value (Manhattan Distance)"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def trace_path(maze, cell_details, current, x_offset, y_offset):
    """Reconstruct the path from start to goal."""
    path = [current]
    row, col = current

    # Trace back from goal to start using parent references
    while not (
        cell_details[row][col].parent_x == row
        and cell_details[row][col].parent_y == col
    ):
        temp_row = cell_details[row][col].parent_x
        temp_col = cell_details[row][col].parent_y
        row, col = temp_row, temp_col
        path.append((row, col))

    # Reverse the path (from start to goal)
    path.reverse()

    # Animate the path
    for i, cell in enumerate(path):
        maze.check_pause()

        if i > 0 and i < len(path) - 1:
            row, col = cell
            f_score = cell_details[row][col].f
            maze.draw_cell(cell, colors.FINAL_PATH_COLOR, x_offset, y_offset, f_score)
            maze.canvas.update()
            time.sleep(1.0 / maze.speed_scale.get())

    print(f"Path found with {len(path)} steps.")


def a_star_search(maze, x_offset, y_offset):
    """Implement the A* search algorithm with visualizations"""
    start = tuple(maze.start_pos)
    goal = tuple(maze.end_pos)

    # Initialize Cell details for each position in the grid
    cell_details = [[Cell() for _ in range(maze.cols)] for _ in range(maze.rows)]

    # Initialize the start cell
    start_row, start_col = start
    cell_details[start_row][start_col].f = 0
    cell_details[start_row][start_col].g = 0
    cell_details[start_row][start_col].h = heuristic(start, goal)
    cell_details[start_row][start_col].parent_x = start_row
    cell_details[start_row][start_col].parent_y = start_col

    # Lists for open and closed nodes
    open_set = []
    closed_set = set()

    # Push start node into open set with its f_score as priority
    heapq.heappush(open_set, (0, start))  # (f_score, position)

    # For visualization
    maze.draw_cell(list(start), colors.START_COLOR, x_offset, y_offset, "S")
    maze.draw_cell(list(goal), colors.END_COLOR, x_offset, y_offset, "G")

    # Main loop of A* search algorithm
    while open_set:
        # Check if paused
        maze.check_pause()

        # Get node with the lowest f_score from open set
        _, current = heapq.heappop(open_set)
        current_row, current_col = current

        # If goal is reached, reconstruct and animate the path
        if current == goal:
            trace_path(maze, cell_details, current, x_offset, y_offset)
            return True

        # Add current node to closed set
        closed_set.add(current)

        # Visualize current node
        if current != start:
            maze.draw_cell(current, colors.CURRENT_COLOR, x_offset, y_offset)
            maze.canvas.update()
            time.sleep(1.0 / maze.speed_scale.get())

        # Define possible directions (up, right, down, left)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # For each direction, check the successors (both x and y)
        for direction in directions:
            # Check if paused before processing each neighbor
            maze.check_pause()

            neighbor_row = current_row + direction[0]
            neighbor_col = current_col + direction[1]
            neighbor = (neighbor_row, neighbor_col)

            # Check if neighbor is valid
            if (
                0 <= neighbor_row < maze.rows
                and 0 <= neighbor_col < maze.cols
                and maze.maze[neighbor_row][neighbor_col] != 1
                and neighbor not in closed_set
            ):
                # Calculate tentative g score
                tentative_g_score = cell_details[current_row][current_col].g + 1

                # If neighbor is not in open set or has a better g score
                if (
                    cell_details[neighbor_row][neighbor_col].f == float("inf")
                    or tentative_g_score < cell_details[neighbor_row][neighbor_col].g
                ):
                    # Update cell details
                    cell_details[neighbor_row][neighbor_col].parent_x = current_row
                    cell_details[neighbor_row][neighbor_col].parent_y = current_col
                    cell_details[neighbor_row][neighbor_col].g = tentative_g_score
                    cell_details[neighbor_row][neighbor_col].h = heuristic(
                        neighbor, goal
                    )
                    cell_details[neighbor_row][neighbor_col].f = (
                        cell_details[neighbor_row][neighbor_col].g
                        + cell_details[neighbor_row][neighbor_col].h
                    )

                    # Add neighbor to open set
                    heapq.heappush(
                        open_set, (cell_details[neighbor_row][neighbor_col].f, neighbor)
                    )

                    # Visualize neighbor as open
                    if neighbor != goal:
                        # Check if paused before visualizing
                        maze.check_pause()

                        # Then visualize if not paused
                        maze.draw_cell(neighbor, colors.OPEN_COLOR, x_offset, y_offset)
                        maze.canvas.update()
                        time.sleep(0.5 / maze.speed_scale.get())

        # Mark current node as closed except start or goal
        if current != start and current != goal:
            current_f_score = cell_details[current_row][current_col].f
            maze.draw_cell(
                current, colors.CLOSED_COLOR, x_offset, y_offset, current_f_score
            )
            maze.canvas.update()

    # If we get here, there is no path
    return False
