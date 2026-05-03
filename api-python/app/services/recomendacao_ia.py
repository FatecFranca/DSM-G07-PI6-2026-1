import json
import os

PESO_IDEAL_RACA = {
    'Australian Shepherd': 23.0, 'Golden Retriever': 30.0, 'Labrador Retriever': 32.0,
    'Poodle': 20.0, 'Siberian Husky': 22.0, 'Dachshund': 10.0, 'Chihuahua': 3.0,
    'Boxer': 28.0, 'Bulldog': 20.0, 'German Shepherd': 35.0, 'Rottweiler': 45.0,
    'Beagle': 12.0, 'Yorkshire Terrier': 4.0
}

def carregar_catalogo():
    path_food = os.path.join('pet-food-advice-api-main', 'db-food.json')
    if os.path.exists(path_food):
        with open(path_food, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def gerar_sugestao_nutricional(dados_animal):
    """
    Recebe os dados do animal vindos da API Java e retorna a recomendação da IA.
    """
    raca = dados_animal.get("raca", "SRD (Sem Raça Definida)")
    peso_atual = dados_animal.get("peso", 0)
    # Tenta pegar o porte do JSON, se não tiver, calcula pelo peso
    porte_pet_original = dados_animal.get("porte", "Médio") 
    
    # 1. Definir Peso Ideal (Lógica SRD por Porte)
    if raca == 'SRD (Sem Raça Definida)':
        if porte_pet_original == 'Pequeno': peso_ref = 7.0
        elif porte_pet_original == 'Médio': peso_ref = 15.0
        else: peso_ref = 30.0
    else:
        peso_ref = PESO_IDEAL_RACA.get(raca, 20.0)

    # 2. Diagnóstico Corporal
    if peso_atual > (peso_ref * 1.15):
        status_corpo = 'Sobrepeso'
    elif peso_atual < (peso_ref * 0.85):
        status_corpo = 'Abaixo do Peso'
    else:
        status_corpo = 'Peso Ideal'

    # 3. Match com o Catálogo
    catalogo = carregar_catalogo()
    sugestoes = []
    mapa_porte = {'Pequeno': 'Small', 'Médio': 'Medium', 'Grande': 'Large'}
    porte_busca = mapa_porte.get(porte_pet_original, 'All')

    for produto in catalogo:
        match_porte = produto['animalSize'] == "All" or produto['animalSize'] == porte_busca
        
        if status_corpo == 'Sobrepeso':
            match_nutricao = produto['condition'] in ['Overweight', 'Weight Management']
        elif status_corpo == 'Abaixo do Peso':
            match_nutricao = produto['condition'] is None or "Puppy" in produto['name']
        else:
            match_nutricao = produto['condition'] in [None, 'Everyday Health']

        if match_porte and match_nutricao:
            sugestoes.append(produto['name'])

    return {
        "status_corporal": status_corpo,
        "peso_referencia": peso_ref,
        "recomendacoes": sugestoes[:2] # Retorna as 2 melhores
    }