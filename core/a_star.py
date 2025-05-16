import heapq
import time
import gui.colors as colors
from core.cell import Cell


def heuristic(a, b):
    """Calculate the heuristic value (Manhattan Distance)"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def trace_path(maze, came_from, current, x_offset, y_offset):
    """Reconstruct the path from start to goal."""
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    # Reverse the path (from start to goal)
    path.reverse()

    # Animate the path
    for i, node in enumerate(path):
        maze.draw_cell(node, colors.FINAL_PATH_COLOR, x_offset, y_offset)
        maze.canvas.update()
        time.sleep(1.0 / maze.speed_scale.get())

    print(f"Path found with {len(path)} steps.")


def a_star_search(maze, x_offset, y_offset):
    """Implement the A* search algorithm with visualizations"""
    start = tuple(maze.start_pos)
    goal = tuple(maze.end_pos)

    # Lists for open and closed nodes
    open_set = []
    closed_set = set()

    # Dictionary to store g scores (cost from start to current node)
    g_score = {start: 0}

    # Dictionary to store f scores (estimated total cost from start to goal via current node)
    f_score = {start: heuristic(start, goal)}

    # Dictionary to store predecessors for path reconstruction
    came_from = {}

    # Push start node into open set with its f_score as priority
    heapq.heappush(open_set, (f_score[start], start))

    # For visualization
    maze.draw_cell(list(start), colors.START_COLOR, x_offset, y_offset)
    maze.draw_cell(list(goal), colors.END_COLOR, x_offset, y_offset)

    while open_set:
        # Get node with the lowest f_score from open set
        current_f, current = heapq.heappop(open_set)

        # If we've reached the goal, reconstruct and animate the path
        if current == goal:
            trace_path(maze, came_from, current, x_offset, y_offset)
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

        # Check neighbors
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            # Check if neighbor is valid
            if (
                0 <= neighbor[0] < maze.rows
                and 0 <= neighbor[1] < maze.cols
                and maze.maze[neighbor[0]][neighbor[1]] != 1
                and neighbor not in closed_set
            ):
                # Calculate tentative g score
                tentative_g_score = g_score[current] + 1

                # If neighbor is not in open set or has a better g score
                if neighbor not in [
                    node[1] for node in open_set
                ] or tentative_g_score < g_score.get(neighbor, float("inf")):
                    # Update came_from, g_score, and f_score
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                    # Add neighbor to open set
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

                    # Visualize neighbor as open
                    if neighbor != goal:  # Don't color the goal node
                        maze.draw_cell(neighbor, colors.OPEN_COLOR, x_offset, y_offset)
                        maze.canvas.update()
                        time.sleep(0.5 / maze.speed_scale.get())

        # Mark current node as closed
        if current != start and current != goal:  # Don't color start or goal
            maze.draw_cell(current, colors.CLOSED_COLOR, x_offset, y_offset)
            maze.canvas.update()

    # If we get here, there is no path
    print("No path found.")
    return False
