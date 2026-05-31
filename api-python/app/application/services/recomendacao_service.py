import json
import os
import logging
import joblib
import pandas as pd
from typing import Dict, Any, List
from app.infraestructure.clients.java_api_client import JavaAPIClient
from app.infraestructure.exception.custom_exceptions import ResourceNotFoundException
from app.domain.utils.utils import DomainUtils

logger = logging.getLogger("RecomendacaoService")

class RecomendacaoService:
    def __init__(self):
        self.java_api_client = JavaAPIClient()
        
        # Caminho absoluto para os artefatos de ML
        PASTA_MODELOS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'modelos_ia'))
        try:
            self.modelo_marca = joblib.load(os.path.join(PASTA_MODELOS, 'modelo_knn_racao.pkl'))
            self.scaler_marca = joblib.load(os.path.join(PASTA_MODELOS, 'scaler_knn_brand.pkl'))
            self.encoders = joblib.load(os.path.join(PASTA_MODELOS, 'label_encoders.pkl'))
            self.modelo_caminhada = joblib.load(os.path.join(PASTA_MODELOS, 'modelo_caminhada_ideal.pkl'))
            self.modelo_dieta = joblib.load(os.path.join(PASTA_MODELOS, 'modelo_dieta_ideal.pkl'))
            self.modelo_atividade = joblib.load(os.path.join(PASTA_MODELOS, 'modelo_atividade_ideal.pkl'))
            
            with open(os.path.join(PASTA_MODELOS, 'db-food.json'), 'r', encoding='utf-8') as f:
                self.catalogo = json.load(f)
            logger.info("Todos os modelos de IA carregados com sucesso no RecomendacaoService.")
        except Exception as e:
            logger.error(f"Erro ao carregar arquivos da IA no RecomendacaoService: {e}")
            self.modelo_marca = None
            self.scaler_marca = None
            self.encoders = None
            self.modelo_caminhada = None
            self.modelo_dieta = None
            self.modelo_atividade = None
            self.catalogo = []

    def gerar_sugestao_nutricional(self, dados_animal: Dict[str, Any], peso_ideal: float) -> Dict[str, Any]:
        """
        Recebe os dados do animal vindos da API Java e gera a recomendação utilizando
        o cascade de Inteligência Artificial com base no peso ideal recebido.
        """
        if self.modelo_marca is None or self.scaler_marca is None or self.encoders is None:
            raise ValueError("Os modelos de recomendação da IA não foram carregados corretamente no servidor.")

        # 1. VALIDAÇÃO E EXTRAÇÃO DOS INPUTS OBRIGATÓRIOS
        # Peso Atual
        peso_val = dados_animal.get("peso")
        if peso_val is None:
            raise ValueError("O peso do animal é obrigatório para gerar a recomendação.")
        try:
            peso_kg = float(peso_val)
            if peso_kg <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("Peso do animal inválido. Deve ser um número maior que zero.")

        # Idade
        data_nasc = dados_animal.get("dataNascimento")
        if not data_nasc:
            raise ValueError("A data de nascimento do animal é obrigatória.")
        idade = DomainUtils.calcular_idade(data_nasc)
        if idade is None:
            raise ValueError("Idade do animal inválida ou não pôde ser calculada a partir da data de nascimento.")

        # Caminhada Diária Atual (KM) - Opcional, com fallback para 0.0
        caminhada_val = dados_animal.get("caminhada_diaria_km") or dados_animal.get("caminhadaDiariaKm") or dados_animal.get("caminhada_diaria") or dados_animal.get("caminhadaDiaria")
        if caminhada_val is not None:
            try:
                caminhada_diaria_km = float(caminhada_val)
                if caminhada_diaria_km < 0:
                    caminhada_diaria_km = 0.0
            except ValueError:
                caminhada_diaria_km = 0.0
        else:
            caminhada_diaria_km = 0.0

        # 2. CODIFICAÇÃO DAS CATEGORIAS DO ANIMAL
        le_raca = self.encoders['Raca']
        le_sexo = self.encoders['Sexo']

        # Normalização da raça usando racaNome
        raca_crua = dados_animal.get("racaNome") or "SRD (Sem Raça Definida)"
        raca_nome = "SRD (Sem Raça Definida)"
        for classe in le_raca.classes_:
            if raca_crua.strip().lower() == classe.strip().lower():
                raca_nome = classe
                break
        
        # Normalização do sexo
        sexo_cru = dados_animal.get("sexo") or "Macho"
        if (sexo_cru or "").lower() in ['f', 'femea', 'fêmea', 'female']:
            sexo_nome = 'Fêmea'
        else:
            sexo_nome = 'Macho'

        raca_encoded = le_raca.transform([raca_nome])[0]
        sexo_encoded = le_sexo.transform([sexo_nome])[0]

        # 3. FLUXO DE INFERÊNCIAS EM CADEIA
        try:
            # A. Peso Ideal recebido como parâmetro
            peso_ideal = round(float(peso_ideal), 2)

            # B. Cálculo de Calorias RER com base no Peso Ideal
            calorias_diarias_RER = round(70 * (peso_ideal ** 0.75), 2)

            # C. Predição da Meta de Caminhada Recomendada (com base no Peso Ideal)
            X_caminhada = pd.DataFrame([{
                'Raca': raca_encoded,
                'Sexo': sexo_encoded,
                'Idade': idade,
                'peso_kg': peso_ideal
            }])
            caminhada_diaria_km_meta = round(float(self.modelo_caminhada.predict(X_caminhada)[0]), 2)

            # D. Predição da Dieta Recomendada
            X_dieta = pd.DataFrame([{
                'Raca': raca_encoded,
                'Sexo': sexo_encoded,
                'Idade': idade,
                'peso_kg': peso_ideal
            }])
            dieta_pred_num = self.modelo_dieta.predict(X_dieta)[0]
            dieta_recomendada = self.encoders['Dieta_Atual'].inverse_transform([dieta_pred_num])[0]

            # E. Predição de Nível de Atividade Recomendado
            X_atividade = pd.DataFrame([{
                'Raca': raca_encoded,
                'Sexo': sexo_encoded,
                'Idade': idade,
                'peso_kg': peso_ideal
            }])
            atividade_pred_num = self.modelo_atividade.predict(X_atividade)[0]
            atividade_recomendada = self.encoders['Nivel_Atividade_Pet'].inverse_transform([atividade_pred_num])[0]

            # F. Predição da Marca de Ração Ideal (KNN) usando as metas saudáveis
            X_brand = pd.DataFrame([{
                'Age': idade,
                'Weight (kg)': peso_ideal,
                'caminhada_diaria_km': caminhada_diaria_km_meta,
                'calorias_diarias_RER': calorias_diarias_RER
            }])
            # Normalizar os dados usando o scaler treinado antes da predição KNN
            X_brand_scaled = self.scaler_marca.transform(X_brand)
            predicao_brand_num = self.modelo_marca.predict(X_brand_scaled)[0]
            marca_prevista_nome = self.encoders['Marca_Racao'].inverse_transform([predicao_brand_num])[0]

        except Exception as e:
            raise ValueError(f"Não foi possível obter a recomendação da IA devido a uma falha nos modelos: {str(e)}")

        # 4. DIAGNÓSTICO CORPORAL COMPARATIVO
        if peso_kg > (peso_ideal * 1.15):
            status_corpo = 'Sobrepeso'
        elif peso_kg < (peso_ideal * 0.85):
            status_corpo = 'Abaixo do Peso'
        else:
            status_corpo = 'Peso Ideal'

        # 5. FILTRAR CATÁLOGO DE PRODUTOS
        # O porte é calculado dinamicamente com base no peso real do animal
        if peso_kg <= 10:
            porte_pet_original = 'Pequeno'
        elif peso_kg <= 25:
            porte_pet_original = 'Médio'
        else:
            porte_pet_original = 'Grande'

        mapa_porte = {'Pequeno': 'Small', 'Médio': 'Medium', 'Grande': 'Large'}
        porte_busca = mapa_porte.get(porte_pet_original, 'All')

        sugestoes = []
        for produto in self.catalogo:
            match_marca = (produto.get('brand') == marca_prevista_nome)
            match_porte = (produto.get('animalSize') == "All" or produto.get('animalSize') == porte_busca)
            
            # Filtro de nutrição baseada no status corporal
            match_nutricao = False
            if status_corpo == 'Sobrepeso':
                match_nutricao = produto.get('condition') in ['Overweight', 'Weight Management', 'Weight Care', 'Active/Weight Management']
            elif status_corpo == 'Abaixo do Peso':
                match_nutricao = produto.get('condition') is None or "Puppy" in produto.get('name', '')
            else:
                match_nutricao = produto.get('condition') in [None, 'Everyday Health']

            if match_marca and match_porte and match_nutricao:
                sugestoes.append(produto['name'])

        # Fallbacks de relaxamento de filtros se nenhum for encontrado
        if not sugestoes:
            for produto in self.catalogo:
                if produto.get('brand') == marca_prevista_nome and (produto.get('animalSize') == "All" or produto.get('animalSize') == porte_busca):
                    sugestoes.append(produto['name'])
        if not sugestoes:
            for produto in self.catalogo:
                if produto.get('brand') == marca_prevista_nome:
                    sugestoes.append(produto['name'])
        if not sugestoes:
            sugestoes = [f"Ração recomendada da marca {marca_prevista_nome}"]

        # 6. JUSTIFICATIVA E METAS DE ESTILO DE VIDA
        if status_corpo == 'Sobrepeso':
            justificativa = (
                f"O pet esta com sobrepeso (Peso Atual: {peso_kg:.1f} kg vs. Peso Ideal: {peso_ideal:.1f} kg). "
                f"Recomenda-se reduzir a ingestao calorica diaria para {calorias_diarias_RER} kcal e "
                f"elevar a atividade fisica do animal para a meta '{atividade_recomendada}'."
            )
        elif status_corpo == 'Abaixo do Peso':
            justificativa = (
                f"O pet esta abaixo do peso (Peso Atual: {peso_kg:.1f} kg vs. Peso Ideal: {peso_ideal:.1f} kg). "
                f"Recomenda-se adotar uma dieta do tipo '{dieta_recomendada}' de alto teor energetico "
                f"e limitar atividades exaustivas temporariamente para acumulo de massa."
            )
        else:
            justificativa = (
                f"Parabens! O pet esta na faixa de peso ideal ({peso_kg:.1f} kg). "
                f"Mantenha a dieta atual equilibrada e siga a rotina de exercicios para preservar a saude."
            )

        return {
            "status_corporal": status_corpo,
            "peso_referencia": peso_ideal,
            "recomendacoes": sugestoes[:2],
            "recomendacoes_estilo_vida": {
                "caminhada_diaria_km_meta": caminhada_diaria_km_meta,
                "nivel_atividade_meta": atividade_recomendada,
                "tempo_brincadeira_horas_meta": 1.5 if status_corpo == 'Sobrepeso' else 1.0,
                "tipo_dieta_meta": dieta_recomendada,
                "justificativa": justificativa
            }
        }

    def obter_recomendacao_ia_animal(self, animal_id: str, peso_ideal: float, token: str) -> Dict[str, Any]:
        """
        Orquestra a busca dos dados do animal na API Java e gera a recomendação nutricional.
        """
        status_code, dados_animal = self.java_api_client.get_animal(animal_id, token)
        
        if status_code != 200 or not dados_animal:
            raise ResourceNotFoundException("Animal não encontrado na base de dados da API Java.")

        # Realiza a predição chamando a lógica do modelo de IA com o peso_ideal
        resultado = self.gerar_sugestao_nutricional(dados_animal, peso_ideal)
        
        return {
            "animalId": animal_id,
            "nome": dados_animal.get("nome", "Animal"),
            "diagnostico": resultado["status_corporal"],
            "peso_ideal_esperado": resultado["peso_referencia"],
            "sugestoes_racao": resultado["recomendacoes"],
            "recomendacoes_estilo_vida": resultado["recomendacoes_estilo_vida"]
        }

