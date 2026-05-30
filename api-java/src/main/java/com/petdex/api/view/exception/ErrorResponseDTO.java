package com.petdex.api.view.exception;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

import java.util.Date;

@Getter
@Setter
@Builder
public class ErrorResponseDTO {
    private String path;
    private String message;
    private boolean success;
    private Date timestamp;
}
