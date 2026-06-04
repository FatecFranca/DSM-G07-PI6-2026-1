import pandas as pd


df = pd.read_csv(
    "dataset/dataset_corrigido_kg.csv"
)

print("\nBASE CARREGADA")
print(df.shape)


df = df[
    df["Breed Size"] != "Unknown"
]

print("\nAPÓS REMOVER UNKNOWN")
print(df.shape)


# CALCULAR PERCENTIS


faixas = (
    df.groupby("Breed Size")["Weight (kg)"]
    .agg(
        P10=lambda x: x.quantile(0.10),
        P90=lambda x: x.quantile(0.90),
        Media="mean",
        Quantidade="count"
    )
    .reset_index()
)

# ARREDONDAR


faixas["P10"] = faixas["P10"].round(2)
faixas["P90"] = faixas["P90"].round(2)
faixas["Media"] = faixas["Media"].round(2)


print("\nFAIXAS POR PORTE")
print(faixas)

faixas.to_csv(
    "faixas_por_porte.csv",
    index=False
)

print("\nARQUIVO SALVO")
print("faixas_por_porte.csv")