import pandas as pd

# carregar dataset
df = pd.read_csv("dataset/synthetic_dog_breed_health_data.csv")

# INFORMAÇÕES GERAIS

print("\n===== PRIMEIRAS LINHAS =====")
print(df.head())

print("\n===== COLUNAS =====")
print(df.columns)

print("\n===== TIPOS DE DADOS =====")
print(df.dtypes)

print("\n===== TAMANHO DA BASE =====")
print(df.shape)

print("\n===== INFORMAÇÕES GERAIS =====")
print(df.info())

print("\n===== VALORES NULOS =====")
print(df.isnull().sum())

print("\n===== ESTATÍSTICAS =====")
print(df.describe())