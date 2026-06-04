import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor


# Carregar base
df = pd.read_csv("dataset/dataset_sem_outliers.csv")

print("\nBASE CARREGADA")
print(df.shape)


# Remover coluna problemática
df = df.drop(columns=["Breed Size"])


# Variável alvo
y = df["Weight (lbs)"]

# Features
X = df.drop(columns=["Weight (lbs)"])


# Separar colunas
colunas_categoricas = X.select_dtypes(include=["object"]).columns.tolist()

colunas_numericas = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()


print("\nCOLUNAS CATEGÓRICAS")
print(colunas_categoricas)

print("\nCOLUNAS NUMÉRICAS")
print(colunas_numericas)


# Pré-processamento
preprocessor = ColumnTransformer([
    (
        "cat",
        OneHotEncoder(handle_unknown="ignore"),
        colunas_categoricas
    )
], remainder="passthrough")


# Divisão treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Modelos
modelos = {
    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        random_state=42
    )
}


# Treinar e avaliar
resultados = []

for nome, modelo in modelos.items():

    print(f"\nTREINANDO: {nome}")

    pipeline = Pipeline([
        ("preprocessamento", preprocessor),
        ("modelo", modelo)
    ])

    pipeline.fit(X_train, y_train)

    predicoes = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, predicoes)

    rmse = mean_squared_error(
        y_test,
        predicoes
    ) ** 0.5

    r2 = r2_score(y_test, predicoes)

    resultados.append({
        "Modelo": nome,
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "R2": round(r2, 2)
    })

    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R²: {r2:.2f}")


# Resultado final
resultado_df = pd.DataFrame(resultados)

print("\nRESULTADOS FINAIS")
print(resultado_df)


# Salvar benchmark
resultado_df.to_csv(
    "dataset/benchmark_modelos.csv",
    index=False
)

print("\nBenchmark salvo com sucesso.")