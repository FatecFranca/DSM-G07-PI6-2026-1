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
    "dataset/dataset_corrigido_kg_lifestage.csv"
)

print("\nBASE CARREGADA")
print(df.shape)

# ==========================
# TARGET
# ==========================

y = df["Weight (kg)"]

X = df.drop(
    columns=["Weight (kg)"]
)

# ==========================
# COLUNAS
# ==========================

categoricas = [
    "Breed",
    "Breed Size",
    "Sex",
    "Spay/Neuter Status",
    "Daily Activity Level",
    "Life Stage"
]

numericas = [
    "Age",
    "Daily Walk Distance (miles)",
    "Hours of Sleep",
    "Play Time (hrs)",
    "Annual Vet Visits"
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

print("\nTREINANDO MODELO FINAL...")

modelo.fit(
    X,
    y
)

print("MODELO TREINADO")

# ==========================
# SALVAR MODELO
# ==========================

joblib.dump(
    modelo,
    "modelo_com_raca.pkl"
)

print("\nMODELO SALVO")
print("Arquivo: modelo_com_raca.pkl")