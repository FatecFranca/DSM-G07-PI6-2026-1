package com.petdex.api.application.services.localizacao;

import com.petdex.api.application.contracts.dto.localizacao.LocalizacaoReqDTO;
import com.petdex.api.application.contracts.dto.localizacao.LocalizacaoResDTO;
import com.petdex.api.application.contracts.dto.PageDTO;
import org.springframework.data.domain.Page;

import java.util.Optional;
import java.time.LocalDate;

public interface LocalizacaoService {
    LocalizacaoResDTO save(LocalizacaoReqDTO localizacaoReq);
    LocalizacaoResDTO fidById(String localizacaoId);
    Page<LocalizacaoResDTO> findAllByAnimalId(String animalId, LocalDate dataInicio, LocalDate dataFim, PageDTO pageDTO);
    Page<LocalizacaoResDTO> findAllByColeiraId(String coleiraId, LocalDate dataInicio, LocalDate dataFim, PageDTO pageDTO);
    Optional<LocalizacaoResDTO> findLastByAnimalId(String animalId);
}
