package com.petdex.api.application.contracts.websocket;

import com.petdex.api.application.contracts.dto.websocket.BatimentoWebSocketDTO;
import com.petdex.api.application.contracts.dto.websocket.LocalizacaoWebSocketDTO;

public interface NotificationService {
    void enviarNotificacaoLocalizacao(String animalId, LocalizacaoWebSocketDTO localizacaoDTO);
    void enviarNotificacaoBatimento(String animalId, BatimentoWebSocketDTO batimentoDTO);
}
