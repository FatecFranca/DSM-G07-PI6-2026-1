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

# Carregar base

df = pd.read_csv("dataset/dataset_tratado.csv")

print("\nBase carregada:")
print(df.shape)


# Definir target

y = df["Weight (lbs)"]
X = df.drop(columns=["Weight (lbs)"])


# Separar colunas

categoricas = X.select_dtypes(include=["object"]).columns.tolist()

numericas = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()


# Pré-processamento

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


# Dividir dados

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Pipeline com Random Forest

pipeline = Pipeline([
    ("preprocessamento", preprocessador),

    ("modelo", RandomForestRegressor(
        n_estimators=100,
        random_state=42
    ))
])


# Treinar modelo completo

print("\nTreinando modelo completo...")

pipeline.fit(X_train, y_train)


# Previsões

predicoes = pipeline.predict(X_test)


# Métricas modelo completo

mae = mean_absolute_error(y_test, predicoes)

rmse = mean_squared_error(
    y_test,
    predicoes
) ** 0.5

r2 = r2_score(y_test, predicoes)

print("\nMÉTRICAS - MODELO COMPLETO")

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R²: {r2:.2f}")


# Importância das features

modelo_rf = pipeline.named_steps["modelo"]

encoder = pipeline.named_steps[
    "preprocessamento"
].named_transformers_["cat"]

nomes_categoricos = encoder.get_feature_names_out(
    categoricas
)

nomes_features = list(nomes_categoricos) + numericas

importancias = modelo_rf.feature_importances_

df_importancias = pd.DataFrame({
    "Feature": nomes_features,
    "Importancia": importancias
})

df_importancias = df_importancias.sort_values(
    by="Importancia",
    ascending=False
)

print("\nTOP 15 FEATURES MAIS IMPORTANTES:\n")
print(df_importancias.head(15))


# Selecionar melhores atributos

top_features = df_importancias.head(10)["Feature"].tolist()

print("\nFeatures selecionadas:")
print(top_features)


# Transformar dados pré-processados

X_train_transformado = pipeline.named_steps[
    "preprocessamento"
].transform(X_train)

X_test_transformado = pipeline.named_steps[
    "preprocessamento"
].transform(X_test)


# Converter para DataFrame

X_train_transformado = pd.DataFrame(
    X_train_transformado,
    columns=nomes_features
)

X_test_transformado = pd.DataFrame(
    X_test_transformado,
    columns=nomes_features
)


# Manter apenas top features

X_train_top = X_train_transformado[top_features]
X_test_top = X_test_transformado[top_features]


# Novo modelo reduzido

modelo_reduzido = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

print("\nTreinando modelo reduzido...")

modelo_reduzido.fit(
    X_train_top,
    y_train
)


# Previsões reduzidas

predicoes_reduzidas = modelo_reduzido.predict(
    X_test_top
)


# Métricas reduzidas

mae_red = mean_absolute_error(
    y_test,
    predicoes_reduzidas
)

rmse_red = mean_squared_error(
    y_test,
    predicoes_reduzidas
) ** 0.5

r2_red = r2_score(
    y_test,
    predicoes_reduzidas
)

print("\nMÉTRICAS - MODELO REDUZIDO")

print(f"MAE: {mae_red:.2f}")
print(f"RMSE: {rmse_red:.2f}")
print(f"R²: {r2_red:.2f}")


# Comparação

print("\nCOMPARAÇÃO FINAL")

print("\nModelo Completo:")
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R²: {r2:.2f}")

print("\nModelo Reduzido:")
print(f"MAE: {mae_red:.2f}")
print(f"RMSE: {rmse_red:.2f}")
print(f"R²: {r2_red:.2f}")


# Salvar modelo reduzido

joblib.dump(
    modelo_reduzido,
    "modelo_reduzido_petdex.pkl"
)

print("\nModelo reduzido salvo com sucesso.")