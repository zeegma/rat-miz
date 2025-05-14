import pandas as pd

def parser():

    print("\nParsing maze.xlsx...")
    # Try to open the excel file and store it to a dataframe variable df
    try:
        df = pd.read_excel('maze.xlsx')
        print("\nReading the excel file and converted to a dataframe.")

        # Lists to store the map matrix and coordinates
        map_matrix = []
        start_coor = []
        finish_coor = []

        # Convert dataframe to a list and return the matrix
        for row in df.axes[0]:
            curr_row = []
            for col in df.axes[1]:
                curr = df.iloc[row][col]
                if curr == 'x':
                    curr_row.append(1)
                elif curr == 'o':
                    curr_row.append(0)
                elif curr == 'S':
                    curr_row.append(0)
                    start_coor += [row, col]
                elif curr == 'F':
                    curr_row.append(0)
                    finish_coor += [row, col]
                else:
                    print("Error: Unknown character in the maze. Aborting parsing.")
                    exit()

            # Append the current row to the two-dimensional matrix
            map_matrix.append(curr_row)

        print("Map has been parsed and ready for map logic.")

        # Return the map, starting coordinates, and finish coordinates
        return map_matrix, start_coor, finish_coor
                        
    # Error if the file cannot be found
    except FileNotFoundError:
        print("Warning: No file found")

if __name__ == "__main__":
    parser()