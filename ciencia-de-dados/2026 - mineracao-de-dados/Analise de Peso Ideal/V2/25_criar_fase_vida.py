import pandas as pd


df = pd.read_csv(
    "dataset/dataset_corrigido_kg.csv"
)

print("\nBASE CARREGADA")
print(df.shape)




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



df.to_csv(
    "dataset/dataset_corrigido_kg_lifestage.csv",
    index=False
)

print("\nBASE SALVA")
print(
    "dataset/dataset_corrigido_kg_lifestage.csv"
)