import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# carregar base
df = pd.read_csv(
    "dataset/dataset_corrigido_kg.csv"
)

print("\nBASE CARREGADA")
print(df.shape)

# variável alvo
y = df["Weight (kg)"]

# features
X = df.drop(columns=["Weight (kg)"])

# guardar raça
racas = df["Breed"]

# separar colunas
categoricas = X.select_dtypes(
    include=["object"]
).columns.tolist()

numericas = X.select_dtypes(
    exclude=["object"]
).columns.tolist()

# pré-processamento
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

# divisão treino/teste
(
    X_train,
    X_test,
    y_train,
    y_test,
    racas_train,
    racas_test
) = train_test_split(
    X,
    y,
    racas,
    test_size=0.2,
    random_state=42
)

# modelo
pipeline = Pipeline([
    ("prep", preprocessador),
    ("modelo", LinearRegression())
])

print("\nTREINANDO MODELO")

pipeline.fit(
    X_train,
    y_train
)

predicoes = pipeline.predict(
    X_test
)

# métricas gerais
mae = mean_absolute_error(
    y_test,
    predicoes
)

rmse = mean_squared_error(
    y_test,
    predicoes
) ** 0.5

r2 = r2_score(
    y_test,
    predicoes
)

print("\nMÉTRICAS GERAIS")
print(f"MAE: {mae:.2f} kg")
print(f"RMSE: {rmse:.2f} kg")
print(f"R²: {r2:.2f}")

# dataframe de análise
resultado = pd.DataFrame({
    "Breed": racas_test.values,
    "Peso Real": y_test.values,
    "Peso Previsto": predicoes
})

# erro absoluto
resultado["Erro Absoluto"] = (
    resultado["Peso Real"]
    - resultado["Peso Previsto"]
).abs()

# erro percentual
resultado["Erro Percentual"] = (
    resultado["Erro Absoluto"]
    / resultado["Peso Real"]
) * 100

# agrupar por raça
erro_percentual = (
    resultado
    .groupby("Breed")
    .agg({
        "Erro Percentual": "mean",
        "Peso Real": "count"
    })
    .rename(columns={
        "Erro Percentual": "Erro Médio (%)",
        "Peso Real": "Quantidade"
    })
    .sort_values(
        by="Erro Médio (%)",
        ascending=False
    )
)

print("\nERRO PERCENTUAL POR RAÇA")
print(erro_percentual)

print("\nTOP 5 MELHORES RAÇAS")
print(
    erro_percentual
    .sort_values("Erro Médio (%)")
    .head(5)
)

print("\nTOP 5 PIORES RAÇAS")
print(
    erro_percentual
    .sort_values(
        "Erro Médio (%)",
        ascending=False
    )
    .head(5)
)

# salvar
erro_percentual.to_csv(
    "erro_percentual_por_raca.csv"
)

print("\nARQUIVO SALVO")
print("erro_percentual_por_raca.csv")