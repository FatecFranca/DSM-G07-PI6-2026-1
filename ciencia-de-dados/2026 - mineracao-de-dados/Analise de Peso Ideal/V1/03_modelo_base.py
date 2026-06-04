import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# 1. CARREGAR BASE TRATADA

df = pd.read_csv("dataset/dataset_tratado.csv")

print("\n===== BASE CARREGADA =====")
print(df.head())

print("\nTamanho da base:", df.shape)

# 2. DEFINIR TARGET

# Variável alvo (o que queremos prever)
y = df["Weight (lbs)"]

# Remover target das entradas
X = df.drop(columns=["Weight (lbs)"])

# 3. IDENTIFICAR COLUNAS

# Colunas categóricas
categoricas = X.select_dtypes(include=["object"]).columns.tolist()

# Colunas numéricas
numericas = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

print("\n===== COLUNAS CATEGÓRICAS =====")
print(categoricas)

print("\n===== COLUNAS NUMÉRICAS =====")
print(numericas)

# 4. PRÉ-PROCESSAMENTO

# Converter categorias em números
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

# 5. DIVIDIR TREINO E TESTE


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\n===== DIVISÃO DOS DADOS =====")
print("Treino:", X_train.shape)
print("Teste:", X_test.shape)

# 6. CRIAR PIPELINE


pipeline = Pipeline([
    ("preprocessamento", preprocessador),

    ("modelo", RandomForestRegressor(
        n_estimators=100,
        random_state=42
    ))
])


# 7. TREINAR MODELO

print("\n===== TREINANDO MODELO =====")

pipeline.fit(X_train, y_train)

print("Modelo treinado com sucesso.")


# 8. FAZER PREVISÕES

predicoes = pipeline.predict(X_test)


# 9. MÉTRICAS

mae = mean_absolute_error(y_test, predicoes)

rmse = mean_squared_error(
    y_test,
    predicoes
) ** 0.5

r2 = r2_score(y_test, predicoes)

print("\n===== MÉTRICAS =====")

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R²: {r2:.2f}")


# 10. COMPARAÇÃO


print("\n===== PREVISÕES VS REAL =====")

for i in range(10):
    print(
        f"Previsto: {predicoes[i]:.2f} lbs "
        f"| Real: {y_test.values[i]:.2f} lbs"
    )

# 11. TESTE MANUAL


novo_animal = pd.DataFrame([{
    "Breed": "Labrador Retriever",
    "Breed Size": "Large",
    "Sex": "Male",
    "Age": 5,
    "Spay/Neuter Status": "Yes",
    "Daily Activity Level": "High",
    "Daily Walk Distance (miles)": 3.0,
    "Other Pets in Household": "No",
    "Seizures": "No",
    "Hours of Sleep": 8,
    "Play Time (hrs)": 2,
    "Owner Activity Level": "Active",
    "Annual Vet Visits": 1,
    "Average Temperature (F)": 70
}])

peso_previsto = pipeline.predict(novo_animal)[0]

print("\n===== TESTE MANUAL =====")
print(f"Peso saudável previsto: {peso_previsto:.2f} lbs")


# 12. SALVAR MODELO


joblib.dump(
    pipeline,
    "modelo_peso_petdex.pkl"
)

print("\n===== MODELO SALVO =====")
print("Arquivo: modelo_peso_petdex.pkl")