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


# guardar porte para análise
portes = df["Breed Size"]


# separar colunas
categoricas = X.select_dtypes(
    include=["object"]
).columns.tolist()

numericas = X.select_dtypes(
    exclude=["object"]
).columns.tolist()

print("\nCOLUNAS CATEGÓRICAS")
print(categoricas)

print("\nCOLUNAS NUMÉRICAS")
print(numericas)


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
    portes_train,
    portes_test
) = train_test_split(
    X,
    y,
    portes,
    test_size=0.2,
    random_state=42
)

print("\nDIVISÃO DOS DADOS")
print("Treino:", X_train.shape)
print("Teste:", X_test.shape)


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


# dataframe para análise
resultado = pd.DataFrame({
    "Breed Size": portes_test.values,
    "Peso Real": y_test.values,
    "Peso Previsto": predicoes
})

# erro absoluto
resultado["Erro Absoluto"] = (
    resultado["Peso Real"]
    -
    resultado["Peso Previsto"]
).abs()

# erro percentual
resultado["Erro Percentual"] = (
    resultado["Erro Absoluto"]
    /
    resultado["Peso Real"]
) * 100


# análise por porte
erro_por_porte = (
    resultado
    .groupby("Breed Size")
    .agg({
        "Erro Absoluto": "mean",
        "Erro Percentual": "mean",
        "Peso Real": "count"
    })
    .rename(columns={
        "Erro Absoluto": "MAE (kg)",
        "Erro Percentual": "Erro Médio (%)",
        "Peso Real": "Quantidade"
    })
    .sort_values(
        by="Erro Médio (%)",
        ascending=False
    )
)

print("\nERRO POR PORTE")
print(erro_por_porte)


# salvar csv
erro_por_porte.to_csv(
    "erro_por_porte.csv"
)

print("\nARQUIVO SALVO")
print("erro_por_porte.csv")