import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression



df = pd.read_csv(
    "dataset/dataset_corrigido_kg.csv"
)

print("\nBASE CARREGADA")
print(df.shape)


y = df["Weight (kg)"]

X = df.drop(
    columns=["Weight (kg)"]
)



categoricas = X.select_dtypes(
    include=["object"]
).columns.tolist()

preprocessador = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categoricas
        )
    ],
    remainder="passthrough"
)



X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

modelo = Pipeline([
    ("prep", preprocessador),
    ("modelo", LinearRegression())
])

modelo.fit(
    X_train,
    y_train
)

print("\nMODELO TREINADO")




casos_teste = pd.DataFrame([

    # SRD PEQUENO
    {
        "Breed": "Unknown",
        "Breed Size": "Small",
        "Sex": "Male",
        "Age": 3,
        "Spay/Neuter Status": "Neutered",
        "Daily Activity Level": "Active",
        "Daily Walk Distance (miles)": 1,
        "Hours of Sleep": 10,
        "Play Time (hrs)": 2,
        "Annual Vet Visits": 1
    },

    # SRD MÉDIO
    {
        "Breed": "Unknown",
        "Breed Size": "Medium",
        "Sex": "Male",
        "Age": 3,
        "Spay/Neuter Status": "Neutered",
        "Daily Activity Level": "Active",
        "Daily Walk Distance (miles)": 2,
        "Hours of Sleep": 10,
        "Play Time (hrs)": 2,
        "Annual Vet Visits": 1
    },

    # SRD GRANDE
    {
        "Breed": "Unknown",
        "Breed Size": "Large",
        "Sex": "Male",
        "Age": 3,
        "Spay/Neuter Status": "Neutered",
        "Daily Activity Level": "Active",
        "Daily Walk Distance (miles)": 3,
        "Hours of Sleep": 10,
        "Play Time (hrs)": 2,
        "Annual Vet Visits": 1
    }

])



previsoes = modelo.predict(
    casos_teste
)

print("\nRESULTADOS SRD")

for i, peso in enumerate(previsoes):

    print(
        f"SRD {i + 1}: "
        f"{peso:.2f} kg"
    )