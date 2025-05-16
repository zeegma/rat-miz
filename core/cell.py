class Cell:
    def __init__(self):
        # Parent cell's row index
        self.parent_x = 0
        # Parent cell's column index
        self.parent_y = 0
        # Total cost of the cell (g + h)
        self.f = float("inf")
        # Cost from start to this cell
        self.g = float("inf")
        # Heuristic cost from this cell to destination
        self.h = 0
