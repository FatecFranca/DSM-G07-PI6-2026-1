import pandas as pd
import random

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


# =========================
# PRÉ-PROCESSAMENTO REALIZADO
# - Seleção manual de atributos relevantes na base original
# - Criação de novas variáveis (feature engineering)
# - Transformação de dados categóricos em numéricos
# - Definição da variável alvo (target)
# - Separação dos dados em treino e teste
# =========================


# 1. Carregar dados
# Leitura da base de dados já previamente tratada (remoção manual de atributos irrelevantes)
df = pd.read_csv("01_tabela_cachorros_gatos_regtest.csv", sep=";")

print("Preview dos dados:")
print(df.head())


# 2. Criar FEATURES (Feature Engineering)

# Criação da variável "porte" com base no peso do animal
# Essa transformação reduz a dependência de raça e melhora a generalização do modelo
def porte(peso):
    if peso < 10:
        return 0  # pequeno
    elif peso < 25:
        return 1  # médio
    else:
        return 2  # grande

df["porte"] = df["peso"].apply(porte)


# Criação da variável "atividade" com base no batimento cardíaco
# Isso permite incluir uma característica fisiológica no modelo
def atividade(fc):
    if fc < 90:
        return 0  # baixo
    elif fc < 130:
        return 1  # médio
    else:
        return 2  # alto

df["atividade"] = df["batimento_cardiaco"].apply(atividade)


# 3. Criar TARGET (variável alvo)

# Criação da variável "peso_medio", que será o valor a ser previsto pelo modelo
# Essa variável é construída com base em regras de domínio (porte, idade e tipo do animal)
def peso_medio_esperado(row):
    idade = row["idade"]
    porte = row["porte"]
    tipo = row["tipo_do_animal"]

    # Definição de um valor base de peso de acordo com o porte
    if porte == 0:
        base = 6
    elif porte == 1:
        base = 18
    else:
        base = 30

    # Ajuste do peso conforme a idade do animal
    if idade < 2:
        base *= 1.1
    elif idade > 8:
        base *= 0.9

    # Ajuste do peso conforme o tipo do animal
    if tipo == "gato":
        base *= 0.8

    # Adição de uma pequena variação aleatória
    # Isso evita que o modelo memorize valores fixos (overfitting)
    base *= random.uniform(0.9, 1.1)

    return base


df["peso_medio"] = df.apply(peso_medio_esperado, axis=1)


# 4. Transformação de dados categóricos

# Conversão da variável "tipo_do_animal" de texto para valor numérico
# Necessário pois o modelo de machine learning não trabalha com dados textuais
df["tipo_do_animal"] = df["tipo_do_animal"].map({
    "cachorro": 0,
    "gato": 1
})


# 5. Seleção de atributos (Feature Selection)

# Definição das variáveis de entrada (features)
# Foram selecionadas apenas as variáveis consideradas relevantes
X = df[
    [
        "tipo_do_animal",
        "idade",
        "genero",
        "batimento_cardiaco",
        "porte",        
        "atividade",
    ]
]

# Definição da variável alvo
y = df["peso_medio"]


# 6. Divisão dos dados

# Separação dos dados em conjunto de treino e teste
# 80% para treino e 20% para teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# 7. Treinar modelo
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


# 8. Testar modelo
predicoes = model.predict(X_test)

print("\nComparação (Previsto vs Real):")
for i in range(5):
    print(f"Previsto: {predicoes[i]:.2f} | Real: {y_test.values[i]:.2f}")


# 9. Métrica de avaliação

# Cálculo do erro médio absoluto (MAE)
erro = mean_absolute_error(y_test, predicoes)
print("\nErro médio absoluto (MAE):", round(erro, 2))


# 10. TESTE FINAL

peso_real = 35

porte_novo = porte(peso_real)
atividade_novo = atividade(120)

novo_animal = pd.DataFrame([{
    "tipo_do_animal": 0,
    "idade": 5,
    "genero": 1,
    "batimento_cardiaco": 120,
    "porte": porte_novo,
    "atividade": atividade_novo
}])

peso_medio_previsto = model.predict(novo_animal)[0]

# Cálculo do índice corporal
indice = peso_real / peso_medio_previsto

# Classificação do estado do animal
if indice > 1.1:
    status = "Acima do peso"
elif indice < 0.9:
    status = "Abaixo do peso"
else:
    status = "Peso saudável"


print("\n===== RESULTADO FINAL =====")
print("Peso real:", peso_real)
print("Peso médio esperado:", round(peso_medio_previsto, 2))
print("Índice corporal:", round(indice, 2))
print("Status:", status)