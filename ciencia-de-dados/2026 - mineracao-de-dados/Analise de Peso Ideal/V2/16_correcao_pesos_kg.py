import pandas as pd
import numpy as np


# carregar base
df = pd.read_csv(
    "dataset/dataset_sem_nulos_kg.csv"
)

print("\nBASE CARREGADA")
print(df.shape)


# faixas de peso por raça (kg)
faixas_peso = {

    "Chihuahua": (1.0, 4.0),
    "Yorkshire Terrier": (2.0, 5.0),
    "Dachshund": (4.0, 9.0),
    "Beagle": (9.0, 16.0),
    "Poodle": (6.0, 32.0),

    "Bulldog": (18.0, 25.0),
    "Boxer": (25.0, 36.0),
    "Australian Shepherd": (18.0, 32.0),
    "Siberian Husky": (16.0, 27.0),

    "Golden Retriever": (25.0, 34.0),
    "Labrador Retriever": (25.0, 36.0),
    "German Shepherd": (22.0, 40.0),
    "Doberman": (27.0, 45.0),
    "Rottweiler": (35.0, 60.0),

    "Great Dane": (45.0, 82.0)
}


# contador
correcoes = 0


# corrigir pesos inconsistentes
for raca, (peso_min, peso_max) in faixas_peso.items():

    filtro = df["Breed"] == raca

    pesos_invalidos = (
        (df["Weight (kg)"] < peso_min) |
        (df["Weight (kg)"] > peso_max)
    )

    indices = df[filtro & pesos_invalidos].index

    for idx in indices:

        novo_peso = round(
            np.random.uniform(
                peso_min,
                peso_max
            ),
            2
        )

        df.loc[idx, "Weight (kg)"] = novo_peso

        correcoes += 1


print("\nTOTAL DE PESOS CORRIGIDOS")
print(correcoes)


# estatísticas finais
print("\nNOVA DISTRIBUIÇÃO POR RAÇA")

estatisticas = df.groupby(
    "Breed"
)["Weight (kg)"].agg([
    "mean",
    "min",
    "max"
])

print(estatisticas)


# salvar nova base
df.to_csv(
    "dataset/dataset_corrigido_kg.csv",
    index=False
)

print("\nBASE CORRIGIDA SALVA")
print("Arquivo: dataset/dataset_corrigido_kg.csv")