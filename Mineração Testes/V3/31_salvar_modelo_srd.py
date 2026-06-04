import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression

# ==========================
# CARREGAR BASE
# ==========================

df = pd.read_csv(
    "dataset/dataset_corrigido_kg.csv"
)

print("\nBASE CARREGADA")
print(df.shape)

# ==========================
# REMOVER UNKNOWN
# ==========================

df = df[
    df["Breed Size"] != "Unknown"
]

print("\nAPÓS REMOVER UNKNOWN")
print(df.shape)

# ==========================
# COLUNAS UTILIZADAS
# ==========================

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

# ==========================
# TARGET
# ==========================

y = df["Weight (kg)"]

X = df.drop(
    columns=["Weight (kg)"]
)

# ==========================
# COLUNAS CATEGÓRICAS
# ==========================

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

# ==========================
# PRÉ-PROCESSAMENTO
# ==========================

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

# ==========================
# MODELO FINAL
# ==========================

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

# ==========================
# SALVAR
# ==========================

joblib.dump(
    modelo,
    "modelo_srd.pkl"
)

print("\nMODELO SALVO")
print("Arquivo: modelo_srd.pkl")