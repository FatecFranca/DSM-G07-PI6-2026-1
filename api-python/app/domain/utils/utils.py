from datetime import datetime, timezone
import math
from typing import Optional

class DomainUtils:
    @staticmethod
    def calcular_idade(data_nascimento_str: str, retornar_float: bool = False):
        """
        Calcula a idade de um animal a partir da string da data de nascimento.
        
        Se retornar_float for True:
            Retorna a idade aproximada em anos como float (ex: 2.5),
            arredondada para 1 casa decimal. Retorna 0.0 em caso de erro ou data futura.
            
        Se retornar_float for False:
            Retorna a idade em anos como inteiro:
            - se idade < 1: retorna 1
            - se idade >= 1: arredonda para o inteiro mais próximo
            - em caso de data futura ou erro: retorna None
        """
        if not data_nascimento_str:
            return 0.0 if retornar_float else None
            
        try:
            # Normaliza 'Z' para '+00:00' e faz o parse
            nascimento = datetime.fromisoformat(data_nascimento_str.replace("Z", "+00:00"))

            # Garante datetime aware em UTC
            if nascimento.tzinfo is None:
                nascimento = nascimento.replace(tzinfo=timezone.utc)
            else:
                nascimento = nascimento.astimezone(timezone.utc)

            hoje = datetime.now(timezone.utc)

            # Data futura => inválida
            if hoje < nascimento:
                return 0.0 if retornar_float else None

            # Calcula anos (usando média de 365.2425 dias por ano para maior precisão)
            dias = (hoje - nascimento).total_seconds() / 86400.0
            anos = dias / 365.2425

            if retornar_float:
                return round(anos, 1)

            if anos < 1:
                return 1

            # Arredonda para o inteiro mais próximo (0.5 -> para cima)
            return int(math.floor(anos + 0.5))
            
        except Exception:
            return 0.0 if retornar_float else None
