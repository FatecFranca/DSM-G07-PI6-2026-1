import pandas as pd
import joblib

# ==========================
# CARREGAR MODELOS
# ==========================

modelo_com_raca = joblib.load(
    "modelo_com_raca.pkl"
)

modelo_srd = joblib.load(
    "modelo_srd.pkl"
)

print("\nMODELOS CARREGADOS")

# ==========================
# CARREGAR FAIXAS
# ==========================

faixas_raca = pd.read_csv(
    "faixas_por_raca.csv"
)

faixas_porte = pd.read_csv(
    "faixas_por_porte.csv"
)

print("FAIXAS CARREGADAS")

# =====================================================
# EXEMPLO 1 - CÃO COM RAÇA
# =====================================================

pet_raca = pd.DataFrame([{
    "Breed": "Labrador Retriever",
    "Breed Size": "Large",
    "Sex": "Male",
    "Age": 5,
    "Spay/Neuter Status": "Neutered",
    "Daily Activity Level": "High",
    "Daily Walk Distance (miles)": 3,
    "Hours of Sleep": 10,
    "Play Time (hrs)": 2,
    "Annual Vet Visits": 1,
    "Life Stage": "Adult"
}])

peso_ideal = float(
    modelo_com_raca.predict(pet_raca)[0]
)

faixa = faixas_raca[
    faixas_raca["Breed"] == "Labrador Retriever"
].iloc[0]

resultado = {
    "peso_ideal": round(peso_ideal, 2),
    "peso_atual": 33.0,
    "peso_minimo": float(faixa["P10"]),
    "peso_maximo": float(faixa["P90"])
}

print("\nRESULTADO COM RAÇA")
print(resultado)

# =====================================================
# EXEMPLO 2 - SRD
# =====================================================

pet_srd = pd.DataFrame([{
    "Breed Size": "Medium",
    "Sex": "Male",
    "Spay/Neuter Status": "Neutered",
    "Age": 5
}])

peso_ideal = float(
    modelo_srd.predict(pet_srd)[0]
)

faixa = faixas_porte[
    faixas_porte["Breed Size"] == "Medium"
].iloc[0]

resultado = {
    "peso_ideal": round(peso_ideal, 2),
    "peso_atual": 20.0,
    "peso_minimo": float(faixa["P10"]),
    "peso_maximo": float(faixa["P90"])
}

print("\nRESULTADO SRD")
print(resultado)