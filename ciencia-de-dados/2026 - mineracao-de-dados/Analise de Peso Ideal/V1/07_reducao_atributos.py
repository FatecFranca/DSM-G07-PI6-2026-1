import pandas as pd

# carregar base
df = pd.read_csv("dataset/dataset_sem_outliers.csv")

print("\nBASE ORIGINAL")
print(df.shape)

# remover atributos considerados irrelevantes
colunas_remover = [
    "Spay/Neuter Status",
    "Other Pets in Household",
    "Seizures",
    "Owner Activity Level",
    "Average Temperature (F)"
]

df = df.drop(columns=colunas_remover)

print("\nCOLUNAS REMOVIDAS")
print(colunas_remover)

print("\nCOLUNAS FINAIS")
print(df.columns)

print("\nTAMANHO FINAL")
print(df.shape)

print("\nPREVIEW FINAL")
print(df.head())

# salvar nova base
df.to_csv("dataset/dataset_reduzido.csv", index=False)

print("\nNova base salva:")
print("dataset/dataset_reduzido.csv")