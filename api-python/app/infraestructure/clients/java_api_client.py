import logging
import requests as req
import os
from dotenv import load_dotenv
from app.infraestructure.exception.custom_exceptions import ResourceNotFoundException

load_dotenv()
logger = logging.getLogger("API Java Integration")

class JavaAPIClient:
    def __init__(self):
        self.base_url = os.getenv("API_URL", "localhost:8080")

    def _get_headers(self, token: str) -> dict:
        return {"Authorization": f"Bearer {token}"}

    def get_animal(self, animal_id: str, token: str):

        url = f"{self.base_url}/animais/{animal_id}"
        headers = self._get_headers(token)

        try:
            response = req.get(url=url, headers=headers)
            if response.status_code == 404:
                raise ResourceNotFoundException(f"Recurso não encontrado na API Java. (Animal {animal_id})")
            if response.status_code != 200:
                logger.error(f"[API ERROR] Buscar dados do animal {animal_id}. Status: {response.status_code} / Response: {response.text[:300]}")
                return response.status_code, {}
            return response.status_code, response.json()

        except ResourceNotFoundException:
            raise
        except Exception as e:
            logger.exception(f"[EXCEPTION ERROR] Buscar os dados do animal: {animal_id}")
            return 0, {}

    def get_animal_ultimo_batimento(self, animal_id: str, token: str) -> tuple[int, dict]:
        
        url = f"{self.base_url}/batimentos/animal/{animal_id}/ultimo"
        headers = self._get_headers(token)
        
        try:
            response = req.get(url=url, headers=headers)
            if response.status_code == 404:
                raise ResourceNotFoundException(f"Recurso não encontrado na API Java. (Último batimento animal {animal_id})")
            if response.status_code != 200:
                logger.error(f"[API ERROR] Último baitmento do animal {animal_id}. Status: {response.status_code} / Response: {response.text[:300]}")
                return response.status_code, response.json()
            return response.status_code, response.json()
        except ResourceNotFoundException:
            raise
        except Exception as e:
            logger.exception(f"[EXCEPTION ERROR] Último batimento do animal {animal_id}")
            return 0, {}
    
    def get_animal_batimentos(self, animal_id: str, token: str, page: int = 0, size: int = 10, sort_by: str = None, direction: str = None, data_inicio: str = None, data_fim: str = None) -> tuple[int,dict]:
        if not size:
            size = 10
    
        url = f"{self.base_url}/batimentos/animal/{animal_id}?page={page}&size={size}"
        if sort_by: url += f"&sortBy={sort_by}"
        if direction: url += f"&direction={direction}"
        if data_inicio: url += f"&dataInicio={data_inicio}"
        if data_fim: url += f"&dataFim={data_fim}"
        
        headers = self._get_headers(token)
        try:
            response = req.get(url=url, headers=headers)
            if response.status_code == 404:
                raise ResourceNotFoundException(f"Recurso não encontrado na API Java. (Batimentos animal {animal_id})")
            if response.status_code != 200:
                logger.error(f"[API ERROR] Buscar baitmentos do animal {animal_id}. Status: {response.status_code} / Response: {response.text[:300]}")
                
                return response.status_code, {}
            return response.status_code, response.json()

        except ResourceNotFoundException:
            raise
        except Exception as e:
            logger.exception(f"[EXCEPTION ERROR] Buscar batimentos do animal {animal_id}")
            return 0, {}
        
    
    def get_animal_movimentos(self, animal_id: str, token:str, page: int = 0, size: int = 10, sort_by: str = None, direction: str = None, data_inicio: str = None, data_fim: str = None) -> tuple[int,dict]:
        if not size:
            size = 10
        url = f"{self.base_url}/movimentos/animal/{animal_id}?page={page}&size={size}"
        if sort_by: url += f"&sortBy={sort_by}"
        if direction: url += f"&direction={direction}"
        if data_inicio: url += f"&dataInicio={data_inicio}"
        if data_fim: url += f"&dataFim={data_fim}"

        headers = self._get_headers(token)

        try:
            response = req.get(url=url, headers=headers)
            if response.status_code == 404:
                raise ResourceNotFoundException(f"Recurso não encontrado na API Java. (Movimentos animal {animal_id})")
            if response.status_code != 200:
                logger.error(f"[API ERROR] Buscar movimentos do animal {animal_id}. Status: {response.status_code} / Response: {response.text[:300]}")
                return response.status_code, {}
            return response.status_code, response.json()
        except ResourceNotFoundException:
            raise
        except Exception as e:
            logger.exception(f"[EXCEPTION ERROR] Buscar movimentos do animal {animal_id}")
            return 0, {}

    def get_animal_localizacao(self, animal_id: str, token:str, page: int = 0, size: int = 10, sort_by: str = None, direction: str = None, data_inicio: str = None, data_fim: str = None) -> tuple[int,dict]:
        if not size:
            size = 10
        url = f"{self.base_url}/localizacoes/animal/{animal_id}?page={page}&size={size}"
        if sort_by: url += f"&sortBy={sort_by}"
        if direction: url += f"&direction={direction}"
        if data_inicio: url += f"&dataInicio={data_inicio}"
        if data_fim: url += f"&dataFim={data_fim}"

        headers = self._get_headers(token)

        try:
            response = req.get(url=url, headers=headers)
            if response.status_code == 404:
                raise ResourceNotFoundException(f"Recurso não encontrado na API Java. (Localizações animal {animal_id})")
            if response.status_code != 200:
                logger.error(f"[API ERROR] Buscar localizacoes do animal {animal_id}. Status: {response.status_code} / Response: {response.text[:300]}")
                return response.status_code, {}
            return response.status_code, response.json()
        except ResourceNotFoundException:
            raise
        except Exception as e:
            logger.exception(f"[EXCEPTION ERROR] Buscar localizacoes do animal {animal_id}")
            return 0, {}
