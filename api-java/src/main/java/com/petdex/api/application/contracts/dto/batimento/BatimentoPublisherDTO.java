package com.petdex.api.application.contracts.dto.batimento;

import com.petdex.api.application.contracts.enums.TelemetryTypeEnum;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.*;

import java.util.Date;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class BatimentoPublisherDTO {

    @Schema(description = "Tipo do dado que vai ser inserido no pub/sub", example = "heart_rate")
    private TelemetryTypeEnum type = TelemetryTypeEnum.HEART_RATE;

    @Schema(description = "Data e hora em que foi coletado o batimento cardíaco", example = "2024-01-20T14:30:00.000+00:00", requiredMode = Schema.RequiredMode.REQUIRED)
    private Date data;

    @Schema(description = "Frequência cardíaca média coletada do animal em batimentos por minuto (BPM)", example = "75", requiredMode = Schema.RequiredMode.REQUIRED)
    private Integer frequenciaMedia;

    @Schema(description = "ID do animal que teve o batimento cardíaco coletado", example = "68194120636f719fcd5ee5fd", requiredMode = Schema.RequiredMode.REQUIRED)
    private String animal;

    @Schema(description = "ID da coleira que realizou a coleta do batimento cardíaco", example = "6819475baa479949daccea94", requiredMode = Schema.RequiredMode.REQUIRED)
    private String coleira;

}
