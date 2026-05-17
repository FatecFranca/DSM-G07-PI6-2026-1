import json
import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime, timezone
import math

# Caminho absoluto para a pasta onde salvamos os artefatos da IA
PASTA_MODELOS = os.path.join(os.path.dirname(__file__), '..', 'modelos_ia')

def carregar_arquivos_ia():
    try:
        modelo = joblib.load(os.path.join(PASTA_MODELOS, 'modelo_xgboost_otimizado.pkl'))
        encoders = joblib.load(os.path.join(PASTA_MODELOS, 'label_encoders.pkl'))
        with open(os.path.join(PASTA_MODELOS, 'db-food.json'), 'r', encoding='utf-8') as f:
            catalogo = json.load(f)
        return modelo, encoders, catalogo
    except Exception as e:
        print(f"Erro ao carregar arquivos da IA: {e}")
        return None, None, []

def calcular_idade(data_nascimento_str):
    if not data_nascimento_str:
        return 2 # Idade padrão
    try:
        data_nascimento = datetime.fromisoformat(data_nascimento_str.replace("Z", "+00:00"))
        if data_nascimento.tzinfo is None:
            data_nascimento = data_nascimento.replace(tzinfo=timezone.utc)
        hoje = datetime.now(timezone.utc)
        anos = (hoje - data_nascimento).total_seconds() / (86400.0 * 365.2425)
        return max(1, int(math.floor(anos + 0.5)))
    except:
        return 2

def gerar_sugestao_nutricional(dados_animal):
    """
    Usa o modelo de Machine Learning (XGBoost) para prever a Marca da Ração.
    """
    modelo, encoders, catalogo = carregar_arquivos_ia()
    
    # Validações e extrações básicas
    raca = dados_animal.get("racaNome", "SRD (Sem Raça Definida)")
    peso_kg = float(dados_animal.get("peso") or 10.0)
    idade = calcular_idade(dados_animal.get("dataNascimento"))
    
    # 1. PREPARANDO AS 4 FEATURES QUE A IA SELECIONOU:
    # ['Idade', 'peso_kg', 'caminhada_diaria_km', 'calorias_diarias_RER']
    caminhada_diaria_km = 1.6 # Valor médio (já que a API não informa isso diretamente)
    calorias_diarias_RER = round(70 * (peso_kg ** 0.75), 2)
    
    # Criar dataframe para a inferência
    X_infer = pd.DataFrame([{
        'Idade': idade,
        'peso_kg': peso_kg,
        'caminhada_diaria_km': caminhada_diaria_km,
        'calorias_diarias_RER': calorias_diarias_RER
    }])

    # 2. INFERÊNCIA DO MODELO DE ML
    marca_prevista_nome = "Royal Canin" # Fallback
    try:
        if modelo and encoders:
            predicao_num = modelo.predict(X_infer)[0]
            # Usar o LabelEncoder para descobrir o nome da marca a partir do número
            le_marca = encoders['Marca_Racao']
            marca_prevista_nome = le_marca.inverse_transform([predicao_num])[0]
    except Exception as e:
        print(f"Erro na inferência do XGBoost: {e}")

    # 3. MATCH COM O DB-FOOD.JSON BASEADO NA MARCA PREVISTA E PORTE DO CÃO
    porte_pet_original = dados_animal.get("porte", "Médio") 
    mapa_porte = {'Pequeno': 'Small', 'Médio': 'Medium', 'Grande': 'Large'}
    porte_busca = mapa_porte.get(porte_pet_original, 'All')

    sugestoes = []
    for produto in catalogo:
        # Pega as marcas e portes iguais
        match_marca = (produto.get('brand') == marca_prevista_nome)
        match_porte = (produto.get('animalSize') == "All" or produto.get('animalSize') == porte_busca)
        
        if match_marca and match_porte:
            sugestoes.append(produto['name'])

    # Se não achou com a marca exata para o porte, tenta só a marca
    if not sugestoes:
        for produto in catalogo:
            if produto.get('brand') == marca_prevista_nome:
                sugestoes.append(produto['name'])
    
    # Último fallback se o catálogo estiver vazio
    if not sugestoes:
        sugestoes = [f"Ração recomendada da marca {marca_prevista_nome}"]

    return {
        "status_corporal": "Análise por IA Concluída",
        "peso_referencia": peso_kg, # Não usamos mais peso_referencia heurístico
        "recomendacoes": sugestoes[:2],
        "marca_prevista": marca_prevista_nome
    }