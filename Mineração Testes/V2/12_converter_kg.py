import pandas as pd

# carregar base original
df = pd.read_csv(
    "dataset/synthetic_dog_breed_health_data.csv"
)

print("\nBASE ORIGINAL")
print(df.shape)

print("\nPREVIEW")
print(df.head())


# converter libras para kg
df["Weight (kg)"] = (
    df["Weight (lbs)"] * 0.453592
).round(2)


# remover coluna antiga em libras
df = df.drop(columns=["Weight (lbs)"])


# visualizar resultado
print("\nCOLUNAS APÓS CONVERSÃO")
print(df.columns)

print("\nPREVIEW COM KG")
print(
    df[
        [
            "Breed",
            "Breed Size",
            "Age",
            "Weight (kg)"
        ]
    ].head()
)


# estatísticas do peso em kg
print("\nESTATÍSTICAS DO PESO (kg)")
print(df["Weight (kg)"].describe())


# salvar nova base
df.to_csv(
    "dataset/dataset_kg.csv",
    index=False
)

print("\nBASE CONVERTIDA SALVA")
print("Arquivo: dataset/dataset_kg.csv")