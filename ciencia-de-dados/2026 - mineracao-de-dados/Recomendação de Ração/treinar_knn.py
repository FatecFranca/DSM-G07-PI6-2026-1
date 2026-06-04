import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

print("[INFO] Iniciando o treinamento do modelo KNN para recomendação de marca de ração...")

# 1. Definir caminhos
diretorio_atual = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else r"c:\petdex\Aprendizagem de Maquina\IA"
caminho_dados = os.path.join(diretorio_atual, 'Datasets Tratados', 'dataset_completo_corrigido_kg.csv')

if not os.path.exists(caminho_dados):
    # Tentar caminho alternativo absoluto
    caminho_dados = r"c:\petdex\Aprendizagem de Maquina\IA\Datasets Tratados\dataset_completo_corrigido_kg.csv"

if not os.path.exists(caminho_dados):
    raise FileNotFoundError(f"Arquivo não encontrado: {caminho_dados}")

# 2. Carregar dados
df = pd.read_csv(caminho_dados)
print(f"[INFO] Registros lidos: {len(df)}")

# Filtrar registros válidos
df_clean = df[df['Food Brand'] != 'Unknown'].copy()
print(f"[INFO] Registros limpos para treinamento (sem 'Unknown'): {len(df_clean)}")

# 3. Preparar Features e Target
# Calcular calorias RER baseadas no peso real
df_clean['calorias_diarias_RER'] = 70 * (df_clean['Weight (kg)'] ** 0.75)
# Converter caminhada de milhas para km
df_clean['caminhada_diaria_km'] = df_clean['Daily Walk Distance (miles)'] * 1.60934

features = ['Age', 'Weight (kg)', 'caminhada_diaria_km', 'calorias_diarias_RER']
X = df_clean[features]
y = df_clean['Food Brand']

# 4. Encoders e Normalização
le_brand = LabelEncoder()
y_encoded = le_brand.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

# StandardScaler para normalização dos dados (essencial para KNN)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Treinar KNN (k=21)
# k=21 foi escolhido por balancear boa acurácia e evitar a predição exclusiva da classe majoritária.
k_vizinhos = 21
modelo_knn = KNeighborsClassifier(n_neighbors=k_vizinhos)
modelo_knn.fit(X_train_scaled, y_train)

# 6. Avaliar modelo
y_pred = modelo_knn.predict(X_test_scaled)
acuracia = accuracy_score(y_test, y_pred)
print(f"\n[MÉTRICAS DO MODELO KNN (k={k_vizinhos})]")
print(f"Taxa de Acerto (Acurácia): {acuracia:.4f} ({acuracia * 100:.2f}%)")
print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred, target_names=le_brand.classes_, zero_division=0))

# 7. Salvar artefatos
diretorio_modelos_gerados = os.path.join(diretorio_atual, 'Modelos Gerados')
os.makedirs(diretorio_modelos_gerados, exist_ok=True)

# Salvar no diretório de modelagem
joblib.dump(modelo_knn, os.path.join(diretorio_modelos_gerados, 'modelo_knn_racao.pkl'))
joblib.dump(scaler, os.path.join(diretorio_modelos_gerados, 'scaler_knn_brand.pkl'))

# Também vamos atualizar o dicionário de label encoders para conter o novo encoder da marca de ração
encoders_path_original = r"c:\petdex\api-python\app\modelos_ia\label_encoders.pkl"
if os.path.exists(encoders_path_original):
    try:
        encoders = joblib.load(encoders_path_original)
    except Exception:
        encoders = {}
else:
    encoders = {}

# Atualizar o encoder de Marca_Racao no dict global
encoders['Marca_Racao'] = le_brand
joblib.dump(encoders, os.path.join(diretorio_modelos_gerados, 'label_encoders.pkl'))

print(f"\n[INFO] Artefatos salvos em: {diretorio_modelos_gerados}")

# Copiar automaticamente para a pasta da API Python
caminho_api_modelos = r"c:\petdex\api-python\app\modelos_ia"
if os.path.exists(caminho_api_modelos):
    joblib.dump(modelo_knn, os.path.join(caminho_api_modelos, 'modelo_knn_racao.pkl'))
    joblib.dump(scaler, os.path.join(caminho_api_modelos, 'scaler_knn_brand.pkl'))
    joblib.dump(encoders, os.path.join(caminho_api_modelos, 'label_encoders.pkl'))
    print(f"[INFO] Artefatos copiados com sucesso para a API Python em: {caminho_api_modelos}")
else:
    print("[WARN] Pasta de destino da API Python não encontrada. Lembre-se de copiar os arquivos manualmente.")
