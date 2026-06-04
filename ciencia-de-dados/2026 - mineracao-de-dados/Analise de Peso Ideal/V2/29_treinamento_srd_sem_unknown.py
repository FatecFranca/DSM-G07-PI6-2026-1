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



df = pd.read_csv(
    "dataset/dataset_corrigido_kg.csv"
)

print("\nBASE ORIGINAL")
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



X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nDIVISÃO DOS DADOS")
print("Treino:", X_train.shape)
print("Teste:", X_test.shape)



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
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "R2": round(r2, 2)
    })

resultado_df = pd.DataFrame(
    resultados
)

print("\nRESULTADOS FINAIS")
print(resultado_df)

resultado_df.to_csv(
    "benchmark_srd_sem_unknown.csv",
    index=False
)

print("\nBENCHMARK SALVO")
print("benchmark_srd_sem_unknown.csv")