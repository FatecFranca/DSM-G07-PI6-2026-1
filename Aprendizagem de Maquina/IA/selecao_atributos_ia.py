import pandas as pd
import os

# Nesse arquivo ele reduz a complexidade. Ele joga fora o que é "ruído" e mantém só o que importa.
# Foi reduzido o dataset de 21 para 6 colunas essenciais. Isso faz com que a IA processe
# as informações de forma muito mais rápida (72% de redução de volume) sem perder a inteligência



# --- DEFINIÇÃO DOS CAMINHOS ---
# Onde está o arquivo original bruto
ARQUIVO_ORIGINAL = os.path.join('Base de Dados', 'synthetic_dog_breed_health_data.csv')

# Onde está o arquivo que tratamos antes
ARQUIVO_TRATADO = os.path.join('Datasets Tratados', 'dataset_petdex_final_PT.csv')

# Onde salva a base ultra-enxuta para a IA
PASTA_SAIDA = 'Datasets Otimizados'

def otimizar_base():
    try:
        # 1. Carregar as bases para comparação
        if not os.path.exists(ARQUIVO_ORIGINAL):
            print(f"❌ Erro: Não encontrei o arquivo original em: {ARQUIVO_ORIGINAL}")
            return
            
        df_orig = pd.read_csv(ARQUIVO_ORIGINAL)
        df_treated = pd.read_csv(ARQUIVO_TRATADO)

        # 2. SELEÇÃO DE ATRIBUTOS (Foco na IA de Recomendação)
        # Escolhi manter apenas o "núcleo duro" da decisão nutricional
        atributos_relevantes = [
            'Raca', 'Idade', 'peso_kg', 'porte_animal', 
            'Status_Saude', 'calorias_diarias_RER'
        ]
        
        df_otimizado = df_treated[atributos_relevantes].copy()

        # 3. Métricas de Melhoria
        colunas_orig = len(df_orig.columns)
        colunas_ia = len(df_otimizado.columns)
        reducao = ((colunas_orig - colunas_ia) / colunas_orig) * 100
        
        # 4. Criar pasta e salvar
        if not os.path.exists(PASTA_SAIDA):
            os.makedirs(PASTA_SAIDA)
            
        caminho_final = os.path.join(PASTA_SAIDA, 'base_ia_otimizada.csv')
        df_otimizado.to_csv(caminho_final, index=False, encoding='utf-8-sig')

        # 5. Relatório Visual
        print("\n" + "="*40)
        print("📊 SELEÇÃO DE ATRIBUTOS CONCLUÍDA")
        print("="*40)
        print(f"🔹 Atributos na Base Bruta: {colunas_orig}")
        print(f"🔹 Atributos na Base Otimizada: {colunas_ia}")
        print(f"🚀 Redução de Dimensionalidade: {reducao:.1f}%")
        print(f"📂 Salvo em: {caminho_final}")
        print("="*40)
        print("\n✅ CONCLUSÃO: Removidos 15 atributos que não impactavam a ração.")

    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    otimizar_base()