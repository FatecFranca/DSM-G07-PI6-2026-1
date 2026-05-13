package com.petdex.api.application.contracts.enums;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;

public enum TelemetryTypeEnum {
    HEART_RATE("heart_rate"),
    LOCATION("location"),
    MOVEMENT("movement");

    private String type;

    TelemetryTypeEnum(String type) {
        this.type = type;
    }

    @JsonValue
    public String getType() {
        return type;
    }

    @JsonCreator
    public static TelemetryTypeEnum fromString(String value) {
        for (TelemetryTypeEnum t : TelemetryTypeEnum.values()) {
            if (t.type.equalsIgnoreCase(value)) {
                return t;
            }
        }
        throw new IllegalArgumentException("Tipo inválido: " + value);
    }
}
