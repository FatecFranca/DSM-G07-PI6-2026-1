from app.schemas import respostas_batimentos
from requests import status_codes
from concurrent.futures import Executor
import pandas as pd
from statistics import mean, stdev
from scipy.stats import skew, norm, kurtosis
import numpy as np
import scipy.stats as stats
from typing import List, Dict
from datetime import datetime, timedelta, timezone, date
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr
from sklearn.preprocessing import StandardScaler
from app.infraestructure.clients.java_api_client import JavaAPIClient
import logging

logger = logging.getLogger("EstatisticaService")

class EstatisticaService:
    def __init__(self):
        self.java_api_client = JavaAPIClient()

    def _get_animal_todos_batimentos(self, animal_id: str, token: str, max_pages: int = 3) -> list[dict]:
        batimentos = []
        page = 0
        size = 100

        if not max_pages:
            logger.info("max_pages não informado. Definindo como 3")
            max_pages = 3

        try:
            status_code, response = self.java_api_client.get_animal_batimentos(animal_id, token, page, size)

            if status_code != 200:
                logger.error(f"API retornou {status_code}. Response: {response.text[:300] if hasattr(response, 'text') else str(response)[:300]}")
                return []

            if not response:
                logger.error("API não retornou conteúdo ao buscar batimentos do animal.")
                return []
            
            total_pages = min(response.get("totalPages", 1), max_pages)
            batimentos.extend(response.get("content", []))
            
            if total_pages > 1:
                for page in range(1, total_pages):
                    status_code, response = self.java_api_client.get_animal_batimentos(animal_id, token, page, size)
                    if response:
                        batimentos.extend(response.get("content", []))
    
        except Exception as e:
            logger.exception("Erro ao buscar todos batimentos")
            pass

        return batimentos

    def _get_animal_movimentos_todos(self, animal_id: str, token: str, max_pages: int = 3) -> list[dict]:
        movimentos = []
        page = 0
        size = 100

        if not max_pages:
            logger.info("max_pages não informado. Definindo como 3.")
            max_pages = 3
        
        try:
            status_code, response = self.java_api_client.get_animal_movimentos(animal_id, token, page, size)

            if status_code != 200:
                logger.error(f"API retornou {status_code}. Response: {response.text[:300] if hasattr(response, 'text') else str(response)[:300]}")
                return []

            if not response:
                logger.error("API não retornou conteúdo ao buscar movimentos do animal.")
                return []

            total_pages = min(response.get("totalPages", 1), max_pages)
            movimentos.extend(response.get("content", []))

            if total_pages > 1:
                for page in range(1, total_pages):
                    status_code, response = self.java_api_client.get_animal_movimentos(animal_id, token, page, size)
                    if response:
                        movimentos.extend(response.get("content", []))
            
        except Exception as e:
            logger.exception("Erro ao buscar movimentos do animal")
            pass

        return movimentos

    # ---------------------------------------------------------
    # Métodos Puros (Cálculos de Negócio)
    # ---------------------------------------------------------

    def calcular_estatisticas(self, dados: List[dict]) -> dict:
        if not dados:
            return {
                "media": None,
                "mediana": None,
                "moda": None,
                "desvio_padrao": None,
                "assimetria": None,
                "curtose": None
            }
        df = pd.DataFrame(dados)
        if df.empty or "frequenciaMedia" not in df.columns:
            return {
                "media": None,
                "mediana": None,
                "moda": None,
                "desvio_padrao": None,
                "assimetria": None,
                "curtose": None
            }

        df["frequenciaMedia"] = pd.to_numeric(df["frequenciaMedia"], errors="coerce")
        valores = df["frequenciaMedia"].dropna()
        valores = valores[(valores >= 30) & (valores <= 200)]
        print(f"Total bruto: {len(df)} | Após filtro de faixa: {len(valores)}")

        if valores.empty:
            return {
                "media": None,
                "mediana": None,
                "moda": None,
                "desvio_padrao": None,
                "assimetria": None,
                "curtose": None
            }

        media = valores.mean()
        desvio = valores.std()

        if desvio > 0:
            limite_inferior = media - 3 * desvio
            limite_superior = media + 3 * desvio
            valores = valores[(valores >= limite_inferior) & (valores <= limite_superior)]

        if valores.empty:
            return {
                "media": None,
                "mediana": None,
                "moda": None,
                "desvio_padrao": None,
                "assimetria": None,
                "curtose": None
            }

        return {
            "media": float(valores.mean()),
            "mediana": float(valores.median()),
            "moda": float(valores.mode().iloc[0]) if not valores.mode().empty else None,
            "desvio_padrao": float(valores.std()) if not pd.isna(valores.std()) else 0.0,
            "assimetria": float(skew(valores, bias=False)) if len(valores) > 2 else 0.0,
            "curtose": float(kurtosis(valores, bias=False)) if len(valores) > 3 else 0.0
        }

    def media_por_intervalo(self, dados: List[dict], inicio: date, fim: date) -> Dict:
        if not dados:
            return {"media": None, "mensagem": "Nenhum dado disponível."}

        df = pd.DataFrame(dados)

        if 'data' not in df.columns or 'frequenciaMedia' not in df.columns:
            return {"media": None, "mensagem": "Colunas esperadas não encontradas."}

        df['data'] = pd.to_datetime(df['data'], errors='coerce').dt.date
        df['frequenciaMedia'] = pd.to_numeric(df['frequenciaMedia'], errors='coerce')

        df = df.dropna(subset=['data', 'frequenciaMedia'])

        df_filtrado = df[(df['data'] >= inicio) & (df['data'] <= fim)]

        if df_filtrado.empty:
            return {"media": None, "mensagem": "Nenhum dado encontrado para o intervalo fornecido."}

        media = int(round(float(df_filtrado['frequenciaMedia'].mean())))
        return {"media": media}

    def calcular_probabilidade(self, valor: int, valores_batimentos: list) -> dict:
        valores_validos = [v for v in valores_batimentos if isinstance(v, (int, float)) and 20 <= v <= 200]

        if not valores_validos:
            return {
                "erro": "Não há dados suficientes dentro da faixa fisiológica (20 a 200 BPM) para análise."
            }

        media = np.mean(valores_validos)
        desvio = np.std(valores_validos)

        if valor < 20 or valor > 250:
            return {
                "valor_informado": valor,
                "media_registrada": int(round(media)),
                "desvio_padrao": int(round(desvio)),
                "titulo": "Valor fora da faixa ❌",
                "avaliacao": "O valor informado está fora da faixa fisiológica plausível para cães e gatos (20 a 200 BPM)."
            }

        # Evita divisão por zero se desvio for nulo
        desvio_calculo = desvio if desvio > 0 else 1.0

        z = abs((valor - media) / desvio_calculo)
        prob = (1 - norm.cdf(z)) * 2 * 100

        if z < 1:
            classificacao = "Dentro do esperado"
            titulo = "Batimento esperado ✅"
            interpretacao = (
                f"O valor de {valor} BPM está dentro do comportamento normal observado nos últimos dias. "
                f"A chance de ocorrer é alta ({round(prob, 2)}%)."
            )
        elif z < 2:
            classificacao = "Ligeiramente incomum"
            titulo = "Batimento um pouco fora do comum ⚠️"
            interpretacao = (
                f"O valor de {valor} BPM é um pouco diferente da média recente. "
                f"A chance de ocorrer é de aproximadamente {round(prob, 2)}%. Não é necessário se preocupar, mas observe o comportamento do seu pet."
            )
        elif z < 3:
            classificacao = "Incomum"
            titulo = "Batimento incomum ❗"
            interpretacao = (
                f"O valor de {valor} BPM é estatisticamente incomum com base nos últimos dias. "
                f"A chance de isso ocorrer naturalmente é de apenas {round(prob, 2)}%. Isso pode indicar agitação, estresse, exaustão ou até uma condition fisiológica crítica, como frequência cardíaca muito alta ou muito baixa. Observe o comportamento do seu pet e, se os sinais persistirem, tente acalmá-lo e procure um veterinário o quanto antes."
            )
        else:
            classificacao = "Raro ou fora do padrão"
            titulo = "Batimento raro ou atípico 🚨"
            interpretacao = (
                f"O valor de {valor} BPM é muito raro com base nos dados recentes. "
                f"A chance de ocorrer é de apenas {round(prob, 2)}%. Isso pode indicar uma situação atípica, erro na medição ou necessidade de atenção veterinária se persistir."
            )

        return {
            "valor_informado": valor,
            "media_registrada": int(round(media)),
            "desvio_padrao": int(round(desvio)),
            "probabilidade_percentual": round(prob, 2),
            "classificacao": classificacao,
            "titulo": titulo,
            "interpretacao": interpretacao,
            "avaliacao": interpretacao
        }

    def calcular_probabilidade_ultimo_batimento(self, valor: int, valores_batimentos: list) -> dict:
        valores_validos = [v for v in valores_batimentos if isinstance(v, (int, float)) and 20 <= v <= 200]

        if not valores_validos:
            return {
                "erro": "Não há dados suficientes dentro da faixa fisiológica (20 a 200 BPM) para análise."
            }

        media = np.mean(valores_validos)
        desvio = np.std(valores_validos)

        if valor < 20 or valor > 250:
            return {
                "valor_informado": valor,
                "media_registrada": int(round(media)),
                "desvio_padrao": int(round(desvio)),
                "titulo": "Último batimento fora da faixa ❌",
                "batimento_analisado": f"{valor} BPM",
                "interpretacao": "O último batimento coletado está fora da faixa fisiológica plausível para cães e gatos (20 a 200 BPM). Provavelmente ocorreu um erro com a coleira durante a coleta."
            }

        # Evita divisão por zero se desvio for nulo
        desvio_calculo = desvio if desvio > 0 else 1.0

        z = abs((valor - media) / desvio_calculo)
        prob = (1 - norm.cdf(z)) * 2 * 100

        if z < 1:
            classificacao = "Dentro do esperado"
            titulo = "Batimento esperado ✅"
            interpretacao = (
                f"O valor do último batimento coletado está dentro do comportamento normal observado nos últimos dias. "
            )
        elif z < 2:
            classificacao = "Ligeiramente incomum"
            titulo = "Batimento um pouco fora do comum ⚠️"
            interpretacao = (
                f"O valor do último batimento coletado é um pouco diferente da média recente. "
                f"Não é necessário se preocupar, mas observe o comportamento do seu pet."
            )
        elif z < 3:
            classificacao = "Incomum"
            titulo = "Batimento incomum ❗"
            interpretacao = (
                f"O valor do último batimento coletado é estatisticamente incomum com base nos últimos dias."
                f"Isso pode indicar agitação, estresse, exaustão ou até uma condição fisiológica crítica. Observe o comportamento do seu pet e, se os sinais persistirem, tente acalmá-lo, observe o comportamneto dele e as próximas análises, se persistir procure um veterinário"
            )
        else:
            classificacao = "Raro ou fora do padrão"
            titulo = "Batimento raro ou atípico 🚨"
            interpretacao = (
                f"O valor do último batimento coletado é muito raro com base nos dados recentes. "
                f"Isso pode indicar uma situação atípica, erro na medição ou necessidade de atenção veterinária se persistir."
            )

        return {
            "valor_informado": valor,
            "media_registrada": int(round(media)),
            "desvio_padrao": int(round(desvio)),
            "probabilidade_percentual": round(prob, 2),
            "classificacao": classificacao,
            "titulo": titulo,
            "interpretacao": interpretacao,
            "batimento_analisado": f"{valor} BPM",
            "avaliacao": interpretacao
        }

    def obter_media_ultimos_5_dias_validos(self, dados: List[dict]) -> dict:
        if not dados:
            return {}
        df = pd.DataFrame(dados)

        if 'data' not in df.columns or 'frequenciaMedia' not in df.columns:
            logger.error(f"Colunas esperadas não encontradas. Colunas encontradas: {df.columns.tolist()}",)
            return {}

        df['data'] = pd.to_datetime(df['data'], errors='coerce').dt.date
        df['frequenciaMedia'] = pd.to_numeric(df['frequenciaMedia'], errors='coerce')

        df = df.dropna(subset=['data', 'frequenciaMedia'])

        medias_por_dia = df.groupby('data')['frequenciaMedia'].mean()

        ultimos_5_dias = medias_por_dia.sort_index(ascending=False).head(5)

        resultado = {str(data): int(round(float(media))) for data, media in ultimos_5_dias.sort_index().items()}
        return resultado

    def obter_media_ultimas_5_horas_registradas(self, dados: List[dict]) -> dict:
        if not dados:
            return {"media": None, "media_por_hora": {}, "mensagem": "Nenhum dado disponível."}
        df = pd.DataFrame(dados)
        if df.empty:
            return {"media": None, "media_por_hora": {}, "mensagem": "Nenhum dado disponível."}

        # Conversão e limpeza
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
        df = df.dropna(subset=["data", "frequenciaMedia"])
        df["frequenciaMedia"] = pd.to_numeric(df["frequenciaMedia"], errors="coerce")
        df = df.dropna(subset=["frequenciaMedia"])

        # Ordenar por data decrescente
        df = df.sort_values(by="data", ascending=False)

        # Arredondar para hora cheia com 'h'
        df["hora"] = df["data"].dt.floor("h")

        # Selecionar as últimas 5 horas únicas
        ultimas_5_horas = df["hora"].drop_duplicates().head(5)

        # Filtrar os dados dessas horas
        df_filtrado = df[df["hora"].isin(ultimas_5_horas)]

        if df_filtrado.empty:
            return {"media": None, "media_por_hora": {}, "mensagem": "Nenhum dado nas últimas 5 horas registradas."}

        # Calcular média por hora
        medias_por_hora = df_filtrado.groupby("hora")["frequenciaMedia"].mean().sort_index()
        medias_formatadas = {str(hora): int(round(float(media))) for hora, media in medias_por_hora.items()}

        # Corrigindo a média geral (média das médias por hora)
        media_geral = int(round(float(medias_por_hora.mean())))

        return {
            "media": media_geral,
            "media_por_hora": medias_formatadas
        }

    def executar_regressao(self, batimentos: List[dict], movimentos: List[dict]) -> Dict:
        df_bat = pd.DataFrame(batimentos)
        df_mov = pd.DataFrame(movimentos)

        df_bat['data'] = pd.to_datetime(df_bat['data'])
        df_mov['data'] = pd.to_datetime(df_mov['data'])

        df_bat_grouped = df_bat.groupby('data').agg({'frequenciaMedia': 'mean'}).reset_index()
        df_mov_grouped = df_mov.groupby('data').mean(numeric_only=True).reset_index()

        df = pd.merge(df_bat_grouped, df_mov_grouped, on='data', how='inner')
        df = df.dropna(subset=['frequenciaMedia'])

        acelerometros = ['acelerometroX', 'acelerometroY', 'acelerometroZ']
        X = df[acelerometros]
        y = df['frequenciaMedia']

        # Correlação de Pearson
        correlacoes = {col: round(pearsonr(X[col], y)[0], 3) for col in X.columns}

        # Padronização
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Treinamento
        modelo = LinearRegression()
        modelo.fit(X_scaled, y)

        coef_dict = dict(zip(acelerometros, modelo.coef_.round(3)))
        coef_geral = round(modelo.intercept_, 3)
        funcao_regressao = f"frequenciaMedia = {coef_geral} + " + " + ".join(
            [f"({coef:.3f} * {var})" for var, coef in coef_dict.items()]
        )

        media_movimentos_pad = X_scaled[-10:].mean(axis=0).reshape(1, -1)
        predicoes = [modelo.predict(media_movimentos_pad)[0] for _ in range(5)]
        segundos_futuros = [(df['data'].max() + timedelta(seconds=i+1)).isoformat() for i in range(5)]
        projecao = dict(zip(segundos_futuros, [int(round(p)) for p in predicoes]))

        # Exporta estatísticas da padronização para reuso na predição
        scaler_info = {
            "media": scaler.mean_.tolist(),
            "desvio": scaler.scale_.tolist(),
            "variaveis": acelerometros
        }

        return {
            "coeficiente_geral": coef_geral,
            "coeficientes": coef_dict,
            "correlacoes": correlacoes,
            "r2": round(modelo.score(X_scaled, y), 3),
            "media_erro_quadratico": round(mean_squared_error(y, modelo.predict(X_scaled)), 2),
            "projecao_5_segundos": projecao,
            "funcao_regressao": funcao_regressao,
            "padronizacao": scaler_info
        }

    # ---------------------------------------------------------
    # Métodos de Orquestração (Integração com JavaAPIClient)
    # ---------------------------------------------------------

    def batimentos_calcular_estatisticas(self, animal_id: str, token: str) -> dict:
        batimentos = self._get_animal_todos_batimentos(animal_id, token, max_pages=3)
        if not batimentos:
            return {"error": True, "mensagem": "Nenhum batimento disponível."}
        return self.calcular_estatisticas(batimentos)

    def media_batimentos_por_intervalo(self, animal_id: str, token: str, inicio: date, fim: date) -> Dict:
        batimentos = self._get_animal_todos_batimentos(animal_id, token, max_pages=3)
        if not batimentos:
            return {"error": True, "media": None, "mensagem": "Nenhum dado disponível."}
        return self.media_por_intervalo(batimentos, inicio, fim)

    def probabilidade_batimento(self, animal_id: str, token: str, valor: int) -> dict:
        try:
            batimentos = self._get_animal_todos_batimentos(animal_id, token, max_pages=3)
            if not batimentos:
                return {"error": True, "mensagem": "Nenhum dado disponível."}

            valores_batimentos = [batimento["frequenciaMedia"] for batimento in batimentos if isinstance(batimento.get("frequenciaMedia"), (int, float))]
            if not valores_batimentos:
                return {"error": True, "mensagem": "Nenhum dado de batimentos disponível."}

            return self.calcular_probabilidade(valor=valor, valores_batimentos=valores_batimentos)
        except Exception as e:
            logger.exception("Erro ao calcular probabilidade do batimento")
            return {"error": True, "mensagem": "Erro ao calcular probabilidade do batimento"}

    def probabilidade_ultimo_batimento(self, animal_id: str, token: str) -> dict:
        try:
            status_code, response = self.java_api_client.get_animal_ultimo_batimento(animal_id, token)
            if status_code != 200 or not response:
                return {"error": True, "mensagem": "Erro ao buscar último batimento do animal"}

            valor_ultimo_batimento = response.get("frequenciaMedia", None)
            if valor_ultimo_batimento is None:
                return {"error": True, "mensagem": "Não foi possível obter o último batimento"}

            batimentos = self._get_animal_todos_batimentos(animal_id, token, max_pages=3)
            if not batimentos:
                return {"error": True, "mensagem": "Nenhum dado disponível."}

            valores_batimentos = [batimento["frequenciaMedia"] for batimento in batimentos if isinstance(batimento.get("frequenciaMedia"), (int, float))]
            if not valores_batimentos:
                return {"error": True, "mensagem": "Nenhum dado de batimentos disponível."}

            return self.calcular_probabilidade_ultimo_batimento(valor=valor_ultimo_batimento, valores_batimentos=valores_batimentos)
        except Exception as e:
            logger.exception("Erro ao calcular probabilidade do último batimento")
            return {"error": True, "mensagem": "Erro ao calcular probabilidade do último batimento"}

    def media_ultimos_5_dias_validos(self, animal_id: str, token: str) -> dict:
        batimentos = self._get_animal_todos_batimentos(animal_id, token, max_pages=3)
        if not batimentos:
            return {}
        return self.obter_media_ultimos_5_dias_validos(batimentos)

    def media_ultimas_5_horas_registradas(self, animal_id: str, token: str) -> dict:
        batimentos = self._get_animal_todos_batimentos(animal_id, token, max_pages=3)
        if not batimentos:
            return {"media": None, "media_por_hora": {}, "mensagem": "Nenhum dado disponível."}
        return self.obter_media_ultimas_5_horas_registradas(batimentos)

    def analise_regressao_batimentos(self, animal_id: str, token: str) -> dict:
        batimentos = self._get_animal_todos_batimentos(animal_id, token, max_pages=3)
        movimentos = self._get_animal_movimentos_todos(animal_id, token, max_pages=3)
        if not batimentos or not movimentos:
            return {"erro": "Dados insuficientes para análise."}
        return self.executar_regressao(batimentos, movimentos)

    def predizer_batimento(self, animal_id: str, token: str, acelerometroX: float, acelerometroY: float, acelerometroZ: float) -> dict:
        resultado = self.analise_regressao_batimentos(animal_id, token)
        if "erro" in resultado:
            return {"erro": "Dados insuficientes para gerar o modelo de regressão."}

        coef = resultado["coeficientes"]
        intercepto = resultado["coeficiente_geral"]
        padronizacao = resultado["padronizacao"]

        entrada_padronizada = {
            "acelerometroX": (acelerometroX - padronizacao["media"][0]) / padronizacao["desvio"][0],
            "acelerometroY": (acelerometroY - padronizacao["media"][1]) / padronizacao["desvio"][1],
            "acelerometroZ": (acelerometroZ - padronizacao["media"][2]) / padronizacao["desvio"][2]
        }

        frequencia_prevista = (
            intercepto
            + coef["acelerometroX"] * entrada_padronizada["acelerometroX"]
            + coef["acelerometroY"] * entrada_padronizada["acelerometroY"]
            + coef["acelerometroZ"] * entrada_padronizada["acelerometroZ"]
        )

        return {
            "frequencia_prevista": round(frequencia_prevista, 2),
            "funcao_usada": resultado["funcao_regressao"]
        }
