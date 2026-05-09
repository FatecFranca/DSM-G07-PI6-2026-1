package com.petdex.api.application.services.movimento;

import com.petdex.api.application.contracts.dto.movimento.MovimentoReqDTO;
import com.petdex.api.application.contracts.dto.movimento.MovimentoResDTO;
import com.petdex.api.application.contracts.dto.PageDTO;
import org.springframework.data.domain.Page;

public interface MovimentoService {
    MovimentoResDTO save(MovimentoReqDTO movimentoReq);
    MovimentoResDTO fidById(String movimentoId);
    Page<MovimentoResDTO> findAllByAnimalId(String animalId, PageDTO pageDTO);
    Page<MovimentoResDTO> findAllByColeiraId(String coleiraId, PageDTO pageDTO);
}
