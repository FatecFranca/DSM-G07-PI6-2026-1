package com.petdex.api.application.services.websocket.interfaces;

import com.petdex.api.domain.contracts.dto.websocket.BatimentoWebSocketDTO;
import com.petdex.api.domain.contracts.dto.websocket.LocalizacaoWebSocketDTO;

public interface NotificationService {
    void enviarNotificacaoLocalizacao(String animalId, LocalizacaoWebSocketDTO localizacaoDTO);
    void enviarNotificacaoBatimento(String animalId, BatimentoWebSocketDTO batimentoDTO);
}
