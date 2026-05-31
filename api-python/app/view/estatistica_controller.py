from fastapi import APIRouter, Depends, Path, Query, HTTPException
from typing import Tuple
from datetime import date
from app.view.middleware.security import get_current_user
from app.application.dto.respostas_batimentos_dto import (
    EstatisticasBatimentosDTO, MediaPorIntervaloDTO, ProbabilidadeBatimentoDTO,
    AnaliseBatimentoUltimoDTO, MediaUltimos5DiasDTO, MediaUltimas5HorasDTO
)
from app.application.dto.respostas_regressao_dto import AnaliseRegressaoDTO, PredicaoBatimentoDTO
from app.application import EstatisticaService
from app.view.exception.exception_handlers import STANDARD_ERRORS

router = APIRouter(tags=["Batimentos"])
estatistica_service = EstatisticaService()

@router.get(
    "/batimentos/animal/{animalId}/estatisticas",
    response_model=EstatisticasBatimentosDTO,
    summary="Consultar estatísticas de batimentos",
    description="Obtém estatísticas gerais dos batimentos cardíacos de um animal, incluindo média, mediana, desvio padrão e outras medidas descritivas.\n\n**Requer autenticação JWT.**",
    responses={
        200: {
            "description": "Estatísticas calculadas com sucesso",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/EstatisticasBatimentosDTO"}
                }
            }
        },
        **STANDARD_ERRORS
    }
)
async def get_estatisticas(
    animalId: str = Path(..., description="Identificador único do animal", example="123"),
    credentials: Tuple[str, str] = Depends(get_current_user)
):
    """
    Obtém estatísticas gerais dos batimentos cardíacos de um animal.

    **Requer autenticação JWT.**

    Args:
        animalId: ID do animal

    Returns:
        dict: Estatísticas dos batimentos (média, desvio padrão, mínimo, máximo, etc.)

    Raises:
        401: Token JWT ausente, inválido ou expirado
    """
    _, token = credentials
    return estatistica_service.batimentos_calcular_estatisticas(animalId, token)

@router.get(
    "/batimentos/animal/{animalId}/batimentos/media-por-data",
    response_model=MediaPorIntervaloDTO,
    summary="Consultar média de batimentos por intervalo de datas",
    description="Calcula a média de batimentos cardíacos de um animal em um intervalo de datas específico.\n\n**Requer autenticação JWT.**",
    responses={
        200: {
            "description": "Média calculada com sucesso",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/MediaPorIntervaloDTO"}
                }
            }
        },
        **STANDARD_ERRORS
    }
)
async def media_batimentos_por_data(
    animalId: str = Path(..., description="Identificador único do animal", example="123"),
    inicio: date = Query(..., description="Data de início do intervalo (formato: YYYY-MM-DD)", example="2024-01-15"),
    fim: date = Query(..., description="Data de fim do intervalo (formato: YYYY-MM-DD)", example="2024-01-19"),
    credentials: Tuple[str, str] = Depends(get_current_user)
):
    """
    Calcula a média de batimentos por data em um intervalo especificado.

    **Requer autenticação JWT.**

    Args:
        animalId: ID do animal
        inicio: Data de início do intervalo (formato: YYYY-MM-DD)
        fim: Data de fim do intervalo (formato: YYYY-MM-DD)

    Returns:
        dict: Média de batimentos por data no intervalo especificado

    Raises:
        401: Token JWT ausente, inválido ou expirado
    """
    _, token = credentials
    return estatistica_service.media_batimentos_por_intervalo(animalId, token, inicio, fim)

@router.get(
    "/batimentos/animal/{animalId}/probabilidade",
    response_model=ProbabilidadeBatimentoDTO,
    summary="Calcular probabilidade de um valor de batimento",
    description="Calcula a probabilidade estatística de um determinado valor de batimento cardíaco ocorrer com base no histórico do animal.\n\n**Requer autenticação JWT.**",
    responses={
        200: {
            "description": "Probabilidade calculada com sucesso",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/ProbabilidadeBatimentoDTO"}
                }
            }
        },
        **STANDARD_ERRORS
    }
)
async def probabilidade_batimento(
    animalId: str = Path(..., description="Identificador único do animal", example="123"),
    valor: int = Query(..., gt=0, description="Valor de batimento para calcular a probabilidade em BPM (deve ser > 0)", example="85"),
    credentials: Tuple[str, str] = Depends(get_current_user)
):
    """
    Calcula a probabilidade de um valor de batimento ocorrer.

    **Requer autenticação JWT.**

    Args:
        animalId: ID do animal
        valor: Valor de batimento para calcular a probabilidade (deve ser > 0)

    Returns:
        dict: Probabilidade do valor de batimento ocorrer

    Raises:
        401: Token JWT ausente, inválido ou expirado
    """
    _, token = credentials
    return estatistica_service.probabilidade_batimento(animalId, token, valor)

@router.get(
    "/batimentos/animal/{animalId}/ultimo/analise",
    response_model=AnaliseBatimentoUltimoDTO,
    summary="Analisar último batimento registrado",
    description="Analisa o último batimento cardíaco registrado pela coleira e calcula sua probabilidade em relação ao histórico do animal.\n\n**Requer autenticação JWT.**",
    responses={
        200: {
            "description": "Análise realizada com sucesso",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/AnaliseBatimentoUltimoDTO"}
                }
            }
        },
        **STANDARD_ERRORS
    }
)
async def probabilidade_ultimo_batimento(
    animalId: str = Path(..., description="Identificador único do animal", example="123"),
    credentials: Tuple[str, str] = Depends(get_current_user)
):
    """
    Analisa o último batimento registrado e calcula sua probabilidade.

    **Requer autenticação JWT.**

    Args:
        animalId: ID do animal

    Returns:
        dict: Análise do último batimento com sua probabilidade

    Raises:
        401: Token JWT ausente, inválido ou expirado
    """
    _, token = credentials
    return estatistica_service.probabilidade_ultimo_batimento(animalId, token)

