package com.petdex.api.view;

import com.petdex.api.application.services.mensageria.publisher.PublisherService;
import com.petdex.api.domain.contracts.dto.batimento.BatimentoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoMensageriaReqDTO;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


@RestController
@RequestMapping("/mensageria")
public class MensageriaController {

    private final PublisherService publisherService;

    public MensageriaController (PublisherService publisherService) {
        this.publisherService = publisherService;
    }

    @PostMapping
    public ResponseEntity<String> publicarMensagem (@RequestBody String mensagem) {
        publisherService.publish(mensagem);
        return new ResponseEntity<>(HttpStatus.OK);
    }

    @PostMapping("/batimento")
    public ResponseEntity<HttpStatus> publicarBatimento(@RequestBody BatimentoMensageriaReqDTO batimento) {
        publisherService.publicarBatimento(batimento);
        return new ResponseEntity<>(HttpStatus.OK);
    }

    @PostMapping("/localizacao")
    public ResponseEntity<HttpStatus> publicarLocalizacao (@RequestBody LocalizacaoMensageriaReqDTO localizacao) {
        publisherService.publicarLocalizacao(localizacao);
        return new ResponseEntity<>(HttpStatus.OK);
    }

   @PostMapping("/movimento")
    public ResponseEntity<HttpStatus> publicarMovimento(@RequestBody MovimentoMensageriaReqDTO movimento) {
        publisherService.publicarMovimento(movimento);
        return new ResponseEntity<>(HttpStatus.OK);
   }
}
