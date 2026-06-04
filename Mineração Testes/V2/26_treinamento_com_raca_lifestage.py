import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ==========================
# CARREGAR BASE
# ==========================

df = pd.read_csv(
    "dataset/dataset_corrigido_kg_lifestage.csv"
)

print("\nBASE CARREGADA")
print(df.shape)

print("\nPREVIEW")
print(df.head())


# ==========================
# TARGET E FEATURES
# ==========================

y = df["Weight (kg)"]

X = df.drop(
    columns=["Weight (kg)"]
)


# ==========================
# IDENTIFICAR COLUNAS
# ==========================

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
# DIVISÃO TREINO / TESTE
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nDIVISÃO DOS DADOS")
print("Treino:", X_train.shape)
print("Teste:", X_test.shape)


# ==========================
# MODELOS
# ==========================

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


# ==========================
# TREINAMENTO
# ==========================

resultados = []

for nome, modelo in modelos.items():

    print(f"\nTREINANDO: {nome}")

    pipeline = Pipeline([
        ("prep", preprocessador),
        ("modelo", modelo)
    ])

    pipeline.fit(
        X_train,
        y_train
    )

    predicoes = pipeline.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predicoes
    )

    rmse = (
        mean_squared_error(
            y_test,
            predicoes
        ) ** 0.5
    )

    r2 = r2_score(
        y_test,
        predicoes
    )

    print(f"MAE: {mae:.2f} kg")
    print(f"RMSE: {rmse:.2f} kg")
    print(f"R²: {r2:.2f}")

    resultados.append({
        "Modelo": nome,
        "MAE (kg)": round(mae, 2),
        "RMSE (kg)": round(rmse, 2),
        "R2": round(r2, 2)
    })


# ==========================
# RESULTADOS
# ==========================

resultado_df = pd.DataFrame(
    resultados
)

print("\nRESULTADOS FINAIS")
print(resultado_df)


# ==========================
# SALVAR BENCHMARK
# ==========================

resultado_df.to_csv(
    "benchmark_com_raca_lifestage.csv",
    index=False
)

print("\nBENCHMARK SALVO")
print(
    "benchmark_com_raca_lifestage.csv"
)