from fastapi import APIRouter, Depends, Path, HTTPException
from typing import Tuple
from app.view.middleware.security import get_current_user
from app.application.dto.sintomas_dto import SintomasInputDTO, AnimalSintomasInputDTO
from app.application.dto.respostas_ia_dto import RespostaCheckupAnimalDTO, RespostaCheckupTesteDTO
from app.application import CheckupService
from app.view.exception.exception_handlers import STANDARD_ERRORS

router = APIRouter(tags=["IA"])
checkup_service = CheckupService()

@router.post(
    "/ia/checkup/animal/{id_animal}",
    response_model=RespostaCheckupAnimalDTO,
    summary="Analisar sintomas de um animal",
    description="Analisa os sintomas de um animal específico e retorna a predição de diagnóstico utilizando o modelo PMML.\n\n**Requer autenticação JWT.**",
    responses={
        200: {
            "description": "Análise realizada com sucesso",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/RespostaCheckupAnimalDTO"}
                }
            }
        },
        **STANDARD_ERRORS
    }
)
async def checkup_animal(
    id_animal: str = Path(..., description="Identificador único do animal a ser analisado", example="68194120636f719fcd5ee5fd"),
    sintomas: SintomasInputDTO = None,
    credentials: Tuple[str, str] = Depends(get_current_user)
):
    """
    Analisa sintomas de um animal e retorna a predição de problema/doença via PMML.

    **Requer autenticação JWT.**

    ## Parâmetros:
    - **id_animal** (path): ID do animal a ser analisado
    - **sintomas** (body): Dados dos sintomas do animal (veja o schema abaixo)

    ## Retorno:
    - **animalId**: ID do animal analisado
    - **dados_entrada**: Dados combinados do animal (da API Java + sintomas)
    - **probabilidades**: Probabilidades de cada classe de doença
    - **resultado**: Nome da classe com maior probabilidade (diagnóstico previsto)

    ## Possíveis diagnósticos:
    - cardiovascular_hematologica
    - cutanea
    - gastrointestinal
    - nenhuma
    - neuro_musculoesqueletica
    - respiratoria
    - urogenital

    ## Erros:
    - **401**: Token JWT ausente, inválido ou expirado
    - **404**: Animal não encontrado na API Java
    - **500**: Erro ao processar o modelo PMML
    """
    user_id, token = credentials
    resultado = checkup_service.analisar_sintomas_animal(id_animal, sintomas.dict(exclude_none=True), token)
    return resultado

@router.post(
    "/ia/checkup",
    response_model=RespostaCheckupTesteDTO,
    summary="Testar predição de diagnóstico",
    description="Rota de teste para validar a predição da IA com base em dados diretos, sem necessidade de integração com a API Java.\n\n**Não requer autenticação JWT** - Use esta rota para testar o modelo PMML.",
    responses={
        200: {
            "description": "Teste de predição realizado com sucesso",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/RespostaCheckupTesteDTO"}
                }
            }
        },
        **STANDARD_ERRORS
    }
)
async def checkup(sintomas: AnimalSintomasInputDTO):
    """
    Rota de teste para validar a predição da IA com base em dados diretos (sem API Java).

    **NÃO requer autenticação JWT** - Use esta rota para testar o modelo PMML.

    ## Parâmetros:
    - **sintomas** (body): Dados completos do animal com sintomas (veja o schema abaixo)

    ## Retorno:
    - **entrada**: Dados de entrada enviados
    - **probabilidades**: Probabilidades de cada classe de doença
    - **resultado**: Nome da classe com maior probabilidade (diagnóstico previsto)

    ## Possíveis diagnósticos:
    - cardiovascular_hematologica
    - cutanea
    - gastrointestinal
    - nenhuma
    - neuro_musculoesqueletica
    - respiratoria
    - urogenital

    ## Notas:
    - Ideal para testar se o modelo PMML está retornando o mesmo resultado que consta na tabela original usada no treinamento
    - Todos os campos são opcionais, mas quanto mais dados fornecidos, melhor a predição
    """
    try:
        dados_teste = sintomas.dict()
        return checkup_service.testar_predicao(dados_teste)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no teste de predição: {str(e)}")
