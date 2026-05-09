package com.petdex.api.view;

import com.petdex.api.application.services.messaging.publisher.TelemetryPublisherService;
import com.petdex.api.application.contracts.dto.batimento.BatimentoPublisherDTO;
import com.petdex.api.application.contracts.dto.localizacao.LocalizacaoPublisherDTO;
import com.petdex.api.application.contracts.dto.movimento.MovimentoPublisherDTO;
import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@AllArgsConstructor
@RestController
@RequestMapping("/telemetria")
public class TelemetryPublisherController {

    private final TelemetryPublisherService telemetryPublisherService;

    @PostMapping("/batimento")
    public ResponseEntity<HttpStatus> publicarBatimento(@RequestBody BatimentoPublisherDTO batimento) {
        telemetryPublisherService.processarBatimento(batimento);
        return new ResponseEntity<>(HttpStatus.OK);
    }

    @PostMapping("/localizacao")
    public ResponseEntity<HttpStatus> publicarLocalizacao (@RequestBody LocalizacaoPublisherDTO localizacao) {
        telemetryPublisherService.processarLocalizacao(localizacao);
        return new ResponseEntity<>(HttpStatus.OK);
    }

   @PostMapping("/movimento")
    public ResponseEntity<HttpStatus> publicarMovimento(@RequestBody MovimentoPublisherDTO movimento) {
        telemetryPublisherService.processarMovimento(movimento);
        return new ResponseEntity<>(HttpStatus.OK);
   }
}
