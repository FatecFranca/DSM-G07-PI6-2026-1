from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import os

app = FastAPI(
    title="API PetDex - Estatísticas",
    description="API para exibir dados e estatísticas dos batimentos cardíacos dos animais monitorados pela coleira inteligente",
    version="1.0.0"
)

def custom_openapi():
    """
    Customiza o esquema OpenAPI para incluir a documentação de autenticação JWT.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="API PetDex - Estatísticas",
        version="1.0.0",
        description="""
        API para exibir dados e estatísticas dos batimentos cardíacos dos animais monitorados pela coleira inteligente.

        ## Autenticação JWT

        Esta API utiliza **JWT (JSON Web Tokens)** para autenticação. Todos os endpoints (exceto `/health`) requerem um token JWT válido.

        ### Como usar:

        1. **Obtenha um token JWT** da API Java (endpoint de login)
        2. **Inclua o token** no header `Authorization` com o formato: `Bearer <seu_token_jwt>`
        3. **Exemplo de requisição:**
           ```
           GET /batimentos/animal/123/estatisticas HTTP/1.1
           Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
           ```

        ### Respostas de erro de autenticação:

        - **401 Unauthorized**: Token ausente, inválido ou expirado
        - **401 Unauthorized**: Formato de header inválido (use `Bearer <token>`)

        ### Fluxo de autenticação:

        1. Cliente faz requisição com token JWT no header `Authorization`
        2. Python API valida o token
        3. Se válido, Python API propaga o mesmo token para a API Java
        4. Requisição é processada com o contexto de autenticação mantido
        """,
        routes=app.routes,
    )

    # Adiciona a definição de segurança Bearer (preservando os schemas existentes)
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}

    openapi_schema["components"]["securitySchemes"]["Bearer"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "Token JWT obtido da API Java. Formato: Bearer <token>"
    }

    # Aplica a segurança Bearer a todos os endpoints (exceto /health)
    for path, path_item in openapi_schema["paths"].items():
        if path != "/health":
            for method in path_item:
                if method in ["get", "post", "put", "delete", "patch"]:
                    if "security" not in path_item[method]:
                        path_item[method]["security"] = [{"Bearer": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# --------------------- Health ---------------------


@app.get(
    "/health",
    tags=["Status"],
    summary="Verificar status da API",
    description="Verifica se a API está operacional e respondendo corretamente.\n\n**Não requer autenticação.**",
    responses={
        200: {
            "description": "API está operacional",
            "content": {
                "application/json": {
                    "example": {"status": "Ok"}
                }
            }
        }
    }
)
async def health_check():
    """
    Verifica o status da API.

    **Não requer autenticação.**

    Returns:
        dict: Status da API
    """
    return {"status": "Ok"}


# --------------------- Roteadores (DDD Controllers) ---------------------
from app.view import checkup_router, estatistica_router, recomendacao_router

app.include_router(checkup_router)
app.include_router(estatistica_router)
app.include_router(recomendacao_router)