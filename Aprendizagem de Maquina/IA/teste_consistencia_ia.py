import pandas as pd
import json
import os

# Caminhos dos arquivos
PATH_OTIMIZADO = os.path.join('Datasets Otimizados', 'base_ia_otimizada.csv')
PATH_FOOD = os.path.join('pet-food-advice-api-main', 'db-food.json')

def executar_teste_consistencia():
    try:
        # 1. Carregar a base que sofreu a Seleção de Atributos
        df_ia = pd.read_csv(PATH_OTIMIZADO)
        
        # 2. Carregar o catálogo de alimentos
        with open(PATH_FOOD, 'r', encoding='utf-8') as f:
            catalogo = json.load(f)

        # 3. Função de Recomendação (Lógica que já validamos)
        def motor_ia(pet):
            sugestoes = []
            mapa_porte = {'Pequeno': 'Small', 'Médio': 'Medium', 'Grande': 'Large'}
            porte_pet = mapa_porte.get(pet['porte_animal'], 'All')

            for produto in catalogo:
                # Filtro de Porte
                match_porte = produto['animalSize'] == "All" or produto['animalSize'] == porte_pet
                
                # Filtro de Saúde
                if pet['Status_Saude'] == 'Não':
                    match_saude = produto['condition'] in ['Overweight', 'Weight Management', 'Digestive Care']
                else:
                    match_saude = produto['condition'] is None or produto['condition'] == "Everyday Health"

                if match_porte and match_saude:
                    sugestoes.append(produto['name'])
            
            return ", ".join(sugestoes[:2]) if sugestoes else "Consulte um veterinário"

        # 4. Gerar recomendações com a base "enxuta"
        print("🧪 Executando teste de consistência na base otimizada...")
        df_ia['Sugestao_Otimizada'] = df_ia.apply(motor_ia, axis=1)

        # 5. Validação visual dos primeiros registros
        print("\n✅ RESULTADO DO TESTE (Amostra):")
        print(df_ia[['Raca', 'Status_Saude', 'Sugestao_Otimizada']].head(5))

        # 6. Salvar para comparação final
        pasta_recomendacao = 'Recomendação'
        if not os.path.exists(pasta_recomendacao):
            os.makedirs(pasta_recomendacao)
            
        df_ia.to_csv(os.path.join(pasta_recomendacao, 'validacao_consistencia.csv'), index=False, encoding='utf-8-sig')
        
        print(f"\n🚀 Teste concluído! O arquivo de validação foi salvo em: {pasta_recomendacao}")

    except Exception as e:
        print(f"❌ Erro no teste: {e}")

if __name__ == "__main__":
    executar_teste_consistencia()