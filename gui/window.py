import tkinter as tk
from tkinter import messagebox
from core.parser import parser
from core.astar import a_star_search
import gui.colors as colors
import math

class Maze:
    def __init__(self, root):
        self.root = root
        self.root.title("Rat Maze")
        self.root.configure(bg=colors.BACKGROUND_COLOR_LEFT)
        self.root.attributes("-fullscreen", True)
        self.root.eval("tk::PlaceWindow . center")
        self.root.bind("<Escape>", self.end_fullscreen)
        self.track_nodes = []

        # Sidebar frame (buttons container)
        self.sidebar = tk.Frame(
            root, bg=colors.BACKGROUND_COLOR_LEFT, width=250, padx=10, pady=10
        )
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Title label
        self.title_label = tk.Label(
            self.sidebar,
            text="Rat Maze",
            font=("Arial", 18, "bold"),
            fg=colors.DEFAULT_WHITE,
            bg=colors.BACKGROUND_COLOR_LEFT,
        )
        self.title_label.pack(pady=(0, 20))

        # Solve Button
        self.solve_button = tk.Button(
            self.sidebar,
            text="Solve with A*",
            bg=colors.BUTTON_COLOR,
            fg=colors.DEFAULT_WHITE,
            font=("Arial", 12),
            relief="flat",
            activebackground=colors.BUTTON_ACTIVE,
            activeforeground=colors.DEFAULT_WHITE,
            command=self.on_solve_clicked
        )
        self.solve_button.pack(fill=tk.X, pady=5)

        # Speed label
        self.speed_label = tk.Label(
            self.sidebar,
            text="Speed:",
            fg=colors.DEFAULT_WHITE,
            bg=colors.BACKGROUND_COLOR_LEFT,
            font=("Arial", 10),
        )
        self.speed_label.pack(pady=(20, 5))

        # Speed scale
        self.speed_scale = tk.Scale(
            self.sidebar,
            from_=1,
            to=100,
            orient=tk.HORIZONTAL,
            bg=colors.BACKGROUND_COLOR_RIGHT,
            fg=colors.DEFAULT_WHITE,
            highlightbackground=colors.BACKGROUND_COLOR_LEFT,
            troughcolor=colors.THROUGH_COLOR,
        )
        self.speed_scale.set(50)
        self.speed_scale.pack(fill=tk.X)

        # Canvas frame (maze container)
        self.canvas_frame = tk.Frame(root, bg=colors.BACKGROUND_COLOR_RIGHT)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg=colors.BACKGROUND_COLOR_RIGHT)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Maze variables
        self.maze = None
        self.rows = 0
        self.cols = 0
        self.start_pos = None
        self.end_pos = None
        self.cell_size = 15

        # Load maze after the window loads fully
        self.root.after(50, self.load_maze)

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", False)

        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Get the window width and height
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Calculate the position to center the window
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the window to the center
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        return "break"
    
    def offset_computation(self):
        # Calculate top padding to visually center maze
        canvas_height = self.canvas.winfo_height()
        canvas_width = self.canvas.winfo_width()

        maze_height = self.rows * self.cell_size
        maze_width = self.cols * self.cell_size

        x_offset = max((canvas_width - maze_width) // 2, 0)
        y_offset = max((canvas_height - maze_height) // 2, 0)

        return x_offset, y_offset
    
    def distance_formula(self, x1, y1, x2, y2):
        return math.sqrt((pow(x2-x1, 2))+pow(y2-y1, 2))
        
    def load_maze(self):
        try:
            # Get the maze, the starting, and end position from parser
            self.maze, self.start_pos, self.end_pos = parser()

            # Get rows and columns of maze
            self.rows = len(self.maze)
            self.cols = len(self.maze[0]) if self.rows > 0 else 0

            if not self.start_pos or not self.end_pos:
                raise ValueError("Start ('S') or End ('F') not found.")

            # Draw the maze after getting necessary values
            self.draw_maze()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading maze: {e}")

    def draw_maze(self):
        # Clear canvas first (if there is)
        self.canvas.delete("all")

        # Then pass these offsets each time a cell is created to visually center it
        x_offset, y_offset = self.offset_computation()

        # Loop through the cells to draw them
        for row in range(self.rows):
            for col in range(self.cols):
                if self.maze[row][col] == 1:
                    # If its 1 then its a wall so color it with wall color
                    self.draw_cell([row, col], colors.WALL_COLOR, x_offset, y_offset)
                else:
                    # Else color it as path
                    self.draw_cell([row, col], colors.PATH_COLOR, x_offset, y_offset)

        # Color starting position differently
        if self.start_pos:
            self.draw_cell(self.start_pos, colors.START_COLOR, x_offset, y_offset)

        # And ending position as well
        if self.end_pos:
            self.draw_cell(self.end_pos, colors.END_COLOR, x_offset, y_offset)

        # Update canvas to reflect maze
        self.canvas.update

    def draw_cell(self, position, color, x_offset=0, y_offset=0):
        # Convert maze cell coordinates to canvas pixel coordinates
        # (x1, y1) is the top left corner, (x2, y2) is the bottom right corner
        row, col = position
        x1 = col * self.cell_size + x_offset
        y1 = row * self.cell_size + y_offset
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        # Create a rectangle (cell) on the maze
        self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=color, outline=colors.OUTLINE_COLOR
        )

    # When the solve button is clicked, run the algorithm
    def on_solve_clicked(self):
        explored_nodes, goal_path = a_star_search(self.maze, self.start_pos, self.end_pos)

        # Compute for the offsets again
        x_offset, y_offset = self.offset_computation()

        # Call an animate nodes method to print out slowly the explored paths and the goal path
        self.animate_nodes(explored_nodes, goal_path, 0, x_offset, y_offset)
    

    def animate_nodes(self, explored_nodes, goal_path, index, x_offset, y_offset):
        # Compute for the speed to traverse results
        speed = 300 // self.speed_scale.get()

        # Explore all explored nodes
        if index < len(explored_nodes):
            curr_node = explored_nodes[index]

            # If we are already on the second node of all solutions, we can start changing the last cell's color
            if index > 0:
                prev_node = explored_nodes[index - 1]
                self.draw_cell(prev_node, colors.DEAD_END_COLOR, x_offset, y_offset)
            
                # Check if we teleported to another place, then mark the last exploration with a trailing color
                if self.distance_formula(curr_node[0], curr_node[1], prev_node[0], prev_node[1]) > 1:
                    self.draw_cell(prev_node, colors.TRAIL_COLOR, x_offset, y_offset)
                    self.track_nodes.append(prev_node)

            # Check if we reconnected to a tracked dead end
            for node in self.track_nodes[:]:  # Copy to avoid list mutation issues
                if self.distance_formula(curr_node[0], curr_node[1], node[0], node[1]) == 1:
                    self.track_nodes.remove(node)
                    self.draw_cell(node, colors.DEAD_END_COLOR, x_offset, y_offset)

            # Color out the cell with yellow as the lead color
            self.draw_cell(explored_nodes[index], colors.END_COLOR, x_offset, y_offset)

            # Do delay animation with speed
            self.canvas.after(speed, self.animate_nodes, explored_nodes, goal_path, index + 1, x_offset, y_offset)

        # Explore the goal path and display it
        elif index < len(explored_nodes) + len(goal_path):
            # Reset path index
            path_index = index - len(explored_nodes)

            # Color it out as the yellow road 
            self.draw_cell(goal_path[path_index], colors.END_COLOR, x_offset, y_offset)
            self.canvas.after(speed, self.animate_nodes, explored_nodes, goal_path, index + 1, x_offset, y_offset)
