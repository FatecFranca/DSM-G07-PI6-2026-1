import pandas as pd
import os

PATH_BASES = 'Base de Dados'

try:
    df = pd.read_csv(os.path.join(PATH_BASES, 'synthetic_dog_breed_health_data.csv'))

    # --- 1. LIMPEZA E PREENCHIMENTO ---
    df['Breed'] = df['Breed'].fillna('SRD (Sem Raça Definida)')
    
    num_cols = ['Age', 'Weight (lbs)', 'Daily Walk Distance (miles)', 'Hours of Sleep', 'Play Time (hrs)', 'Annual Vet Visits']
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())

    cat_cols = ['Sex', 'Diet', 'Food Brand', 'Medications', 'Seizures', 'Daily Activity Level', 'Healthy']
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # --- 2. TRADUÇÃO DO CONTEÚDO (LINHAS) ---
    
    # Dicionário de traduções gerais
    traducoes = {
        'Sex': {'Male': 'Macho', 'Female': 'Fêmea'},
        'Healthy': {'Yes': 'Sim', 'No': 'Não'},
        'Medications': {'Yes': 'Sim', 'No': 'Não'},
        'Seizures': {'Yes': 'Sim', 'No': 'Não'},
        'Daily Activity Level': {
            'None': 'Nenhum', 
            'Low': 'Baixo', 
            'Moderate': 'Moderado', 
            'Active': 'Ativo', 
            'Very Active': 'Muito Ativo'
        },
        'Diet': {
            'Wet food': 'Úmida', 
            'Hard food': 'Ração Seca', 
            'Home cooked': 'Caseira', 
            'Special diet': 'Especial'
        }
    }

    for coluna, mapa in traducoes.items():
        df[coluna] = df[coluna].map(mapa).fillna(df[coluna])

    # --- 3. ENGENHARIA E CONVERSÕES ---
    df['peso_kg'] = (df['Weight (lbs)'] * 0.453592).round(2)
    df['caminhada_diaria_km'] = (df['Daily Walk Distance (miles)'] * 1.60934).round(2)
    
    def get_size(w):
        if w <= 10: return 'Pequeno'
        elif w <= 25: return 'Médio'
        else: return 'Grande'
    df['porte_animal'] = df['peso_kg'].apply(get_size)
    
    df['calorias_diarias_RER'] = (70 * (df['peso_kg'] ** 0.75)).round(2)

    # --- 4. RENOMEAÇÃO E SELEÇÃO (Removendo Nivel_Atividade_Dono) ---
    mapeamento_colunas = {
        'Breed': 'Raca',
        'Sex': 'Sexo',
        'Age': 'Idade',
        'Diet': 'Dieta_Atual',
        'Food Brand': 'Marca_Racao',
        'Medications': 'Medicamentos',
        'Seizures': 'Convulsoes',
        'Hours of Sleep': 'Horas_Sono',
        'Play Time (hrs)': 'Tempo_Brincadeira_Horas',
        'Daily Activity Level': 'Nivel_Atividade_Pet',
        'Annual Vet Visits': 'Visitas_Anuais_Veterinario',
        'Healthy': 'Status_Saude'
    }
    
    df_pt = df.rename(columns=mapeamento_colunas)
    
    # Selecionamos apenas as colunas desejadas (Nivel_Atividade_Dono ficou de fora)
    colunas_finais = [
        'Raca', 'Sexo', 'Idade', 'peso_kg', 'porte_animal', 
        'Nivel_Atividade_Pet', 'Dieta_Atual', 'Marca_Racao', 
        'caminhada_diaria_km', 'Medicamentos', 'Convulsoes', 'Horas_Sono', 
        'Tempo_Brincadeira_Horas', 'Visitas_Anuais_Veterinario', 
        'calorias_diarias_RER', 'Status_Saude'
    ]
    
    df_final = df_pt[colunas_finais]

    # Salva com encoding adequado para Excel no Windows
    df_final.to_csv('dataset_petdex_final_PT.csv', index=False, encoding='utf-8-sig')


except Exception as e:
    print(f"❌ Erro: {e}")