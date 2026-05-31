import logging
import os
import math
import pandas as pd
from typing import Dict, Any, Optional
from app.infraestructure.clients.java_api_client import JavaAPIClient
from app.domain.utils.utils import DomainUtils
from app.infraestructure.exception.custom_exceptions import ResourceNotFoundException

logger = logging.getLogger("CheckupService")

# Resolve o caminho absoluto para o diretório base 'api-python'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MODEL_PATH = os.path.join(BASE_DIR, "models", "modelo_CART.pmml")
_pmml_model = None

class CheckupService:
    def __init__(self):
        self.java_api_client = JavaAPIClient()

    def _load_model(self):
        """Carrega o modelo PMML de forma lazy."""
        global _pmml_model
        if _pmml_model is None:
            try:
                # Import pypmml apenas quando necessário
                from pypmml import Model
                logger.info(f"🔄 Carregando modelo PMML: {MODEL_PATH}")
                _pmml_model = Model.load(MODEL_PATH)
                logger.info(f"✅ Modelo PMML carregado com sucesso: {MODEL_PATH}")
            except Exception as e:
                logger.error(f"❌ Erro ao carregar modelo PMML: {e}")
                # Tenta carregar modelos alternativos
                alternative_models = [
                    os.path.join(BASE_DIR, "models", "modelo_decision_tree.pmml"),
                    os.path.join(BASE_DIR, "models", "modelo_svm.pmml"),
                    os.path.join(BASE_DIR, "models", "modelo_smo.pmml")
                ]
                for alt_model in alternative_models:
                    try:
                        from pypmml import Model
                        logger.info(f"🔄 Tentando modelo alternativo: {alt_model}")
                        _pmml_model = Model.load(alt_model)
                        logger.info(f"✅ Modelo alternativo carregado: {alt_model}")
                        break
                    except Exception as alt_e:
                        logger.warning(f"⚠️ Modelo alternativo {alt_model} também falhou: {alt_e}")
                        continue

                if _pmml_model is None:
                    logger.error("❌ Nenhum modelo PMML pôde ser carregado")

        return _pmml_model

    def predict_pmml(self, dados: dict) -> dict:
        """
        Realiza a predição usando o modelo PMML carregado.
        """
        current_model = self._load_model()
        if current_model is None:
            logger.error("❌ Modelo PMML não foi carregado corretamente")
            raise Exception("Modelo PMML não disponível")

        try:
            df = pd.DataFrame([dados])
            result = current_model.predict(df)
            return result.to_dict(orient="records")[0]
        except Exception as e:
            logger.error(f"🚨 Erro ao realizar predição: {e}")
            raise Exception(str(e))

    def predict_with_pmml_animal(self, dados: dict) -> dict:
        """
        Função que combina dados do animal com sintomas e realiza a predição.
        """
        current_model = self._load_model()
        if current_model is None:
            logger.error("❌ Modelo PMML não foi carregado corretamente")
            raise Exception("Modelo PMML não disponível")

        try:
            df = pd.DataFrame([dados])
            logger.info(f"\nDados : {dados}")
            result = current_model.predict(df)
            logger.info(f"Resultado: {result}")
            logger.info("✅ Predição realizada com sucesso")
            return result.to_dict(orient="records")[0]
        except Exception as e:
            logger.error(f"🚨 Erro ao realizar predição com PMML: {e}")
            raise Exception(str(e))

    def predict_with_pmml(self, animal_data: dict, sintomas_data: dict) -> dict:
        """
        Função que combina dados do animal com sintomas e realiza a predição.
        """
        current_model = self._load_model()
        if current_model is None:
            logger.error("❌ Modelo PMML não foi carregado corretamente")
            raise Exception("Modelo PMML não disponível")

        try:
            # Combina dados do animal com sintomas
            dados_completos = {**animal_data, **sintomas_data}

            # Converte campos categóricos para lowercase se necessário
            if "tipo_do_animal" in dados_completos and dados_completos["tipo_do_animal"]:
                dados_completos["tipo_do_animal"] = str(dados_completos["tipo_do_animal"]).lower()
            if "raca" in dados_completos and dados_completos["raca"]:
                dados_completos["raca"] = str(dados_completos["raca"]).lower()

            # Garante que campos numéricos sejam números
            campos_numericos = ["idade", "genero", "peso", "batimento_cardiaco"]
            for campo in campos_numericos:
                if campo in dados_completos:
                    try:
                        dados_completos[campo] = float(dados_completos[campo]) if dados_completos[campo] is not None else 0.0
                    except (ValueError, TypeError):
                        dados_completos[campo] = 0.0

            logger.info(f"🔍 Dados para predição: {dados_completos}")

            # Realiza a predição
            df = pd.DataFrame([dados_completos])
            result = current_model.predict(df)

            logger.info("✅ Predição realizada com sucesso")
            return result.to_dict(orient="records")[0]

        except Exception as e:
            logger.error(f"🚨 Erro ao realizar predição com PMML: {e}")
            raise Exception(str(e))

    def get_animal_data(self, data: Any) -> dict:
        """
        Consulta/normaliza os dados do animal e retorna os campos necessários para o modelo de predição.
        """
        if isinstance(data, str):
            token = os.getenv("JAVA_API_TOKEN")
            status_code, res = self.java_api_client.get_animal(data, token)
            if status_code != 200 or not res:
                return {}
            data = res

        return {
            "tipo_do_animal": data.get("especieNome", "").lower(),
            "raca": data.get("racaNome", "").lower(),
            "idade": DomainUtils.calcular_idade(data.get("dataNascimento"), retornar_float=True),
            "genero": 1 if data.get("sexo") == "M" else 0,
            "peso": data.get("peso", 0),
            "batimento_cardiaco": 0  # futuro: integrar com sensores
        }

    def analisar_sintomas_animal(self, animal_id: str, sintomas: dict, token: str) -> dict:
        """
        Orquestra a busca de dados do animal, cálculo de idade, normalização de raça,
        chamada do modelo de predição e sanitização dos resultados.
        """
        # 1. Busca dados do animal na API Java
        status_code, response = self.java_api_client.get_animal(animal_id, token)
        if status_code != 200 or not response:
            raise ResourceNotFoundException("Animal não encontrado na base de dados da API Java.")

        # 2. Busca último batimento
        status_code_bat, response_bat = self.java_api_client.get_animal_ultimo_batimento(animal_id, token)
        ultimo_batimento = None
        if status_code_bat == 200 and response_bat:
            ultimo_batimento = response_bat.get("frequenciaMedia")

        # 3. Calcula idade aproximada em anos usando DomainUtils (inteiro, como esperado pelo main.py antigo)
        data_nasc = response.get("dataNascimento")
        idade = DomainUtils.calcular_idade(data_nasc, retornar_float=False)

        # 4. Trata raça
        raca = response.get("racaNome")
        if raca == "SRD (Sem Raça Definida)":
            raca = "sem_raca_definida_(srd)"
        else:
            raca = (raca or "").lower().replace(" ", "_")

        # 5. Monta dados do modelo
        dados_modelo = {
            "tipo_do_animal": (response.get("especieNome") or "").lower(),
            "raca": raca,
            "idade": idade,
            "genero": 1 if (response.get("sexo") or "").lower() == "m" else 0,
            "peso": response.get("peso"),
            "batimento_cardiaco": ultimo_batimento,
            **sintomas
        }

        logger.info(f"Dados modelo montados: {dados_modelo}")

        # 6. Executa predição
        resultado = self.predict_with_pmml_animal(dados_modelo)

        # 7. Substitui todos os nan por None para evitar erro JSON
        resultado_sanitizado = {}
        classe_prevista = None
        if isinstance(resultado, dict):
            for k, v in resultado.items():
                if isinstance(v, float) and math.isnan(v):
                    resultado_sanitizado[k] = None
                else:
                    resultado_sanitizado[k] = v

            # 8. Extrai a classe com maior probabilidade
            max_prob = -1
            for key, value in resultado_sanitizado.items():
                if key.startswith("probability(") and isinstance(value, (int, float)) and value is not None:
                    if value > max_prob:
                        max_prob = value
                        classe_prevista = key.replace("probability(", "").replace(")", "")
        else:
            resultado_sanitizado = {"raw_result": resultado}

        return {
            "animalId": animal_id,
            "dados_entrada": dados_modelo,
            "probabilidades": resultado_sanitizado,
            "resultado": classe_prevista
        }

    def testar_predicao(self, sintomas: dict) -> dict:
        """
        Orquestra a predição para rota de teste direta (sem API Java).
        """
        resultado = self.predict_with_pmml({}, sintomas)

        # Sanitiza e Extrai a classe com maior probabilidade
        classe_prevista = None
        resultado_sanitizado = {}
        if isinstance(resultado, dict):
            for k, v in resultado.items():
                if isinstance(v, float) and math.isnan(v):
                    resultado_sanitizado[k] = None
                else:
                    resultado_sanitizado[k] = v

            max_prob = -1
            for key, value in resultado_sanitizado.items():
                if key.startswith("probability(") and isinstance(value, (int, float)) and value is not None:
                    if value > max_prob:
                        max_prob = value
                        classe_prevista = key.replace("probability(", "").replace(")", "")
        else:
            resultado_sanitizado = {"raw_result": resultado}

        return {
            "entrada": sintomas,
            "probabilidades": resultado_sanitizado,
            "resultado": classe_prevista
        }
