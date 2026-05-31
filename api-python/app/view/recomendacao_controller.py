from fastapi import APIRouter, Depends, Path, HTTPException
from typing import Tuple
from app.view.middleware.security import get_current_user
from app.application import RecomendacaoService
from app.view.exception.exception_handlers import STANDARD_ERRORS
from app.application.dto.respostas_ia_dto import RecomendacaoIADTO

router = APIRouter(tags=["IA - Recomendação"])
recomendacao_service = RecomendacaoService()

@router.get(
    "/animal/{animalId}/ia-recomendacao",
    response_model=RecomendacaoIADTO,
    summary="Obter recomendação da IA",
    description="Rota que integra a inteligência de peso ideal com os dados reais do animal para fornecer sugestões nutricionais.\n\n**Requer autenticação JWT.**",
    responses={
        200: {
            "description": "Recomendação gerada com sucesso"
        },
        **STANDARD_ERRORS
    }
)
async def obter_recomendacao_ia(
    animalId: str = Path(..., description="Identificador único do animal"), 
    credentials: Tuple[str, str] = Depends(get_current_user)
):
    """
    Rota que integra a inteligência de peso ideal com os dados reais do animal.

    **Requer autenticação JWT.**
    """
    _, token = credentials
    return recomendacao_service.obter_recomendacao_ia_animal(animalId, token)
