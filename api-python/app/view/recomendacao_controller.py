from fastapi import APIRouter, Depends, Path, HTTPException
from typing import Tuple
from app.view.middleware.security import get_current_user
from app.application import RecomendacaoService

router = APIRouter(tags=["IA - Recomendação"])
recomendacao_service = RecomendacaoService()

@router.get(
    "/animal/{animalId}/ia-recomendacao",
    summary="Obter recomendação da IA",
    description="Rota que integra a inteligência de peso ideal com os dados reais do animal para fornecer sugestões nutricionais.\n\n**Requer autenticação JWT.**"
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
    resultado = recomendacao_service.obter_recomendacao_ia_animal(animalId, token)
    
    if isinstance(resultado, dict) and "erro" in resultado:
        if resultado.get("status_code") == 404:
            raise HTTPException(status_code=404, detail=resultado.get("erro"))
        raise HTTPException(status_code=500, detail=resultado.get("erro"))
        
    return resultado
