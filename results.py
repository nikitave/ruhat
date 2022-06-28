import pandas as pd
from flask import send_file, send_from_directory


def export_to_excel(data, filename):
    """
    Export dataframe with results of a quiz to excel file
    """

    df = pd.DataFrame(data)
    df.to_excel(filename, sheet_name="Results", index=False)
