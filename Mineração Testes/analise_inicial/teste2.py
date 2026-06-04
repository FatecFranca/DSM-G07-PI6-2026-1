import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# =========================
# 1. Carregar dados
# =========================
df = pd.read_csv("01_tabela_cachorros_gatos_regtest.csv", sep=";")

print("Preview dos dados:")
print(df.head())


# =========================
# 2. Criar PESO IDEAL (melhorado)
# =========================
def calcular_peso_ideal(row):
    peso = row["peso"]
    idade = row["idade"]
    tipo = row["tipo_do_animal"]

    # ajuste por idade
    if idade < 2:
        fator_idade = 1.1
    elif idade > 8:
        fator_idade = 0.9
    else:
        fator_idade = 1.0

    # ajuste por espécie
    if tipo == "gato":
        fator_tipo = 0.95
    else:
        fator_tipo = 1.0

    return peso * fator_idade * fator_tipo


df["peso_ideal"] = df.apply(calcular_peso_ideal, axis=1)


# =========================
# 3. Criar FEATURES novas
# =========================

# Porte baseado no peso
def porte(peso):
    if peso < 10:
        return 0
    elif peso < 25:
        return 1
    else:
        return 2

df["porte"] = df["peso"].apply(porte)


# Atividade baseada no batimento cardíaco
def atividade(fc):
    if fc < 90:
        return 0
    elif fc < 130:
        return 1
    else:
        return 2

df["atividade"] = df["batimento_cardiaco"].apply(atividade)


# =========================
# 4. Converter categorias
# =========================
df["tipo_do_animal"] = df["tipo_do_animal"].map({"cachorro": 0, "gato": 1})


# =========================
# 5. Separar X e y
# =========================

# ⚠️ TESTE MAIS INTELIGENTE (sem usar peso diretamente)
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

y = df["peso_ideal"]


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
# 9. Teste com novo animal
# =========================
novo_animal = [[0, 5, 1, 120, 2, 1]]  
# [tipo, idade, genero, batimento, porte, atividade]

pred = model.predict(novo_animal)
print("\nPeso ideal previsto para novo animal:", round(pred[0], 2))