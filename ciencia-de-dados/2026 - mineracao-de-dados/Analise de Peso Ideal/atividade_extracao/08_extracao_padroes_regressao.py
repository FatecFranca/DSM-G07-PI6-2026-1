import pandas as pd

# Importação da função responsável por dividir os dados
# em conjuntos de treino e teste
from sklearn.model_selection import train_test_split

# Ferramentas utilizadas no pré-processamento
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# Algoritmos de regressão utilizados na extração de padrões
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

# Métricas utilizadas para avaliação dos modelos
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# -------------------------------------------------------------------
# OBJETIVO DA ETAPA
# -------------------------------------------------------------------
# Esta etapa tem como objetivo realizar a extração de padrões
# utilizando algoritmos de Machine Learning do tipo regressão.
#
# O foco do modelo é aprender padrões existentes na base de dados
# para prever o peso saudável esperado de cães com base em
# características físicas e comportamentais.
#
# Também é realizada uma comparação entre diferentes algoritmos
# de regressão para identificar qual apresenta melhor desempenho.
# -------------------------------------------------------------------


# carregar base reduzida
# A base utilizada já passou pelas etapas anteriores de:
# - limpeza
# - remoção de atributos irrelevantes
# - tratamento de dados
# - redução de features
df = pd.read_csv("dataset/dataset_reduzido.csv")

print("\nBASE CARREGADA")
print(df.shape)

print("\nPREVIEW")
print(df.head())


# variável alvo (target)
# O modelo irá tentar prever o peso do animal
y = df["Weight (lbs)"]

# features
# Todas as demais colunas serão utilizadas como atributos de entrada
X = df.drop(columns=["Weight (lbs)"])


# separar colunas categóricas e numéricas
# Essa separação é necessária para aplicar transformações adequadas
categoricas = X.select_dtypes(include=["object"]).columns.tolist()
numericas = X.select_dtypes(exclude=["object"]).columns.tolist()

print("\nCOLUNAS CATEGÓRICAS")
print(categoricas)

print("\nCOLUNAS NUMÉRICAS")
print(numericas)


# pré-processamento
# O algoritmo de Machine Learning não trabalha diretamente com texto.
#
# Por isso, as colunas categóricas passam por OneHotEncoder,
# transformando categorias em valores numéricos binários.
#
# Exemplo:
# "Male" -> [1,0]
# "Female" -> [0,1]
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


# divisão treino/teste
# 80% da base será utilizada para treinamento
# 20% será utilizada para testes e validação
#
# Isso permite verificar se o modelo consegue generalizar
# corretamente para dados nunca vistos.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nDIVISÃO DOS DADOS")
print("Treino:", X_train.shape)
print("Teste:", X_test.shape)


# modelos utilizados
#
# Linear Regression:
# Busca relações lineares entre os atributos e o peso.
#
# Random Forest:
# Utiliza múltiplas árvores de decisão para encontrar padrões.
#
# Gradient Boosting:
# Treina árvores sequenciais corrigindo erros anteriores.
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


# lista para armazenar os resultados finais
resultados = []


# treinamento e avaliação dos modelos
for nome, modelo in modelos.items():

    print(f"\nTREINANDO: {nome}")

    # Pipeline
    # Une pré-processamento + treinamento em uma única estrutura
    pipeline = Pipeline([
        ("prep", preprocessador),
        ("modelo", modelo)
    ])

    # treinamento do modelo
    # O algoritmo aprende padrões a partir dos dados de treino
    pipeline.fit(X_train, y_train)

    # geração das previsões
    predicoes = pipeline.predict(X_test)

    # cálculo do erro médio absoluto
    # Mede o erro médio entre valor previsto e valor real
    mae = mean_absolute_error(y_test, predicoes)

    # cálculo da raiz do erro quadrático médio
    # Penaliza erros maiores
    rmse = mean_squared_error(
        y_test,
        predicoes
    ) ** 0.5

    # cálculo do R²
    # Mede o quanto o modelo consegue explicar os dados
    r2 = r2_score(y_test, predicoes)

    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R²: {r2:.2f}")

    # salvar resultados
    resultados.append({
        "Modelo": nome,
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "R2": round(r2, 2)
    })


# dataframe final com benchmark dos modelos
resultado_df = pd.DataFrame(resultados)

print("\nRESULTADOS FINAIS")
print(resultado_df)


# salvar benchmark
# O benchmark permite comparar o desempenho
# entre os diferentes algoritmos utilizados
resultado_df.to_csv(
    "benchmark_modelos_reduzidos.csv",
    index=False
)

print("\nBenchmark salvo com sucesso.")
print("Arquivo: benchmark_modelos_reduzidos.csv")