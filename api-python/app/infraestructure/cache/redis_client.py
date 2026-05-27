import os
import redis
import json
import logging
from typing import Any, Optional

logger = logging.getLogger("RedisClient")

class RedisClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        host = os.environ.get("REDIS_HOST", "localhost")
        port = int(os.environ.get("REDIS_PORT", 6379))
        self.default_ttl = int(os.environ.get("CACHE_TTL_MINUTES", 10)) * 60

        try:
            pool = redis.ConnectionPool(host=host, port=port, decode_responses=True)
            self.client = redis.Redis(connection_pool=pool)
            self.client.ping()
            logger.info(f"Conectado ao Redis em {host}:{port}")
        except Exception as e:
            logger.error(f"Erro ao conectar no Redis: {e}")
            self.client = None

    def get(self, key: str) -> Optional[Any]:
        if not self.client:
            return None
        try:
            data = self.client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"Erro ao ler chave {key} no Redis: {e}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        if not self.client:
            return False
        try:
            ttl = ttl if ttl is not None else self.default_ttl
            self.client.set(key, json.dumps(value), ex=ttl)
            return True
        except Exception as e:
            logger.error(f"Erro ao escrever chave {key} no Redis: {e}")
            return False
