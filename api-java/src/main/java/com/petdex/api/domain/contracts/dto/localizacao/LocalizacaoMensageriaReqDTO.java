package com.petdex.api.domain.contracts.dto.localizacao;

import com.petdex.api.domain.contracts.enums.TelemetryTypeEnum;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.*;

import java.util.Date;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class LocalizacaoMensageriaReqDTO {

    @Schema(description = "Tipo do dado que vai ser inserido no pub/sub. Não é alterável.", example = "location")
    private TelemetryTypeEnum type = TelemetryTypeEnum.LOCATION;

    @Schema(description = "Data e hora em que foi realizada a coleta da localização", example = "2024-01-20T14:30:00.000+00:00", requiredMode = Schema.RequiredMode.REQUIRED)
    private Date data;

    @Schema(description = "Latitude da posição geográfica onde o animal se encontra no momento da coleta", example = "-23.550520", requiredMode = Schema.RequiredMode.REQUIRED)
    private Double latitude;

    @Schema(description = "Longitude da posição geográfica onde o animal se encontra no momento da coleta", example = "-46.633308", requiredMode = Schema.RequiredMode.REQUIRED)
    private Double longitude;

    @Schema(description = "ID do animal que teve a localização coletada", example = "507f1f77bcf86cd799439011", requiredMode = Schema.RequiredMode.REQUIRED)
    private String animal;

    @Schema(description = "ID da coleira que realizou a coleta da localização do animal", example = "507f1f77bcf86cd799439011", requiredMode = Schema.RequiredMode.REQUIRED)
    private String coleira;
}
