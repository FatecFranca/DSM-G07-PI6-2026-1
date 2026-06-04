import pandas as pd
import numpy as np

# carregar base em kg
df = pd.read_csv(
    "dataset/dataset_kg.csv"
)

print("\nBASE ORIGINAL")
print(df.shape)




# tratar colunas categóricas
categoricas = df.select_dtypes(
    include=["object"]
).columns

for coluna in categoricas:
    df[coluna] = df[coluna].fillna(
        "Unknown"
    )


# tratar colunas numéricas
numericas = df.select_dtypes(
    exclude=["object"]
).columns

for coluna in numericas:
    mediana = df[coluna].median()

    df[coluna] = df[coluna].fillna(
        mediana
    )


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


correcoes = 0

for raca, (peso_min, peso_max) in faixas_peso.items():

    filtro_raca = df["Breed"] == raca

    filtro_peso = (
        (df["Weight (kg)"] < peso_min)
        |
        (df["Weight (kg)"] > peso_max)
    )

    indices = df[
        filtro_raca & filtro_peso
    ].index

    for idx in indices:

        df.loc[idx, "Weight (kg)"] = round(
            np.random.uniform(
                peso_min,
                peso_max
            ),
            2
        )

        correcoes += 1


print("\nTOTAL DE PESOS CORRIGIDOS")
print(correcoes)

print("\nVALORES NULOS FINAIS")
print(df.isnull().sum())

print("\nBASE FINAL")
print(df.shape)

print("\nPREVIEW")
print(df.head())


# salvar
df.to_csv(
    "dataset/dataset_completo_corrigido_kg.csv",
    index=False
)

print("\nBASE SALVA")
print(
    "Arquivo: dataset/dataset_completo_corrigido_kg.csv"
)