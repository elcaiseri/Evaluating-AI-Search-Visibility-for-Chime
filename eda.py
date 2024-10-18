import os
import pandas as pd
from typing import Dict

# Constants
SUSTAINABILITY_PATH = "backend/data/Dataset 1 (Sustainability Research Results).xlsx"
CHRISTMAS_PATH = "backend/data/Dataset 2 (Christmas Research Results).xlsx"
PROCESSED_DIR = "backend/data/processed/"

def load_excel(file_path: str) -> pd.DataFrame:
    """
    Load an Excel file into a pandas DataFrame.

    Parameters:
        file_path (str): Path to the Excel file.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    try:
        return pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        raise ValueError(f"Failed to load {file_path}: {str(e)}")

def extract_data_blocks(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Extract sections from the DataFrame based on 'Question' headers.

    Parameters:
        df (pd.DataFrame): Input DataFrame to process.

    Returns:
        Dict[str, pd.DataFrame]: Dictionary of DataFrames split by questions.
    """
    question_rows = df[df.iloc[:, 0].str.contains('Question', na=False)].index

    # Extract data blocks by iterating over question rows
    data_blocks = {
        df.iloc[start, 0]: df.iloc[start:end].reset_index(drop=True)
        for start, end in zip(question_rows, question_rows[1:].tolist() + [len(df)])
    }
    return data_blocks

def save_data_blocks(data_blocks: Dict[str, pd.DataFrame], prefix: str) -> None:
    """
    Save each data block to an Excel file.

    Parameters:
        data_blocks (Dict[str, pd.DataFrame]): Dictionary of data blocks.
        prefix (str): Prefix for the saved file names (e.g., 'sustainability').
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    for key, df in data_blocks.items():
        filename = f"{prefix}_{'_'.join(key.split()[:2]).lower()}.xlsx"
        save_path = os.path.join(PROCESSED_DIR, filename)
        try:
            df.to_excel(save_path, index=False)
            print(f"Saved: {save_path}")
        except Exception as e:
            print(f"Failed to save {filename}: {str(e)}")

def process_dataset(file_path: str, prefix: str) -> None:
    """
    Load, process, and save data blocks for a given dataset.

    Parameters:
        file_path (str): Path to the dataset Excel file.
        prefix (str): Prefix for naming the processed files.
    """
    print(f"Processing {prefix} dataset...")
    df = load_excel(file_path)
    data_blocks = extract_data_blocks(df)
    save_data_blocks(data_blocks, prefix)
    print(f"Processing of {prefix} dataset completed.")

if __name__ == "__main__":
    process_dataset(SUSTAINABILITY_PATH, "sustainability")
    process_dataset(CHRISTMAS_PATH, "christmas")
    print("All datasets processed and saved successfully.")