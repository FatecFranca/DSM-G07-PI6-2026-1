from pydantic import BaseModel, Field
from typing import Optional


class PesoIdealRequestDTO(BaseModel):
    """
    Dados de entrada para a análise de peso ideal do animal.
    """
    raca: Optional[str] = Field(
        None,
        description="Raça do animal (deixe nulo ou vazio para Sem Raça Definida - SRD)",
        example="Golden Retriever"
    )
    porte: str = Field(
        ...,
        description="Porte do animal (Pequeno, Médio, Grande)",
        example="Grande"
    )
    sexo: str = Field(
        ...,
        description="Sexo do animal (M ou F)",
        example="M"
    )
    data_nascimento: str = Field(
        ...,
        description="Data de nascimento do animal (formato YYYY-MM-DD)",
        example="2020-05-15"
    )
    castrado: bool = Field(
        ...,
        description="Status de castração (true ou false)",
        example=True
    )
    peso_atual: float = Field(
        ...,
        description="Peso atual do animal em kg",
        example=32.5
    )

    class Config:
        schema_extra = {
            "example": {
                "raca": "Golden Retriever",
                "porte": "Grande",
                "sexo": "M",
                "data_nascimento": "2020-05-15",
                "castrado": True,
                "peso_atual": 32.5
            }
        }


class PesoIdealResponseDTO(BaseModel):
    """
    Resposta com a análise do peso ideal do animal, limites e o peso atual.
    """
    peso_ideal: float = Field(
        ...,
        description="Peso ideal projetado pela Inteligência Artificial em kg",
        example=30.2
    )
    peso_atual: float = Field(
        ...,
        description="Peso atual do animal (recebido na requisição)",
        example=32.5
    )
    peso_minimo: float = Field(
        ...,
        description="Limite inferior de peso saudável em kg",
        example=28.0
    )
    peso_maximo: float = Field(
        ...,
        description="Limite superior de peso saudável em kg",
        example=34.0
    )

    class Config:
        schema_extra = {
            "example": {
                "peso_ideal": 30.2,
                "peso_atual": 32.5,
                "peso_minimo": 28.0,
                "peso_maximo": 34.0
            }
        }
