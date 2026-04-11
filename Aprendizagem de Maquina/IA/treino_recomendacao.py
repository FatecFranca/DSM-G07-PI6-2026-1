import pandas as pd
import json
import os

# Caminhos
PATH_BASES = 'Base de Dados'
PATH_DATASET = 'dataset_pronto_treino_V5.csv'
PATH_FOOD = os.path.join('pet-food-advice-api-main', 'db-food.json')

def treinar_recomendacao():
    # 1. Carregar Dados Tratados e Catálogo de Alimentos
    df_pet = pd.read_csv(PATH_DATASET)
    with open(PATH_FOOD, 'r', encoding='utf-8') as f:
        catalog = json.load(f)
    
    print(f"🤖 Iniciando Motor de Recomendação para {len(df_pet)} perfis...")

    # 2. Lógica de Recomendação (O "Cérebro" da IA)
    def recomendar(pet):
        recomendacoes = []
        
        for produto in catalog:
            # Regra 1: Bater o Porte (Small/Medium/Large)
            # Se o produto for para "All" ou bater com o porte do pet
            match_size = produto['animalSize'] == "All" or produto['animalSize'] == pet['animalSize']
            
            # Regra 2: Bater a Condição de Saúde
            # Se o pet não é saudável (Healthy == 'No') e o produto é para 'Overweight'
            match_condition = True
            if pet['Healthy'] == 'No' and produto['condition'] == 'Overweight':
                match_condition = True
            elif pet['Healthy'] == 'Yes' and produto['condition'] is None:
                match_condition = True
            else:
                match_condition = False

            if match_size and match_condition:
                recomendacoes.append(produto['name'])
        
        return recomendacoes[:2] # Retorna as 2 melhores opções

    # 3. Aplicando o "Treino" na base
    # Na prática, estamos gerando o resultado que a IA deve entregar
    df_pet['Recomendacao_IA'] = df_pet.apply(recomendar, axis=1)

    # 4. Salvar Resultado para Validação do PI
    df_pet[['Breed', 'animalWeight_kg', 'Healthy', 'Recomendacao_IA']].head(10).to_csv('resultado_recomendacao.csv', index=False)
    print("✅ Treinamento de lógica concluído! Resultado salvo em 'resultado_recomendacao.csv'")

if __name__ == "__main__":
    treinar_recomendacao()