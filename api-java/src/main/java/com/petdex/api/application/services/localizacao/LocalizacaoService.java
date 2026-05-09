package com.petdex.api.application.services.localizacao;

import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoReqDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoResDTO;
import com.petdex.api.domain.contracts.dto.PageDTO;
import org.springframework.data.domain.Page;

import java.util.Optional;

public interface LocalizacaoService {
    LocalizacaoResDTO save(LocalizacaoReqDTO localizacaoReq);
    LocalizacaoResDTO fidById(String localizacaoId);
    Page<LocalizacaoResDTO> findAllByAnimalId(String animalId, PageDTO pageDTO);
    Page<LocalizacaoResDTO> findAllByColeiraId(String coleiraId, PageDTO pageDTO);
    Optional<LocalizacaoResDTO> findLastByAnimalId(String animalId);
}
