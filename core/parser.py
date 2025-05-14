import pandas as pd

def parser():

    # Try to open the excel file and store it to a dataframe variable df
    try:
        df = pd.read_excel('maze.xlsx')
        print("Read the excel file and converted to a dataframe.")

        # Convert dataframe to a list and return the matrix
        return df.values.tolist()
        
    except FileNotFoundError:
        print("Warning: No file found")
