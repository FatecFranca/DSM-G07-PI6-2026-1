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
        
        PASTA_MODELOS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'models', 'recomendation'))
        try:
            self.modelo_marca = joblib.load(os.path.join(PASTA_MODELOS, 'modelo_knn_racao.pkl'))
            self.scaler_marca = joblib.load(os.path.join(PASTA_MODELOS, 'scaler_knn_brand.pkl'))
            self.encoders = joblib.load(os.path.join(PASTA_MODELOS, 'label_encoders.pkl'))
            
            with open(os.path.join(PASTA_MODELOS, 'db-food.json'), 'r', encoding='utf-8') as f:
                self.catalogo = json.load(f)
            logger.info("Todos os modelos de IA carregados com sucesso no RecomendacaoService.")
        except Exception as e:
            logger.error(f"Erro ao carregar arquivos da IA no RecomendacaoService: {e}")
            self.modelo_marca = None
            self.scaler_marca = None
            self.encoders = None
            self.catalogo = []

    def gerar_sugestao_nutricional(self, dados_animal: Dict[str, Any], peso_ideal: float) -> Dict[str, Any]:
        """
        Recebe os dados do animal vindos da API Java e gera a recomendação utilizando
        o classificador KNN com base no peso ideal recebido.
        """
        if self.modelo_marca is None or self.scaler_marca is None or self.encoders is None:
            raise ValueError("Os modelos de recomendação da IA não foram carregados corretamente no servidor.")

        peso_val = dados_animal.get("peso")
        if peso_val is None:
            raise ValueError("O peso do animal é obrigatório para gerar a recomendação.")
        try:
            peso_kg = float(peso_val)
            if peso_kg <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("Peso do animal inválido. Deve ser um número maior que zero.")

        data_nasc = dados_animal.get("dataNascimento")
        if not data_nasc:
            raise ValueError("A data de nascimento do animal é obrigatória.")
        idade = DomainUtils.calcular_idade(data_nasc)
        if idade is None:
            raise ValueError("Idade do animal inválida ou não pôde ser calculada a partir da data de nascimento.")

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

        try:
            peso_ideal = round(float(peso_ideal), 2)

            calorias_diarias_RER = round(70 * (peso_ideal ** 0.75), 2)

            X_brand = pd.DataFrame([{
                'Age': idade,
                'Weight (kg)': peso_ideal,
                'caminhada_diaria_km': caminhada_diaria_km,
                'calorias_diarias_RER': calorias_diarias_RER
            }])
            X_brand_scaled = self.scaler_marca.transform(X_brand)
            predicao_brand_num = self.modelo_marca.predict(X_brand_scaled)[0]
            marca_prevista_nome = self.encoders['Marca_Racao'].inverse_transform([predicao_brand_num])[0]

        except Exception as e:
            raise ValueError(f"Não foi possível obter a recomendação da IA devido a uma falha nos modelos: {str(e)}")

        if peso_kg > (peso_ideal * 1.10):
            status_corpo = 'Sobrepeso'
        elif peso_kg < (peso_ideal * 0.90):
            status_corpo = 'Abaixo do Peso'
        else:
            status_corpo = 'Peso Ideal'

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
            
            match_nutricao = False
            if status_corpo == 'Sobrepeso':
                match_nutricao = produto.get('condition') in ['Overweight', 'Weight Management', 'Weight Care', 'Active/Weight Management']
            elif status_corpo == 'Abaixo do Peso':
                match_nutricao = produto.get('condition') is None or "Puppy" in produto.get('name', '')
            else:
                match_nutricao = produto.get('condition') in [None, 'Everyday Health']

            if match_marca and match_porte and match_nutricao:
                sugestoes.append(produto)

        if not sugestoes:
            for produto in self.catalogo:
                if produto.get('brand') == marca_prevista_nome and (produto.get('animalSize') == "All" or produto.get('animalSize') == porte_busca):
                    sugestoes.append(produto)
        if not sugestoes:
            for produto in self.catalogo:
                if produto.get('brand') == marca_prevista_nome:
                    sugestoes.append(produto)
        if not sugestoes:
            sugestoes = [{
                "brand": marca_prevista_nome,
                "name": f"Ração recomendada da marca {marca_prevista_nome}"
            }]

        if status_corpo == 'Sobrepeso':
            motivo = "Como o seu animal está acima do peso ideal (Sobrepeso), é recomendada essa ração para o controle e gerenciamento de peso."
        elif status_corpo == 'Abaixo do Peso':
            motivo = "Como o seu animal está abaixo do peso ideal, é recomendada essa ração para auxiliar no ganho de peso e fornecer uma nutrição reforçada."
        else:
            motivo = "Como o seu animal está na faixa de peso ideal, é recomendada essa ração para a manutenção da sua saúde e nutrição diária."

        recomendacoes_estruturadas = []
        for prod in sugestoes:
            recomendacoes_estruturadas.append({
                "marca": prod.get("brand") or marca_prevista_nome,
                "nome": prod.get("name") or f"Ração recomendada da marca {marca_prevista_nome}",
                "motivo": motivo
            })

        return {
            "status_corporal": status_corpo,
            "peso_referencia": peso_ideal,
            "recomendacoes": recomendacoes_estruturadas[:2]
        }

    def obter_recomendacao_ia_animal(self, animal_id: str, peso_ideal: float, token: str) -> Dict[str, Any]:
        """
        Orquestra a busca dos dados do animal na API Java e gera a recomendação nutricional.
        """
        status_code, dados_animal = self.java_api_client.get_animal(animal_id, token)
        
        if status_code != 200 or not dados_animal:
            raise ResourceNotFoundException("Animal não encontrado na base de dados da API Java.")

        resultado = self.gerar_sugestao_nutricional(dados_animal, peso_ideal)
        
        return {
            "animalId": animal_id,
            "nome": dados_animal.get("nome", "Animal"),
            "diagnostico": resultado["status_corporal"],
            "peso_ideal_esperado": resultado["peso_referencia"],
            "sugestoes_racao": resultado["recomendacoes"]
        }
