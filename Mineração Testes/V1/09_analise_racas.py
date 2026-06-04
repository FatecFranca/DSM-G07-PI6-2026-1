import pandas as pd

# carregar base
df = pd.read_csv("dataset/dataset_sem_outliers.csv")

print("\nBASE CARREGADA")
print(df.shape)

# analisar pesos por raça
analise = df.groupby("Breed")["Weight (lbs)"].agg([
    "count",
    "mean",
    "std",
    "min",
    "max"
])

# ordenar pela quantidade
analise = analise.sort_values(by="count", ascending=False)

print("\nANÁLISE POR RAÇA")
print(analise)

# salvar análise
analise.to_csv(
    "analise_peso_por_raca.csv"
)

print("\nArquivo salvo:")
print("analise_peso_por_raca.csv")