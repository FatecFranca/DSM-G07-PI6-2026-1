from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class RespostaCheckupAnimalDTO(BaseModel):
    """
    Resposta da análise de checkup de um animal com sintomas.
    
    Contém o ID do animal, dados de entrada utilizados, probabilidades de cada diagnóstico
    e o resultado final da predição.
    """
    animalId: str = Field(
        ...,
        description="Identificador único do animal analisado",
        example="68194120636f719fcd5ee5fd"
    )
    dados_entrada: Dict[str, Any] = Field(
        ...,
        description="Dados combinados do animal (informações demográficas + sintomas) utilizados no modelo",
        example={
            "tipo_do_animal": "cachorro",
            "raca": "sem_raca_definida_(srd)",
            "idade": 10,
            "genero": 1,
            "peso": 26.0,
            "batimento_cardiaco": 62.0,
            "duracao": 7.0,
            "perda_de_apetite": 1,
            "vomito": 1,
            "diarreia": 1,
            "desidratacao": 1,
            "dor": 1,
            "febre": 1,
            "fraqueza": 1,
            "letargia": 1
        }
    )
    probabilidades: Dict[str, Optional[float]] = Field(
        ...,
        description="Probabilidades calculadas para cada classe de diagnóstico possível",
        example={
            "probability(cardiovascular_hematologica)": 0.15,
            "probability(cutanea)": 0.05,
            "probability(gastrointestinal)": 0.65,
            "probability(nenhuma)": 0.05,
            "probability(neuro_musculoesqueletica)": 0.05,
            "probability(respiratoria)": 0.03,
            "probability(urogenital)": 0.02
        }
    )
    resultado: Optional[str] = Field(
        ...,
        description="Diagnóstico previsto (classe com maior probabilidade)",
        example="gastrointestinal"
    )

    class Config:
        schema_extra = {
            "example": {
                "animalId": "68194120636f719fcd5ee5fd",
                "dados_entrada": {
                    "tipo_do_animal": "cachorro",
                    "raca": "sem_raca_definida_(srd)",
                    "idade": 10,
                    "genero": 1,
                    "peso": 26.0,
                    "batimento_cardiaco": 62.0,
                    "duracao": 7.0,
                    "perda_de_apetite": 1,
                    "vomito": 1,
                    "diarreia": 1,
                    "desidratacao": 1,
                    "dor": 1,
                    "febre": 1,
                    "fraqueza": 1,
                    "letargia": 1
                },
                "probabilidades": {
                    "probability(cardiovascular_hematologica)": 0.15,
                    "probability(cutanea)": 0.05,
                    "probability(gastrointestinal)": 0.65,
                    "probability(nenhuma)": 0.05,
                    "probability(neuro_musculoesqueletica)": 0.05,
                    "probability(respiratoria)": 0.03,
                    "probability(urogenital)": 0.02
                },
                "resultado": "gastrointestinal"
            }
        }


class RespostaCheckupTesteDTO(BaseModel):
    """
    Resposta da análise de checkup de teste (sem dados da API Java).
    
    Utilizada para validação do modelo PMML com dados diretos.
    """
    entrada: Dict[str, Any] = Field(
        ...,
        description="Dados de entrada enviados para análise",
        example={
            "duracao": 7.0,
            "perda_de_apetite": 1,
            "vomito": 1,
            "diarreia": 1,
            "desidratacao": 1,
            "dor": 1,
            "febre": 1,
            "fraqueza": 1,
            "letargia": 1
        }
    )
    probabilidades: Dict[str, Optional[float]] = Field(
        ...,
        description="Probabilidades calculadas para cada classe de diagnóstico",
        example={
            "probability(cardiovascular_hematologica)": 0.15,
            "probability(cutanea)": 0.05,
            "probability(gastrointestinal)": 0.65,
            "probability(nenhuma)": 0.05,
            "probability(neuro_musculoesqueletica)": 0.05,
            "probability(respiratoria)": 0.03,
            "probability(urogenital)": 0.02
        }
    )
    resultado: Optional[str] = Field(
        ...,
        description="Diagnóstico previsto (classe com maior probabilidade)",
        example="gastrointestinal"
    )

    class Config:
        schema_extra = {
            "example": {
                "entrada": {
                    "duracao": 7.0,
                    "perda_de_apetite": 1,
                    "vomito": 1,
                    "diarreia": 1,
                    "desidratacao": 1,
                    "dor": 1,
                    "febre": 1,
                    "fraqueza": 1,
                    "letargia": 1
                },
                "probabilidades": {
                    "probability(cardiovascular_hematologica)": 0.15,
                    "probability(cutanea)": 0.05,
                    "probability(gastrointestinal)": 0.65,
                    "probability(nenhuma)": 0.05,
                    "probability(neuro_musculoesqueletica)": 0.05,
                    "probability(respiratoria)": 0.03,
                    "probability(urogenital)": 0.02
                },
                "resultado": "gastrointestinal"
            }
        }


class RecomendacaoEstiloVidaDTO(BaseModel):
    """
    Metas de estilo de vida saudável recomendadas pela IA.
    """
    caminhada_diaria_km_meta: float = Field(..., description="Meta recomendada de caminhada diária em km", example=3.5)
    nivel_atividade_meta: str = Field(..., description="Nível de atividade física ideal recomendado", example="Moderado")
    tempo_brincadeira_horas_meta: float = Field(..., description="Meta recomendada de horas de brincadeira diária", example=1.5)
    tipo_dieta_meta: str = Field(..., description="Tipo de dieta alimentar recomendado", example="Ração Seca")
    justificativa: str = Field(..., description="Explicação detalhada e diagnóstico clínico-nutricional em português", example="O pet está saudável...")


class RecomendacaoIADTO(BaseModel):
    """
    Recomendação nutricional e de estilo de vida gerada pela IA.
    """
    animalId: str = Field(..., example="68194120636f719fcd5ee5fd")
    nome: str = Field(..., example="Rex")
    diagnostico: str = Field(..., example="Sobrepeso")
    peso_ideal_esperado: float = Field(..., example=20.0)
    sugestoes_racao: list[str] = Field(..., example=["Ração Light Plus", "Ração Weight Control"])
    recomendacoes_estilo_vida: RecomendacaoEstiloVidaDTO = Field(..., description="Metas recomendadas de estilo de vida saudável")

    class Config:
        schema_extra = {
            "example": {
                "animalId": "68194120636f719fcd5ee5fd",
                "nome": "Rex",
                "diagnostico": "Sobrepeso",
                "peso_ideal_esperado": 20.0,
                "sugestoes_racao": ["Ração Light Plus", "Ração Weight Control"],
                "recomendacoes_estilo_vida": {
                    "caminhada_diaria_km_meta": 3.5,
                    "nivel_atividade_meta": "Moderado",
                    "tempo_brincadeira_horas_meta": 1.5,
                    "tipo_dieta_meta": "Ração Seca",
                    "justificativa": "O pet está saudável..."
                }
            }
        }
