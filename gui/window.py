import tkinter as tk
from tkinter import messagebox, colorchooser
from core.parser import parser
from core.a_star import a_star_search
import gui.colors as colors
from utils.helpers import compute_offset
import time
import pygame


class Maze:
    def __init__(self, root):
        self.root = root
        self.root.title("Rat Maze")
        self.root.configure(bg=colors.BACKGROUND_COLOR_LEFT)
        self.root.attributes("-fullscreen", True)
        self.root.eval("tk::PlaceWindow . center")
        self.root.bind("<Escape>", self.end_fullscreen)

        # Sidebar frame (buttons container)
        self.sidebar = tk.Frame(
            root, bg=colors.BACKGROUND_COLOR_LEFT, width=430, padx=10, pady=10
        )
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Title label
        self.title_label = tk.Label(
            self.sidebar,
            text="Rat Maze with A*",
            font=("Arial", 18, "bold"),
            fg=colors.DEFAULT_WHITE,
            bg=colors.BACKGROUND_COLOR_LEFT,
        )
        self.title_label.pack(pady=(0, 20))

        # Control buttons frame
        self.control_frame = tk.Frame(self.sidebar, bg=colors.BACKGROUND_COLOR_LEFT)
        self.control_frame.pack(fill=tk.X, pady=(0, 20))

        # Solve button
        self.solve_button = tk.Button(
            self.control_frame,
            text="Solve",
            bg=colors.BUTTON_COLOR,
            fg=colors.DEFAULT_WHITE,
            font=("Arial", 12),
            relief="flat",
            activebackground=colors.BUTTON_ACTIVE,
            activeforeground=colors.DEFAULT_BLACK,
            command=self.on_solve_click,
        )
        self.solve_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Pause button
        self.pause_button = tk.Button(
            self.control_frame,
            text="Pause",
            bg=colors.BUTTON_COLOR_PAUSE,
            fg=colors.DEFAULT_WHITE,
            font=("Arial", 12),
            relief="flat",
            activebackground=colors.BUTTON_ACTIVE_PAUSE,
            activeforeground=colors.DEFAULT_BLACK,
            command=self.on_pause_click,
        )
        self.pause_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Speed control frame
        self.speed_frame = tk.Frame(self.sidebar, bg=colors.BACKGROUND_COLOR_LEFT)
        self.speed_frame.pack(fill=tk.X, pady=(0, 20))

        # Speed label
        self.speed_label = tk.Label(
            self.speed_frame,
            text="Speed",
            fg=colors.DEFAULT_WHITE,
            bg=colors.BACKGROUND_COLOR_LEFT,
            font=("Arial", 12),
        )
        self.speed_label.pack(anchor=tk.CENTER)

        # Speed scale
        self.speed_scale = tk.Scale(
            self.speed_frame,
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

        # Color customization frame
        self.color_frame = tk.Frame(self.sidebar, bg=colors.BACKGROUND_COLOR_LEFT)
        self.color_frame.pack(fill=tk.X, pady=(0, 20))

        # Wall color button
        self.wall_color_btn = tk.Button(
            self.color_frame,
            text="Wall Color",
            bg="#5f5c5e",
            fg=colors.DEFAULT_WHITE,
            font=("Arial", 10),
            relief="flat",
            command=self.choose_wall_color,
        )
        self.wall_color_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Path color button
        self.path_color_btn = tk.Button(
            self.color_frame,
            text="Path Color",
            bg="#5f5c5e",
            fg=colors.DEFAULT_WHITE,
            font=("Arial", 10),
            relief="flat",
            command=self.choose_path_color,
        )
        self.path_color_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Decision panel label
        self.decision_label = tk.Label(
            self.sidebar,
            text="A* Decision Log",
            fg=colors.DEFAULT_WHITE,
            bg=colors.BACKGROUND_COLOR_LEFT,
            font=("Arial", 12),
        )
        self.decision_label.pack(pady=(5, 5))

        # Create a frame for the decision panel
        self.decision_frame = tk.Frame(
            self.sidebar, bg=colors.BACKGROUND_COLOR_RIGHT, bd=1, relief=tk.SUNKEN
        )
        self.decision_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 10))

        # Add scrollbar to the frame
        self.decision_scrollbar = tk.Scrollbar(self.decision_frame)
        self.decision_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create text widget for decisions
        self.decision_text = tk.Text(
            self.decision_frame,
            bg=colors.BACKGROUND_COLOR_RIGHT,
            fg=colors.DEFAULT_WHITE,
            width=28,
            height=10,
            yscrollcommand=self.decision_scrollbar.set,
            font=("Courier", 10),
            wrap=tk.WORD,
        )
        self.decision_text.pack(fill=tk.BOTH, expand=True)
        self.decision_scrollbar.config(command=self.decision_text.yview)

        # Configure text tags for for logging
        self.decision_text.tag_configure(
            "open", background=colors.OPEN_COLOR, foreground=colors.DEFAULT_BLACK
        )
        self.decision_text.tag_configure(
            "closed", background=colors.CLOSED_COLOR, foreground=colors.DEFAULT_BLACK
        )
        self.decision_text.tag_configure(
            "path", background=colors.FINAL_PATH_COLOR, foreground=colors.DEFAULT_BLACK
        )
        self.decision_text.tag_configure(
            "current", background=colors.CURRENT_COLOR, foreground=colors.DEFAULT_BLACK
        )

        # Make the text widget read only
        self.decision_text.config(state=tk.DISABLED)

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
        self.paused = False
        self.solving_in_progress = False

        # For the sound
        pygame.mixer.init()

        self.sound = pygame.mixer.Sound("audio/tukso.mp3")

        # Load maze after the window loads fully
        self.root.after(50, self.load_maze)

        # Custom color variables
        self.wall_color = colors.WALL_COLOR  
        self.path_color = colors.PATH_COLOR 
        
    def choose_wall_color(self):
        """Open color picker for wall color"""
        color = colorchooser.askcolor(title="Choose Wall Color")[1]
        if color:
            self.wall_color = color
            if hasattr(self, 'maze'):
                self.draw_maze()

    def choose_path_color(self):
        """Open color picker for path color"""
        color = colorchooser.askcolor(title="Choose Path Color")[1]
        if color:
            self.path_color = color
            if hasattr(self, 'maze'):
                self.draw_maze()

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
        x_offset, y_offset = compute_offset(self)

        # Loop through the cells to draw them
        for row in range(self.rows):
            for col in range(self.cols):
                if self.maze[row][col] == 1:
                    # If its 1 then its a wall so color it with wall color
                    self.draw_cell([row, col], self.wall_color, x_offset, y_offset)
                else:
                    # Else color it as path
                    self.draw_cell([row, col], self.path_color, x_offset, y_offset)

        # Color starting position differently
        if self.start_pos:
            self.draw_cell(self.start_pos, colors.START_COLOR, x_offset, y_offset, "S")

        # And ending position as well
        if self.end_pos:
            self.draw_cell(self.end_pos, colors.END_COLOR, x_offset, y_offset, "G")

        # Update canvas to reflect maze
        self.canvas.update

    def draw_cell(self, position, color, x_offset=0, y_offset=0, value=None):
        # Convert maze cell coordinates to canvas pixel coordinates
        row, col = position
        x1 = col * self.cell_size + x_offset
        y1 = row * self.cell_size + y_offset
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        # Create a rectangle (cell) on the maze
        self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=color, outline=colors.OUTLINE_COLOR
        )

        # Optionally draw value on cell
        if value is not None:
            self.canvas.create_text(
                (x1 + x2) // 2,
                (y1 + y2) // 2,
                text=str(value),
                fill=colors.DEFAULT_BLACK,
                font=("Arial", int(self.cell_size / 3)),
            )

    def on_solve_click(self):
        # Start the sound
        self.sound_channel = self.sound.play(-1)

        # Reset the maze display before solving
        self.draw_maze()

        # Set solving flag and reset pause state
        self.solving_in_progress = True
        self.paused = False
        self.pause_button.config(text="Pause", bg=colors.BUTTON_COLOR_PAUSE)
        self.solve_button.config(
            state="disabled",
            bg=colors.BUTTON_COLOR_DISABLED,
            text="Solving",
        )

        # Reset the decision log
        self.reset_decision_log()

        # Calculate offsets for cell placement
        x_offset, y_offset = compute_offset(self)

        # Run the A* algorithm
        path_found = a_star_search(self, x_offset, y_offset)

        # Reset solving flag when done
        self.solving_in_progress = False
        self.solve_button.config(state="normal", bg=colors.BUTTON_COLOR, text="Solve")
        pygame.mixer.stop()

        if path_found:
            print("The maze has been solved successfully!")
        else:
            print("Failed to find a path through the maze.")

    def on_pause_click(self):
        if self.solving_in_progress:
            self.paused = not self.paused
            if self.paused:
                self.pause_button.config(text="Resume", bg=colors.BUTTON_COLOR)
                pygame.mixer.pause()
            else:
                self.pause_button.config(text="Pause", bg=colors.BUTTON_COLOR_PAUSE)
                pygame.mixer.unpause()

    def check_pause(self):
        if self.paused:
            # Wait until unpaused
            while self.paused:
                self.root.update()
                time.sleep(0.1)

    def log_decision(self, cell_pos, g_score, h_score, f_score, status):
        row, col = cell_pos

        # Enable editing
        self.decision_text.config(state=tk.NORMAL)

        # Format decision entry
        entry = (
            f"({row}, {col}): f(n) = {f_score} <- g(n) = {g_score} + h(n) = {h_score}\n"
        )

        # Insert at the beginning (newest at top)
        self.decision_text.insert("1.0", entry, status)

        # Disable editing again
        self.decision_text.config(state=tk.DISABLED)

        # Update UI
        self.decision_text.update()

    def reset_decision_log(self):
        self.decision_text.config(state=tk.NORMAL)
        self.decision_text.delete("1.0", tk.END)
        self.decision_text.config(state=tk.DISABLED)
