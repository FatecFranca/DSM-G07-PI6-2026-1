from fastapi import APIRouter, Depends, Path, HTTPException, Query
from typing import Tuple, Optional
from app.view.middleware.security import get_current_user
from app.application import RecomendacaoService
from app.view.exception.exception_handlers import STANDARD_ERRORS
from app.application.dto.respostas_ia_dto import RecomendacaoIADTO, SimulacaoRecomendacaoInputDTO

router = APIRouter(tags=["IA - Recomendação"])
recomendacao_service = RecomendacaoService()

@router.get(
    "/animal/{animalId}/ia-recomendacao",
    response_model=RecomendacaoIADTO,
    summary="Obter recomendação da IA",
    description="Rota que integra a inteligência de recomendação com os dados reais do animal e o peso ideal.\n\n**Requer autenticação JWT.**",
    responses={
        200: {
            "description": "Recomendação gerada com sucesso"
        },
        **STANDARD_ERRORS
    }
)
async def obter_recomendacao_ia(
    animalId: str = Path(..., description="Identificador único do animal", example="68194120636f719fcd5ee5fd"), 
    pesoIdeal: float = Query(..., description="Peso ideal recomendado para o animal em kg", example=25.0),
    credentials: Tuple[str, str] = Depends(get_current_user)
):
    """
    Rota que integra a inteligência de recomendação com os dados reais do animal e o peso ideal.

    **Requer autenticação JWT.**
    """
    _, token = credentials
    return recomendacao_service.obter_recomendacao_ia_animal(animalId, pesoIdeal, token)


@router.post(
    "/ia/recomendacao",
    response_model=RecomendacaoIADTO,
    summary="Simular recomendação da IA",
    description="Rota que simula a recomendação nutricional enviando diretamente todos os dados necessários do animal no corpo da requisição, sem integração com a API Java.\n\n**Não requer autenticação JWT.**",
    responses={
        200: {
            "description": "Simulação realizada com sucesso"
        },
        **STANDARD_ERRORS
    }
)
async def simular_recomendacao_ia(dados: SimulacaoRecomendacaoInputDTO):
    """
    Rota que simula a recomendação nutricional enviando diretamente todos os dados necessários do animal no corpo da requisição, sem integração com a API Java.

    **Não requer autenticação JWT.**
    """
    try:
        dados_animal = {
            "peso": dados.peso,
            "dataNascimento": dados.dataNascimento,
            "caminhada_diaria_km": dados.caminhada_diaria_km,
            "porte": dados.porte,
            "racaNome": dados.raca,
            "nome": "Animal"
        }
        resultado = recomendacao_service.gerar_sugestao_nutricional(dados_animal, dados.peso_ideal)
        return {
            "animalId": "simulado",
            "nome": "Animal",
            "diagnostico": resultado["status_corporal"],
            "peso_ideal_esperado": resultado["peso_referencia"],
            "sugestoes_racao": resultado["recomendacoes"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na simulação de recomendação: {str(e)}")
