import pandas as pd

# carregar base em kg
df = pd.read_csv("dataset/dataset_kg.csv")

print("\nBASE ORIGINAL")
print(df.shape)


# manter apenas animais saudáveis
df = df[df["Healthy"] == "Yes"]

print("\nAPÓS FILTRAR SAUDÁVEIS")
print(df.shape)


# remover colunas irrelevantes
colunas_remover = [
    "ID",
    "Diet",
    "Food Brand",
    "Medications",
    "Synthetic",
    "Healthy",
    "Average Temperature (F)",
    "Other Pets in Household",
    "Seizures",
    "Owner Activity Level"
]

df = df.drop(columns=colunas_remover)

print("\nCOLUNAS RESTANTES")
print(df.columns)


# verificar nulos
print("\nVALORES NULOS ANTES")
print(df.isnull().sum())


# remover registros nulos


print("\nVALORES NULOS DEPOIS")
print(df.isnull().sum())


print("\nBASE FINAL")
print(df.shape)


# preview
print("\nPREVIEW FINAL")
print(df.head())


# salvar
df.to_csv(
    "dataset/dataset_limpo_kg.csv",
    index=False
)

print("\nBASE LIMPA SALVA")
print("Arquivo: dataset/dataset_limpo_kg.csv")