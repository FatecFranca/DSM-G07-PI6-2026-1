import pandas as pd
import json
import os

# Definição dos caminhos das pastas e arquivos
PASTA_DATASETS = 'Datasets Tratados'
ARQUIVO_PETS = os.path.join(PASTA_DATASETS, 'dataset_petdex_final_PT.csv')
ARQUIVO_FOOD = os.path.join('pet-food-advice-api-main', 'db-food.json')

try:
    # 1. Carregar os dados e remover duplicatas
    if not os.path.exists(ARQUIVO_PETS):
        print(f"❌ Erro: O arquivo não foi encontrado em: {ARQUIVO_PETS}")
    else:
        df_pet = pd.read_csv(ARQUIVO_PETS, encoding='utf-8-sig')
        
        antes = len(df_pet)
        df_pet = df_pet.drop_duplicates()
        depois = len(df_pet)
        print(f"🧹 Limpeza: Removidas {antes - depois} linhas duplicadas da pasta '{PASTA_DATASETS}'.")

        # 2. Carregar o catálogo de rações (JSON)
        with open(ARQUIVO_FOOD, 'r', encoding='utf-8') as f:
            catalogo = json.load(f)

        # 3. Motor de Recomendação (Nomes Originais)
        def motor_ia(pet):
            sugestoes = []
            # Mapeamento interno apenas para busca no JSON
            mapa_porte = {'Pequeno': 'Small', 'Médio': 'Medium', 'Grande': 'Large'}
            porte_pet = mapa_porte.get(pet['porte_animal'], 'All')

            for produto in catalogo:
                # Match de Porte
                match_porte = produto['animalSize'] == "All" or produto['animalSize'] == porte_pet
                
                # Match de Saúde (Sim/Não do arquivo PT)
                if pet['Status_Saude'] == 'Não':
                    match_saude = produto['condition'] in ['Overweight', 'Weight Management', 'Digestive Care']
                else:
                    match_saude = produto['condition'] is None or produto['condition'] == "Everyday Health"

                if match_porte and match_saude:
                    # Adiciona o nome original do JSON
                    sugestoes.append(produto['name'])
            
            return ", ".join(sugestoes[:2]) if sugestoes else "Consulte um veterinário"

        # 4. Processar e Salvar
        print("🤖 Gerando recomendações para os 10.000 perfis...")
        df_pet['Sugestao_Racao'] = df_pet.apply(motor_ia, axis=1)
        
        # Colunas conforme o seu modelo
        colunas_finais = ['Raca', 'peso_kg', 'Status_Saude', 'Sugestao_Racao']
        df_resultado = df_pet[colunas_finais]

        df_resultado.to_csv('resultado_petdex_completo.csv', index=False, encoding='utf-8-sig')
        print(f"✅ Sucesso! Gerado 'resultado_petdex_completo.csv' com {len(df_resultado)} registros únicos.")

except Exception as e:
    print(f"❌ Erve técnico: {e}")