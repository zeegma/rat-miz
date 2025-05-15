import heapq

from core.node import Node
from core.parser import parser

# Define the size of the grid
ROW = 47
COL = 57

# Check if a Node is valid (within the grid)
def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)


# Check if a Node is unblocked
def is_unblocked(grid, row, col):
    return grid[row][col] == 0


# Check if a Node is the finishination
def is_finished(row, col, finish):
    return row == finish[0] and col == finish[1]


# Calculate the heuristic value of a Node (Manhattan Distance)
def calculate_h_value(row, col, finish):
    return abs(row - finish[0]) + abs(col - finish[1])


# Trace the path from source to finishination
def trace_path(Node_details, finish):

    path = []
    row = finish[0]
    col = finish[1]

    # Trace the path from finishination to source using parent Nodes
    # It will only terminate when we get to the starting node as it is it's own parent (will equal to)
    while not (Node_details[row][col].parent_x == row and Node_details[row][col].parent_y == col):
        path.append([row, col])
        temp_row = Node_details[row][col].parent_x
        temp_col = Node_details[row][col].parent_y
        row = temp_row
        col = temp_col

    # Add the source Node to the path
    path.append([row, col])

    # Reverse the path to get the path from source to finishination
    path.reverse()

    return path


# Implement the A* search algorithm
def a_star_search(grid, start, finish):

    # Check if the starting and finish coordinates are valid
    if not is_valid(start[0], start[1]) or not is_valid(finish[0], finish[1]):
        print("Starting/Finish coordinates are invalid")
        return

    # Check if the starting and finish coordinates are unblocked
    if not is_unblocked(grid, start[0], start[1]) or not is_unblocked(grid, finish[0], finish[1]):
        print("Starting/Finish coordinates are blocked")
        return

    # Check if we are already at the finish
    if is_finished(start[0], start[1], finish):
        print("We are already at the finish node")
        return

    # Initialize the visited nodes list
    visited_list = [[False for _ in range(COL)] for _ in range(ROW)]

    # Initialize the details of each Node
    Node_details = [[Node() for _ in range(COL)] for _ in range(ROW)]

    # Initialize the sequence of all the explored noted
    explored_nodes = []

    # Initialize the start Node details
    i = start[0]
    j = start[1]
    Node_details[i][j].f = 0
    Node_details[i][j].g = 0
    Node_details[i][j].h = 0
    Node_details[i][j].parent_x = i
    Node_details[i][j].parent_y = j

    # Initialize the open list (Nodes to be visited) with the start Node
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Initialize the flag for whether the finish line is found
    found_finish = False

    # Main loop of A* search algorithm
    while len(open_list) > 0:
        # Pop the Node with the smallest f value from the open list
        p = heapq.heappop(open_list)

        explored_nodes.append((p[1], p[2]))

        # Mark the Node as visited
        i = p[1]
        j = p[2]
        visited_list[i][j] = True

        # For each direction, check the successors (both x and y)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            # If the successor is valid, unblocked, and not visited
            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not visited_list[new_i][new_j]:

                # If the successor is the end/finish line
                if is_finished(new_i, new_j, finish):

                    # Set the parent of the finishination Node
                    Node_details[new_i][new_j].parent_x = i
                    Node_details[new_i][new_j].parent_y = j

                    explored_nodes.append((new_i, new_j))
                    print("\nThe maze has been solved!")

                    # Trace and print the path from source to finishination
                    goal_path = trace_path(Node_details, finish)
                    found_finish = True
                    return explored_nodes, goal_path

                else:
                    # Calculate the new f, g, and h values
                    g_new = Node_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, finish)
                    f_new = g_new + h_new

                    # If the Node is not in the open list or the new f value is smaller
                    if Node_details[new_i][new_j].f == float('inf') or Node_details[new_i][new_j].f > f_new:

                        # Add the Node to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))

                        # Update the Node details
                        Node_details[new_i][new_j].f = f_new
                        Node_details[new_i][new_j].g = g_new
                        Node_details[new_i][new_j].h = h_new
                        Node_details[new_i][new_j].parent_x = i
                        Node_details[new_i][new_j].parent_y = j

    # If the finish node is not found after visiting all nodes
    if not found_finish:
        print("Failed to find the end of the maze.")


def main():
    # Define values to use for the algorithm
    grid, start, finish = parser()

    print(start, finish)
    # Run the A* search algorithm
    a_star_search(grid, start, finish)


if __name__ == "__main__":
    main()