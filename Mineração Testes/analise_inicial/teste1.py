import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# =========================
# 1. Carregar dados
# =========================
df = pd.read_csv("01_tabela_cachorros_gatos_regtest.csv", sep=";")

print(df.columns)

print("Preview dos dados:")
print(df.head())


# =========================
# 2. Criar peso ideal (TARGET)
# =========================
def calcular_peso_ideal(row):
    peso = row["peso"]
    
    if peso < 10:
        return peso * 1.1
    elif peso < 25:
        return peso * 0.95
    else:
        return peso * 0.9

df["peso_ideal"] = df.apply(calcular_peso_ideal, axis=1)


# =========================
# 3. Criar features novas
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
    if fc < 80:
        return 0  # baixo
    elif fc < 120:
        return 1  # médio
    else:
        return 2  # alto

df["atividade"] = df["batimento_cardiaco"].apply(atividade)


# =========================
# 4. Converter categorias
# =========================
df["tipo_do_animal"] = df["tipo_do_animal"].map({"cachorro": 0, "gato": 1})


# =========================
# 5. Separar X e y
# =========================
X = df[[
    "tipo_do_animal",
    "idade",
    "genero",
    "peso",
    "batimento_cardiaco",
    "porte",
    "atividade"
]]

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
model = RandomForestRegressor()
model.fit(X_train, y_train)


# =========================
# 8. Testar modelo
# =========================
predicoes = model.predict(X_test)

print("\nComparação (Previsto vs Real):")
for i in range(5):
    print(f"Previsto: {predicoes[i]:.2f} | Real: {y_test.values[i]:.2f}")