import logging
import requests as req
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("API Java Integration")

class JavaAPIClient:
    def __init(self) -> tuple[int, dict]:
        self.base_url = os.getenv("API_URL", "localhost:8080")

    def _get_headers(self, token: str) -> dict:
        return {"Authorization": f"Bearer {token}"}

    def get_animal(self, animal_id: str, token: str):

        url = f"{self.base_url}/animais/{animal_id}"
        headers = self._get_headers(token)

        try:
            response = req.get(url=url, headers=headers)
            if response.status_code != 200:
                logger.error(f"[API ERROR] Buscar dados do animal {animal_id}. Status: {response.status_code} / Response: {response.text[:300]}")
                return response.status_code, {}
            return response.status_code, response.json()

        except Exception as e:
            logger.exception(f"[EXCEPTION ERROR] Buscar os dados do animal: {animal_id}")
            return 0, {}

    def get_animal_ultimo_batimento(self, animal_id: str, token: str) -> tuple[int, dict]:
        
        url = f"{self.base_url}/batimentos/animal/{animal_id}/ultimo"
        headers = self._get_headers(token)
        
        try:
            response = req.get(url=url, headers=headers)
            if response.status_code != 200:
                logger.error(f"[API ERROR] Último baitmento do animal {animal_id}. Status: {response.status_code} / Response: {response.text[:300]}")
                return response.status_code, response.json()
            return response.status_code, response.json()
        except Exception as e:
            logger.exception(f"[EXCEPTION ERROR] Último batimento do animal {animal_id}")
            return 0, {}
    
    def get_animal_batimentos(self, animal_id: str, token: str, page: int = 0, size: int = 10) -> tuple[int,dict]:
        if not size:
            size = 10
    
        url = f"{self.base_url}/batimentos/animal/{animal_id}?page={page}&size={size}"
        headers = self._get_headers(token)
        try:
            response = req.get(url=url, headers=headers)
            if response.status_code != 200:
                logger.error(f"[API ERROR] Buscar baitmentos do animal {animal_id}. Status: {response.status_code} / Response: {response.text[:300]}")
                
                return response.status_code, {}
            return response.status_code, response.json()

        except Exception as e:
            logger.exception(f"[EXCEPTION ERROR] Buscar batimentos do animal {animal_id}")
            return 0, {}
        
    
    def get_animal_movimentos(self, animal_id: str, token:str, page: int = 0, size: int = 10) -> tuple[int,dict]:
        if not size:
            size = 10
        url = f"{self.base_url}/movimentos/animal/{animal_id}?page={page}&size={size}"
        headers = self._get_headers(token)

        try:
            response = req.get(url=url, headers=headers)
            if response.status_code != 200:
                logger.error(f"[API ERROR] Buscar movimentos do animal {animal_id}. Status: {response.status_code} / Response: {response.text[:300]}")
                return response.status_code, {}
            return response.status_code, response.json()
        except Exception as e:
            logger.exception(f"[EXCEPTION ERROR] Buscar movimentos do animal {animal_id}")
            return 0, {}
