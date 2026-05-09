package com.petdex.api.domain.contracts.dto.movimento;

import com.petdex.api.domain.contracts.enums.TelemetryTypeEnum;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.*;

import java.util.Date;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class MovimentoPublisherDTO {


    @Schema(description = "Tipo do dado que vai ser inserido no pub/sub. Não é alterável.", example = "movement")
    private TelemetryTypeEnum type = TelemetryTypeEnum.MOVEMENT;

    @Schema(description = "Data e hora em que foi realizada a coleta do movimento", example = "2024-01-20T14:30:00.000+00:00", requiredMode = Schema.RequiredMode.REQUIRED)
    private Date data;

    @Schema(description = "Valor de aceleração no eixo X no momento da coleta em m/s²", example = "0.5", requiredMode = Schema.RequiredMode.REQUIRED)
    private Double acelerometroX;

    @Schema(description = "Valor de aceleração no eixo Y no momento da coleta em m/s²", example = "0.3", requiredMode = Schema.RequiredMode.REQUIRED)
    private Double acelerometroY;

    @Schema(description = "Valor de aceleração no eixo Z no momento da coleta em m/s²", example = "9.8", requiredMode = Schema.RequiredMode.REQUIRED)
    private Double acelerometroZ;

    @Schema(description = "Valor da rotação do giroscópio no eixo X no momento da coleta em graus/s", example = "0.1", requiredMode = Schema.RequiredMode.REQUIRED)
    private Double giroscopioX;

    @Schema(description = "Valor da rotação do giroscópio no eixo Y no momento da coleta em graus/s", example = "0.2", requiredMode = Schema.RequiredMode.REQUIRED)
    private Double giroscopioY;

    @Schema(description = "Valor da rotação do giroscópio no eixo Z no momento da coleta em graus/s", example = "0.05", requiredMode = Schema.RequiredMode.REQUIRED)
    private Double giroscopioZ;

    @Schema(description = "ID do animal que teve o movimento coletado", example = "507f1f77bcf86cd799439011", requiredMode = Schema.RequiredMode.REQUIRED)
    private String animal;

    @Schema(description = "ID da coleira que realizou a coleta do movimento do animal", example = "507f1f77bcf86cd799439011", requiredMode = Schema.RequiredMode.REQUIRED)
    private String coleira;
}
