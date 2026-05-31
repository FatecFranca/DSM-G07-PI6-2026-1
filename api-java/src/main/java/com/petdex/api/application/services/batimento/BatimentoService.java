package com.petdex.api.application.services.batimento;

import com.petdex.api.application.contracts.dto.batimento.BatimentoReqDTO;
import com.petdex.api.application.contracts.dto.batimento.BatimentoResDTO;
import com.petdex.api.application.contracts.dto.PageDTO;
import org.springframework.data.domain.Page;

import java.util.Optional;
import java.time.LocalDate;

public interface BatimentoService {

     BatimentoResDTO save(BatimentoReqDTO batimentoReq);
     BatimentoResDTO fidById(String batimentoId);
     Page<BatimentoResDTO> findAllByAnimalId(String animalId, LocalDate dataInicio, LocalDate dataFim, PageDTO pageDTO);
     Page<BatimentoResDTO> findAllByColeiraId(String coleiraId, LocalDate dataInicio, LocalDate dataFim, PageDTO pageDTO);
     Optional<BatimentoResDTO> findLastByAnimalId(String animalId);

}
