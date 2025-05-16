def compute_offset(maze_obj):
    # Calculate top padding to visually center maze
    canvas_height = maze_obj.canvas.winfo_height()
    canvas_width = maze_obj.canvas.winfo_width()

    maze_height = maze_obj.rows * maze_obj.cell_size
    maze_width = maze_obj.cols * maze_obj.cell_size

    x_offset = max((canvas_width - maze_width) // 2, 0)
    y_offset = max((canvas_height - maze_height) // 2, 0)

    return x_offset, y_offset
