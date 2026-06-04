import pandas as pd

# Carregar base tratada
df = pd.read_csv("dataset/dataset_tratado.csv")

print("\nBASE ORIGINAL")
print(df.shape)

# Mostrar estatísticas por porte
print("\nESTATÍSTICAS POR PORTE")
print(
    df.groupby("Breed Size")["Weight (lbs)"].describe()
)

# Lista para armazenar dataframes limpos
bases_filtradas = []

# Separar por porte
portes = df["Breed Size"].unique()

for porte in portes:

    df_porte = df[df["Breed Size"] == porte]

    # Q1 e Q3
    q1 = df_porte["Weight (lbs)"].quantile(0.25)
    q3 = df_porte["Weight (lbs)"].quantile(0.75)

    # IQR
    iqr = q3 - q1

    # Limites
    limite_inferior = q1 - (1.5 * iqr)
    limite_superior = q3 + (1.5 * iqr)

    print(f"\nPORTE: {porte}")
    print(f"Limite inferior: {limite_inferior:.2f}")
    print(f"Limite superior: {limite_superior:.2f}")

    # Remover outliers
    df_filtrado = df_porte[
        (df_porte["Weight (lbs)"] >= limite_inferior)
        &
        (df_porte["Weight (lbs)"] <= limite_superior)
    ]

    removidos = len(df_porte) - len(df_filtrado)

    print(f"Registros removidos: {removidos}")

    bases_filtradas.append(df_filtrado)

# Juntar tudo novamente
df_final = pd.concat(bases_filtradas)

print("\nBASE FINAL")
print(df_final.shape)

# Salvar nova base
df_final.to_csv(
    "dataset/dataset_sem_outliers.csv",
    index=False
)

print("\nNova base salva:")
print("dataset/dataset_sem_outliers.csv")