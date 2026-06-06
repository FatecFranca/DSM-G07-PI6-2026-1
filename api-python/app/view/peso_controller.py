from fastapi import APIRouter, Depends, Body, HTTPException
from typing import Tuple
from app.view.middleware.security import get_current_user
from app.application.dto.peso_dto import PesoIdealRequestDTO, PesoIdealResponseDTO
from app.application.services.peso_service import PesoService
from app.infraestructure.clients.java_api_client import JavaAPIClient
from app.view.exception.exception_handlers import STANDARD_ERRORS

router = APIRouter(tags=["Peso Ideal"])
peso_service = PesoService()

@router.post(
    "/peso/analise-ideal",
    response_model=PesoIdealResponseDTO,
    summary="Analisar peso ideal do pet",
    description="Prediz o peso ideal de um animal utilizando um modelo de IA baseado em suas características.\n\n**Requer autenticação JWT.**",
    responses={
        200: {
            "description": "Análise realizada com sucesso",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/PesoIdealResponseDTO"}
                }
            }
        },
        **STANDARD_ERRORS
    }
)
async def analisar_peso_ideal(
    dados: PesoIdealRequestDTO = Body(...),
    credentials: Tuple[str, str] = Depends(get_current_user)
):
    """
    Realiza a predição do peso ideal de um animal com Inteligência Artificial.

    **Requer autenticação JWT.**

    Utiliza os modelos `.pkl` para prever o peso ideal, de acordo com as 
    características informadas (Raça, Porte, Sexo, Idade, Status de Castração).
    """
    return peso_service.analisar_peso_ideal(dados)


@router.get(
    "/peso/animal/{animal_id}/analise-ideal",
    response_model=PesoIdealResponseDTO,
    summary="Analisar peso ideal do pet pelo ID",
    description="Busca os dados do animal na API Java e prediz seu peso ideal com IA.\n\n**Requer autenticação JWT.**",
    responses={
        200: {
            "description": "Análise realizada com sucesso",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/PesoIdealResponseDTO"}
                }
            }
        },
        **STANDARD_ERRORS
    }
)
async def analisar_peso_ideal_por_animal_id(
    animal_id: str,
    credentials: Tuple[str, str] = Depends(get_current_user)
):
    """
    Busca as informações do animal na API Java usando o `animal_id`
    e utiliza o modelo de Inteligência Artificial para predizer o peso ideal.
    """
    token = credentials[1]
    java_client = JavaAPIClient()
    
    status, animal_data = java_client.get_animal(animal_id, token)
    
    if status != 200:
        if status == 404:
            raise HTTPException(status_code=404, detail="Animal não encontrado na API Java")
        # Se a API Java retornar 0 (falha de conexão), usamos o status 503 Service Unavailable
        error_status = 503 if status == 0 else status
        raise HTTPException(status_code=error_status, detail=f"Erro ao buscar dados do animal na API Java. Status: {status} (Serviço indisponível ou erro na requisição)")
    
    try:
        dados = PesoIdealRequestDTO(
            raca=animal_data.get("raca"),
            porte=animal_data.get("porte"),
            sexo=animal_data.get("sexo"),
            data_nascimento=animal_data.get("data_nascimento") or animal_data.get("dataNascimento"),
            castrado=animal_data.get("castrado"),
            peso_atual=animal_data.get("peso_atual") or animal_data.get("pesoAtual") or animal_data.get("peso") or 0.0
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao formatar os dados do animal obtidos da API Java: {str(e)}")
        
    return peso_service.analisar_peso_ideal(dados)
