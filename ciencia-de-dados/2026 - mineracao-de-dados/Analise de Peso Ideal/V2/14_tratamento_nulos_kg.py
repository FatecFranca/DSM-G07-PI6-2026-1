import pandas as pd

# carregar base
df = pd.read_csv("dataset/dataset_limpo_kg.csv")

print("\nBASE ORIGINAL")
print(df.shape)


# separar colunas categóricas e numéricas
categoricas = df.select_dtypes(include=["object"]).columns
numericas = df.select_dtypes(exclude=["object"]).columns

print("\nCOLUNAS CATEGÓRICAS")
print(categoricas)

print("\nCOLUNAS NUMÉRICAS")
print(numericas)


# preencher categóricas com "Unknown"
for coluna in categoricas:
    df[coluna] = df[coluna].fillna("Unknown")


# preencher numéricas com mediana
for coluna in numericas:
    mediana = df[coluna].median()
    df[coluna] = df[coluna].fillna(mediana)


print("\nVALORES NULOS FINAIS")
print(df.isnull().sum())


print("\nBASE FINAL")
print(df.shape)


print("\nPREVIEW")
print(df.head())


# salvar
df.to_csv(
    "dataset/dataset_sem_nulos_kg.csv",
    index=False
)

print("\nBASE SALVA")
print("Arquivo: dataset/dataset_sem_nulos_kg.csv")