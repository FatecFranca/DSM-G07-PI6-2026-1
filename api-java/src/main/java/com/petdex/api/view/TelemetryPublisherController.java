package com.petdex.api.view;

import com.petdex.api.application.services.messaging.publisher.TelemetryPublisherService;
import com.petdex.api.application.contracts.dto.batimento.BatimentoPublisherDTO;
import com.petdex.api.application.contracts.dto.localizacao.LocalizacaoPublisherDTO;
import com.petdex.api.application.contracts.dto.movimento.MovimentoPublisherDTO;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@AllArgsConstructor
@RestController
@Tag(name = "Telemetria", description = "Operações para publicação de dados de telemetria recebidos da coleira, que serão processados e salvos no banco de dados via mensageria (Google Cloud Pub/Sub).")
@RequestMapping("/telemetria")
public class TelemetryPublisherController {

    private final TelemetryPublisherService telemetryPublisherService;

    @Operation(
            summary = "Publicar batimento cardíaco",
            description = "Recebe os dados de um batimento cardíaco coletado pela coleira, processa a telemetria e a publica em um tópico do Google Cloud Pub/Sub para ser salva assincronamente no banco de dados MongoDB",
            tags = {"Telemetria"},
            requestBody = @io.swagger.v3.oas.annotations.parameters.RequestBody(
                    description = "Dados do batimento cardíaco que será publicado",
                    required = true,
                    content = @Content(
                            mediaType = "application/json",
                            schema = @Schema(implementation = BatimentoPublisherDTO.class)
                    )
            ),
            responses = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "Batimento cardíaco publicado e enviado para processamento com sucesso"
                    )
            }
    )
    @PostMapping("/batimento")
    public ResponseEntity<HttpStatus> publicarBatimento(@RequestBody BatimentoPublisherDTO batimento) {
        telemetryPublisherService.processarBatimento(batimento);
        return new ResponseEntity<>(HttpStatus.OK);
    }

    @Operation(
            summary = "Publicar localização",
            description = "Recebe os dados de geolocalização coletados pela coleira, processa e publica em um tópico do Google Cloud Pub/Sub para serem salvos assincronamente no banco de dados MongoDB, permitindo o acompanhamento do animal e notificações de saída de área segura",
            tags = {"Telemetria"},
            requestBody = @io.swagger.v3.oas.annotations.parameters.RequestBody(
                    description = "Dados de localização que serão publicados",
                    required = true,
                    content = @Content(
                            mediaType = "application/json",
                            schema = @Schema(implementation = LocalizacaoPublisherDTO.class)
                    )
            ),
            responses = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "Localização publicada e enviada para processamento com sucesso"
                    )
            }
    )
    @PostMapping("/localizacao")
    public ResponseEntity<HttpStatus> publicarLocalizacao (@RequestBody LocalizacaoPublisherDTO localizacao) {
        telemetryPublisherService.processarLocalizacao(localizacao);
        return new ResponseEntity<>(HttpStatus.OK);
    }

    @Operation(
            summary = "Publicar movimento (Acelerômetro/Giroscópio)",
            description = "Recebe os dados de movimentação do animal coletados pela coleira, realiza o processamento inicial e os publica em um tópico do Google Cloud Pub/Sub para armazenamento assíncrono no banco de dados MongoDB",
            tags = {"Telemetria"},
            requestBody = @io.swagger.v3.oas.annotations.parameters.RequestBody(
                    description = "Dados de movimentação que serão publicados",
                    required = true,
                    content = @Content(
                            mediaType = "application/json",
                            schema = @Schema(implementation = MovimentoPublisherDTO.class)
                    )
            ),
            responses = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "Movimento publicado e enviado para processamento com sucesso"
                    )
            }
    )
    @PostMapping("/movimento")
    public ResponseEntity<HttpStatus> publicarMovimento(@RequestBody MovimentoPublisherDTO movimento) {
        telemetryPublisherService.processarMovimento(movimento);
        return new ResponseEntity<>(HttpStatus.OK);
    }
}
