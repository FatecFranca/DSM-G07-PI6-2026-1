import pandas as pd
import random

# carregar base
df = pd.read_csv("dataset/dataset_sem_outliers.csv")

print("\nBASE ORIGINAL")
print(df.shape)


# faixas realistas de peso por raça (lbs)
faixas_peso = {

    "Chihuahua": (2, 8),
    "Yorkshire Terrier": (4, 10),
    "Dachshund": (8, 20),
    "Beagle": (20, 35),
    "Poodle": (10, 70),

    "Bulldog": (40, 55),
    "Boxer": (50, 80),
    "Australian Shepherd": (40, 65),

    "Golden Retriever": (55, 75),
    "Labrador Retriever": (55, 80),
    "German Shepherd": (50, 90),
    "Siberian Husky": (35, 65),
    "Doberman": (60, 100),
    "Rottweiler": (80, 130),
    "Great Dane": (100, 180)
}


# contador de correções
correcoes = 0


# corrigir pesos incoerentes
for index, row in df.iterrows():

    raca = row["Breed"]
    peso = row["Weight (lbs)"]

    # verificar se a raça existe nas regras
    if raca in faixas_peso:

        minimo, maximo = faixas_peso[raca]

        # peso incoerente
        if peso < minimo or peso > maximo:

            novo_peso = round(
                random.uniform(minimo, maximo),
                1
            )

            df.at[index, "Weight (lbs)"] = novo_peso

            correcoes += 1


print("\nTOTAL DE PESOS CORRIGIDOS")
print(correcoes)


# estatísticas novas
print("\nNOVA DISTRIBUIÇÃO POR RAÇA")

analise = df.groupby("Breed")["Weight (lbs)"].agg([
    "mean",
    "min",
    "max"
])

print(analise)


# salvar nova base
df.to_csv(
    "dataset/dataset_corrigido.csv",
    index=False
)

print("\nBASE CORRIGIDA SALVA")
print("Arquivo: dataset/dataset_corrigido.csv")