@router.get(
    "/batimentos/animal/{animalId}/media-ultimos-5-dias",
    response_model=MediaUltimos5DiasDTO,
    summary="Consultar média de batimentos dos últimos 5 dias",
    description="Calcula a média de batimentos cardíacos de um animal para cada um dos últimos 5 dias com dados disponíveis.\n\n**Requer autenticação JWT.**",
    responses={
        200: {
            "description": "Médias calculadas com sucesso",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/MediaUltimos5DiasDTO"}
                }
            }
        },
        **STANDARD_ERRORS
    }
)
async def media_batimentos_ultimos_5_dias(
    animalId: str = Path(..., description="Identificador único do animal", example="123"),
    credentials: Tuple[str, str] = Depends(get_current_user)
):
    """
    Calcula a média de batimentos dos últimos 5 dias válidos.

    **Requer autenticação JWT.**

    Args:
        animalId: ID do animal

    Returns:
        dict: Dicionário com as médias de batimentos dos últimos 5 dias

    Raises:
        401: Token JWT ausente, inválido ou expirado
    """
    _, token = credentials
    return {"medias": estatistica_service.media_ultimos_5_dias_validos(animalId, token)}

@router.get(
    "/batimentos/animal/{animalId}/media-ultimas-5-horas-registradas",
    response_model=MediaUltimas5HorasDTO,
    summary="Consultar média de batimentos das últimas 5 horas",
    description="Calcula a média de batimentos cardíacos de um animal para cada uma das últimas 5 horas com dados registrados.\n\n**Requer autenticação JWT.**",
    responses={
        200: {
            "description": "Médias calculadas com sucesso",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/MediaUltimas5HorasDTO"}
                }
            }
        },
        **STANDARD_ERRORS
    }
)
async def media_batimentos_ultimas_5_horas(
    animalId: str = Path(..., description="Identificador único do animal", example="123"),
    credentials: Tuple[str, str] = Depends(get_current_user)
):
    """
    Calcula a média de batimentos das últimas 5 horas registradas.

    **Requer autenticação JWT.**

    Args:
        animalId: ID do animal

    Returns:
        dict: Média de batimentos das últimas 5 horas registradas

    Raises:
        401: Token JWT ausente, inválido ou expirado
    """
    _, token = credentials
    return estatistica_service.media_ultimas_5_horas_registradas(animalId, token)

@router.get(
    "/batimentos/animal/{animalId}/regressao",
    response_model=AnaliseRegressaoDTO,
    summary="Analisar regressão entre batimentos e movimentos",
    description="Realiza análise de regressão linear entre os batimentos cardíacos e os dados de movimento (aceleração) de um animal, fornecendo coeficientes e correlações.\n\n**Requer autenticação JWT.**",
    responses={
        200: {
            "description": "Análise de regressão realizada com sucesso",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/AnaliseRegressaoDTO"}
                }
            }
        },
        **STANDARD_ERRORS
    }
)
async def analise_regressao_batimentos(
    animalId: str = Path(..., description="Identificador único do animal", example="123"),
    credentials: Tuple[str, str] = Depends(get_current_user)
):
    """
    Realiza análise de regressão entre batimentos e movimentos.

    **Requer autenticação JWT.**

    Args:
        animalId: ID do animal

    Returns:
        dict: Resultado da análise de regressão com coeficientes e função utilizada

    Raises:
        401: Token JWT ausente, inválido ou expirado
    """
    _, token = credentials
    return estatistica_service.analise_regressao_batimentos(animalId, token)

@router.get(
    "/batimentos/animal/{animalId}/predizer",
    response_model=PredicaoBatimentoDTO,
    summary="Prever frequência cardíaca baseada em aceleração",
    description="Prediz a frequência cardíaca de um animal baseado em valores de aceleração (acelerômetro) utilizando um modelo de regressão linear treinado com dados históricos.\n\n**Requer autenticação JWT.**",
    responses={
        200: {
            "description": "Predição realizada com sucesso",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/PredicaoBatimentoDTO"}
                }
            }
        },
        **STANDARD_ERRORS
    }
)
async def predizer_batimento(
    animalId: str = Path(..., description="Identificador único do animal", example="123"),
    acelerometroX: float = Query(..., description="Valor do acelerômetro no eixo X", example="0.5"),
    acelerometroY: float = Query(..., description="Valor do acelerômetro no eixo Y", example="0.3"),
    acelerometroZ: float = Query(..., description="Valor do acelerômetro no eixo Z", example="0.2"),
    credentials: Tuple[str, str] = Depends(get_current_user)
):
    """
    Prediz a frequência de batimentos baseado em valores de aceleração.

    **Requer autenticação JWT.**

    Utiliza um modelo de regressão linear para prever a frequência cardíaca
    baseado nos valores dos acelerômetros (X, Y, Z).

    Args:
        animalId: ID do animal
        acelerometroX: Valor do acelerômetro no eixo X
        acelerometroY: Valor do acelerômetro no eixo Y
        acelerometroZ: Valor do acelerômetro no eixo Z

    Returns:
        dict: Frequência prevista e função de regressão utilizada

    Raises:
        401: Token JWT ausente, inválido ou expirado
    """
    _, token = credentials
    return estatistica_service.predizer_batimento(animalId, token, acelerometroX, acelerometroY, acelerometroZ)
