package com.petdex.api.view.exception;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

import io.swagger.v3.oas.annotations.media.Schema;
import java.util.Date;

@Getter
@Setter
@Builder
@Schema(name = "Resposta de Erro", description = "Estrutura padrão para retorno de erros na API")
public class ErrorResponseDTO {

    @Schema(description = "Caminho (endpoint) onde o erro ocorreu", example = "/animais")
    private String path;

    @Schema(description = "Mensagem detalhada descrevendo o erro", example = "Requisição inválida ou dados ausentes.")
    private String message;

    @Schema(description = "Status de sucesso da operação (sempre false para erros)", example = "false")
    private boolean success;

    @Schema(description = "Data e hora exata em que o erro ocorreu", example = "2024-05-30T19:47:00.000+00:00")
    private Date timestamp;
}
