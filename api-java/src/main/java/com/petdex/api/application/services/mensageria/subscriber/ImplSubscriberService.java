package com.petdex.api.application.services.mensageria.subscriber;

import com.petdex.api.domain.contracts.dto.batimento.BatimentoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoMensageriaReqDTO;
import org.springframework.stereotype.Service;

@Service
public class ImplSubscriberService implements SubscriberService{
    @Override
    public boolean processarBatimento(BatimentoMensageriaReqDTO batimento) {
        System.out.println("Batimento recebido: " + batimento);
        return false;
    }

    @Override
    public boolean processarLocalizacao(LocalizacaoMensageriaReqDTO localizacao) {
        System.out.println("Localizacao recebido: " + localizacao);
        return false;
    }

    @Override
    public boolean processarMovimento(MovimentoMensageriaReqDTO movimento) {
        System.out.println("Movimento recebido: " + movimento);
        return false;
    }
}
