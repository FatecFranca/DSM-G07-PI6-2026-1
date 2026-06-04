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


# carregar base corrigida
df = pd.read_csv(
    "dataset/dataset_corrigido_kg.csv"
)

print("\nBASE CARREGADA")
print(df.shape)


# variável alvo
y = df["Weight (kg)"]

# features
X = df.drop(columns=["Weight (kg)"])


# guardar raça para análise posterior
racas = df["Breed"]


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
    racas_train,
    racas_test
) = train_test_split(
    X,
    y,
    racas,
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

print("\nMÉTRICAS GERAIS")

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

print(f"MAE: {mae:.2f} kg")
print(f"RMSE: {rmse:.2f} kg")
print(f"R²: {r2:.2f}")


# dataframe para análise
resultado = pd.DataFrame({
    "Breed": racas_test.values,
    "Peso Real": y_test.values,
    "Peso Previsto": predicoes
})

resultado["Erro Absoluto"] = (
    resultado["Peso Real"]
    -
    resultado["Peso Previsto"]
).abs()


# análise por raça
erro_por_raca = (
    resultado
    .groupby("Breed")
    .agg({
        "Erro Absoluto": "mean",
        "Peso Real": "count"
    })
    .rename(columns={
        "Erro Absoluto": "MAE",
        "Peso Real": "Quantidade"
    })
    .sort_values(
        by="MAE",
        ascending=False
    )
)

print("\nERRO MÉDIO POR RAÇA")
print(erro_por_raca)


# top 5 melhores
print("\nTOP 5 RAÇAS COM MENOR ERRO")
print(
    erro_por_raca
    .sort_values("MAE")
    .head(5)
)


# top 5 piores
print("\nTOP 5 RAÇAS COM MAIOR ERRO")
print(
    erro_por_raca
    .sort_values("MAE", ascending=False)
    .head(5)
)


# salvar csv
erro_por_raca.to_csv(
    "erro_por_raca.csv"
)

print("\nARQUIVO SALVO")
print("erro_por_raca.csv")