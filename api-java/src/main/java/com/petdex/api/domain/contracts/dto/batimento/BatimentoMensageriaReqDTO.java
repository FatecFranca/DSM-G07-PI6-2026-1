package com.petdex.api.domain.contracts.dto.batimento;

import com.petdex.api.domain.contracts.enums.TelemetryTypeEnum;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.*;

import java.util.Date;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class BatimentoMensageriaReqDTO {

    @Schema(description = "Tipo do dado que vai ser inserido no pub/sub", example = "heart_rate")
    private TelemetryTypeEnum type = TelemetryTypeEnum.HEART_RATE;

    @Schema(description = "Data e hora em que foi coletado o batimento cardíaco", example = "2024-01-20T14:30:00.000+00:00", requiredMode = Schema.RequiredMode.REQUIRED)
    private Date data;

    @Schema(description = "Frequência cardíaca média coletada do animal em batimentos por minuto (BPM)", example = "75", requiredMode = Schema.RequiredMode.REQUIRED)
    private Integer frequenciaMedia;

    @Schema(description = "ID do animal que teve o batimento cardíaco coletado", example = "507f1f77bcf86cd799439011", requiredMode = Schema.RequiredMode.REQUIRED)
    private String animal;

    @Schema(description = "ID da coleira que realizou a coleta do batimento cardíaco", example = "507f1f77bcf86cd799439011", requiredMode = Schema.RequiredMode.REQUIRED)
    private String coleira;

}
