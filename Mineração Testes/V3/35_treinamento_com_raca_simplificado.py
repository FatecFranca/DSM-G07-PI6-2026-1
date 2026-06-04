import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

# ==========================
# CARREGAR BASE
# ==========================

df = pd.read_csv(
    "dataset/dataset_corrigido_kg_lifestage.csv"
)

print("\nBASE CARREGADA")
print(df.shape)

# ==========================
# COLUNAS UTILIZADAS
# ==========================

colunas = [
    "Breed",
    "Breed Size",
    "Sex",
    "Age",
    "Spay/Neuter Status",
    "Life Stage",
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
# COLUNAS
# ==========================

categoricas = [
    "Breed",
    "Breed Size",
    "Sex",
    "Spay/Neuter Status",
    "Life Stage"
]

numericas = [
    "Age"
]

print("\nCOLUNAS CATEGÓRICAS")
print(categoricas)

print("\nCOLUNAS NUMÉRICAS")
print(numericas)

# ==========================
# DIVISÃO
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nDIVISÃO DOS DADOS")
print("Treino:", X_train.shape)
print("Teste:", X_test.shape)

# ==========================
# PIPELINE
# ==========================

preprocessador = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categoricas
        )
    ],
    remainder="passthrough"
)

modelo = Pipeline([
    ("prep", preprocessador),
    ("regressor", LinearRegression())
])

# ==========================
# TREINAMENTO
# ==========================

print("\nTREINANDO MODELO")

modelo.fit(
    X_train,
    y_train
)

# ==========================
# PREVISÕES
# ==========================

y_pred = modelo.predict(
    X_test
)

# ==========================
# MÉTRICAS
# ==========================

mae = mean_absolute_error(
    y_test,
    y_pred
)

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

r2 = r2_score(
    y_test,
    y_pred
)

print("\nRESULTADOS")
print(f"MAE: {mae:.2f} kg")
print(f"RMSE: {rmse:.2f} kg")
print(f"R²: {r2:.2f}")