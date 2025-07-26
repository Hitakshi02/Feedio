import pandas as pd
import os

def load_csv(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File not found: {csv_path}")

    df = pd.read_csv(csv_path)

    # Expect at least a 'text' or 'feedback' column
    if 'text' not in df.columns:
        raise ValueError("CSV must contain a 'text' column.")

    df = df[['text']].dropna()
    df.reset_index(drop=True, inplace=True)
    return df

def generate_simple_upload_id(path="data/upload_counter.txt"):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("0000")

    with open(path, "r") as f:
        last = int(f.read())

    new_id = f"{last + 1:04d}"

    with open(path, "w") as f:
        f.write(new_id)

    return new_id
