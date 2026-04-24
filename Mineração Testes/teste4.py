import pandas as pd
import random

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


# =========================
# 1. Carregar dados
# =========================
df = pd.read_csv("01_tabela_cachorros_gatos_regtest.csv", sep=";")

print("Preview dos dados:")
print(df.head())


# =========================
# 2. Criar FEATURES
# =========================

# Porte baseado no peso
def porte(peso):
    if peso < 10:
        return 0  # pequeno
    elif peso < 25:
        return 1  # médio
    else:
        return 2  # grande

df["porte"] = df["peso"].apply(porte)


# Nível de atividade baseado no batimento cardíaco
def atividade(fc):
    if fc < 90:
        return 0  # baixo
    elif fc < 130:
        return 1  # médio
    else:
        return 2  # alto

df["atividade"] = df["batimento_cardiaco"].apply(atividade)


# =========================
# 3. Criar TARGET (peso médio esperado com VARIAÇÃO)
# =========================
def peso_medio_esperado(row):
    idade = row["idade"]
    porte = row["porte"]
    tipo = row["tipo_do_animal"]

    # base por porte
    if porte == 0:
        base = 6
    elif porte == 1:
        base = 18
    else:
        base = 30

    # ajuste por idade
    if idade < 2:
        base *= 1.1
    elif idade > 8:
        base *= 0.9

    # ajuste por espécie
    if tipo == "gato":
        base *= 0.8

    # VARIAÇÃO REAL 
    base *= random.uniform(0.9, 1.1)

    return base


df["peso_medio"] = df.apply(peso_medio_esperado, axis=1)


# =========================
# 4. Converter categorias
# =========================
df["tipo_do_animal"] = df["tipo_do_animal"].map({
    "cachorro": 0,
    "gato": 1
})


# =========================
# 5. Separar X e y
# =========================
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

y = df["peso_medio"]


# =========================
# 6. Dividir dados
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# =========================
# 7. Treinar modelo
# =========================
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


# =========================
# 8. Testar modelo
# =========================
predicoes = model.predict(X_test)

print("\nComparação (Previsto vs Real):")
for i in range(5):
    print(f"Previsto: {predicoes[i]:.2f} | Real: {y_test.values[i]:.2f}")


# =========================
# 9. Métrica
# =========================
erro = mean_absolute_error(y_test, predicoes)
print("\nErro médio absoluto (MAE):", round(erro, 2))


# =========================
# 10. TESTE FINAL (simulação real)
# =========================

# Dados do animal
peso_real = 35

# calcular porte e atividade
porte_novo = porte(peso_real)
atividade_novo = atividade(120)

novo_animal = pd.DataFrame([{
    "tipo_do_animal": 0,   # cachorro
    "idade": 5,
    "genero": 1,
    "batimento_cardiaco": 120,
    "porte": porte_novo,
    "atividade": atividade_novo
}])

peso_medio_previsto = model.predict(novo_animal)[0]

# índice corporal (IMC adaptado)
indice = peso_real / peso_medio_previsto

# classificação
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