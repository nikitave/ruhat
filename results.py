import pandas as pd

def export_to_excel(data, filename):
    """
    Export dataframe with results of a quiz to excel file
    """
    df = pd.DataFrame(data)
    df.to_excel(f'storage\{filename}', sheet_name="Results", index=False)
