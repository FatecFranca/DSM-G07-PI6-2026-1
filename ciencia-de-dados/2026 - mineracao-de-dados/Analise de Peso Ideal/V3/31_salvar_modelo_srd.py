import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression


df = pd.read_csv(
    "dataset/dataset_corrigido_kg.csv"
)

print("\nBASE CARREGADA")
print(df.shape)



df = df[
    df["Breed Size"] != "Unknown"
]

print("\nAPÓS REMOVER UNKNOWN")
print(df.shape)


colunas = [
    "Breed Size",
    "Sex",
    "Spay/Neuter Status",
    "Age",
    "Weight (kg)"
]

df = df[colunas]

print("\nCOLUNAS UTILIZADAS")
print(df.columns)

y = df["Weight (kg)"]

X = df.drop(
    columns=["Weight (kg)"]
)

categoricas = [
    "Breed Size",
    "Sex",
    "Spay/Neuter Status"
]

numericas = [
    "Age"
]

print("\nCOLUNAS CATEGÓRICAS")
print(categoricas)

print("\nCOLUNAS NUMÉRICAS")
print(numericas)


preprocessador = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categoricas
        )
    ],
    remainder="passthrough"
)

modelo = Pipeline([
    ("prep", preprocessador),
    ("regressor", LinearRegression())
])

print("\nTREINANDO MODELO FINAL SRD...")

modelo.fit(
    X,
    y
)

print("MODELO TREINADO")


joblib.dump(
    modelo,
    "modelo_srd.pkl"
)

print("\nMODELO SALVO")
print("Arquivo: modelo_srd.pkl")