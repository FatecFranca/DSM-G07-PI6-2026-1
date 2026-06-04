import pandas as pd

# 1. CARREGAR BASE

df = pd.read_csv("dataset/synthetic_dog_breed_health_data.csv")

print("\n===== BASE ORIGINAL =====")
print("Linhas e colunas:", df.shape)

# 2. FILTRAR APENAS ANIMAIS SAUDÁVEIS

df = df[df["Healthy"] == "Yes"]

print("\n===== APÓS FILTRAR ANIMAIS SAUDÁVEIS =====")
print("Linhas e colunas:", df.shape)

# 3. REMOVER COLUNAS IRRELEVANTES

colunas_remover = [
    "ID",
    "Synthetic",
    "Healthy",
    "Food Brand",
    "Diet",
    "Medications"
]

df = df.drop(columns=colunas_remover)

print("\n===== COLUNAS MANTIDAS =====")
print(df.columns)

# 4. VERIFICAR NULOS

print("\n===== VALORES NULOS ANTES =====")
print(df.isnull().sum())

# 5. TRATAMENTO DOS NULOS


# Separar colunas numéricas e categóricas
colunas_numericas = df.select_dtypes(include=["float64", "int64"]).columns
colunas_categoricas = df.select_dtypes(include=["object"]).columns


# 5.1 Preencher numéricas com MEDIANA

for coluna in colunas_numericas:
    mediana = df[coluna].median()
    df[coluna] = df[coluna].fillna(mediana)


# 5.2 Preencher categóricas com MODA


for coluna in colunas_categoricas:
    moda = df[coluna].mode()[0]
    df[coluna] = df[coluna].fillna(moda)


# 6. VERIFICAÇÃO FINAL


print("\n===== VALORES NULOS DEPOIS =====")
print(df.isnull().sum())

print("\n===== TAMANHO FINAL =====")
print(df.shape)

print("\n===== PREVIEW FINAL =====")
print(df.head())


# 7. SALVAR BASE TRATADA

df.to_csv("dataset/dataset_tratado.csv", index=False)

print("\n===== BASE TRATADA SALVA =====")
print("Arquivo: dataset/dataset_tratado.csv")