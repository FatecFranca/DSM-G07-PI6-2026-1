import pandas as pd


# ==========================
# CARREGAR BASE
# ==========================

df = pd.read_csv(
    "dataset/dataset_corrigido_kg.csv"
)

print("\nBASE CARREGADA")
print(df.shape)


# ==========================
# CRIAR FASE DA VIDA
# ==========================

def classificar_fase(idade):

    if idade < 2:
        return "Puppy"

    elif idade < 5:
        return "Young Adult"

    elif idade < 8:
        return "Adult"

    else:
        return "Senior"


df["Life Stage"] = df["Age"].apply(
    classificar_fase
)


# ==========================
# DISTRIBUIÇÃO
# ==========================

print("\nDISTRIBUIÇÃO DAS FASES")

print(
    df["Life Stage"]
    .value_counts()
)

print("\nPREVIEW")

print(
    df[
        [
            "Age",
            "Life Stage"
        ]
    ]
    .head(20)
)


# ==========================
# SALVAR
# ==========================

df.to_csv(
    "dataset/dataset_corrigido_kg_lifestage.csv",
    index=False
)

print("\nBASE SALVA")
print(
    "dataset/dataset_corrigido_kg_lifestage.csv"
)