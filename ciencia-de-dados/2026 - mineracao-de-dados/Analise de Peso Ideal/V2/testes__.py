import pandas as pd

df = pd.read_csv("dataset/dataset_corrigido_kg.csv")

print(
    df["Breed Size"]
    .value_counts(dropna=False)
)