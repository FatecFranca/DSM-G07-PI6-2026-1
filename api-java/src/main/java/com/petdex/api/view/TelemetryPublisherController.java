package com.petdex.api.view;

import com.petdex.api.application.services.mensageria.publisher.TelemetryPublisherService;
import com.petdex.api.domain.contracts.dto.batimento.BatimentoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoMensageriaReqDTO;
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
    public ResponseEntity<HttpStatus> publicarBatimento(@RequestBody BatimentoMensageriaReqDTO batimento) {
        telemetryPublisherService.publicarBatimento(batimento);
        return new ResponseEntity<>(HttpStatus.OK);
    }

    @PostMapping("/localizacao")
    public ResponseEntity<HttpStatus> publicarLocalizacao (@RequestBody LocalizacaoMensageriaReqDTO localizacao) {
        telemetryPublisherService.publicarLocalizacao(localizacao);
        return new ResponseEntity<>(HttpStatus.OK);
    }

   @PostMapping("/movimento")
    public ResponseEntity<HttpStatus> publicarMovimento(@RequestBody MovimentoMensageriaReqDTO movimento) {
        telemetryPublisherService.publicarMovimento(movimento);
        return new ResponseEntity<>(HttpStatus.OK);
   }
}
