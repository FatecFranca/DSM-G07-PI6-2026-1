import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

from xgboost import XGBRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# carregar base
df = pd.read_csv(
    "dataset/dataset_sem_nulos_kg.csv"
)

print("\nBASE CARREGADA")
print(df.shape)

print("\nPREVIEW")
print(df.head())


# variável alvo
y = df["Weight (kg)"]

# features
X = df.drop(columns=["Weight (kg)"])


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
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nDIVISÃO DOS DADOS")
print("Treino:", X_train.shape)
print("Teste:", X_test.shape)


# modelos
modelos = {
    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        random_state=42
    ),

    "XGBoost": XGBRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=6,
        random_state=42
    )
}


# resultados
resultados = []

for nome, modelo in modelos.items():

    print(f"\nTREINANDO: {nome}")

    pipeline = Pipeline([
        ("prep", preprocessador),
        ("modelo", modelo)
    ])

    pipeline.fit(X_train, y_train)

    predicoes = pipeline.predict(X_test)

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

    resultados.append({
        "Modelo": nome,
        "MAE (kg)": round(mae, 2),
        "RMSE (kg)": round(rmse, 2),
        "R2": round(r2, 2)
    })


# dataframe final
resultado_df = pd.DataFrame(resultados)

print("\nRESULTADOS FINAIS")
print(resultado_df)


# salvar benchmark
resultado_df.to_csv(
    "benchmark_modelos_kg.csv",
    index=False
)

print("\nBENCHMARK SALVO")
print("Arquivo: benchmark_modelos_kg.csv")