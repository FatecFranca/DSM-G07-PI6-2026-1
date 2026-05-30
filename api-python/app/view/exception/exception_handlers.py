from datetime import datetime, timezone
from fastapi import Request, FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel
from app.infraestructure.exception.custom_exceptions import ResourceNotFoundException, BadRequestException, ConflictException

class ErrorResponseDTO(BaseModel):
    path: str
    message: str
    success: bool
    timestamp: datetime

def build_error_response(status_code: int, message: str, request: Request) -> JSONResponse:
    content = ErrorResponseDTO(
        path=request.url.path,
        message=message,
        success=False,
        timestamp=datetime.now(timezone.utc)
    ).model_dump(mode='json')
    return JSONResponse(status_code=status_code, content=content)

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(ResourceNotFoundException)
    async def resource_not_found_handler(request: Request, exc: ResourceNotFoundException):
        return build_error_response(status.HTTP_404_NOT_FOUND, exc.message, request)

    @app.exception_handler(BadRequestException)
    async def bad_request_handler(request: Request, exc: BadRequestException):
        return build_error_response(status.HTTP_400_BAD_REQUEST, exc.message, request)

    @app.exception_handler(ConflictException)
    async def conflict_handler(request: Request, exc: ConflictException):
        return build_error_response(status.HTTP_400_BAD_REQUEST, "Não foi possível realizar o cadastro pois já existe um registro correspondente na base de dados.", request)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            loc = " -> ".join([str(l) for l in error.get("loc", [])])
            errors.append(f"{loc}: {error.get('msg')}")
        message = "Erros de validação - " + "; ".join(errors)
        return build_error_response(status.HTTP_400_BAD_REQUEST, message, request)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        message = exc.detail if isinstance(exc.detail, str) else "Erro HTTP"
        if exc.status_code == 404 and message == "Not Found":
            message = "Endpoint não encontrado."
        elif exc.status_code == 401:
            message = "Não autorizado: Autenticação necessária ou inválida."
        elif exc.status_code == 403:
            message = "Acesso negado: Você não tem permissão para acessar este recurso."
            
        return build_error_response(exc.status_code, message, request)

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return build_error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ocorreu um erro interno inesperado no servidor.", request)
