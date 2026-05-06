package com.petdex.api.application.services.mensageria.subscriber;

import com.petdex.api.domain.contracts.dto.batimento.BatimentoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoMensageriaReqDTO;
import org.springframework.stereotype.Service;


public interface SubscriberService {

    boolean processarBatimento(BatimentoMensageriaReqDTO batimento);
    boolean processarLocalizacao(LocalizacaoMensageriaReqDTO localizacao);
    boolean processarMovimento(MovimentoMensageriaReqDTO movimento);
}
