package com.petdex.api.application.services.raca;

import com.petdex.api.domain.collections.Especie;
import com.petdex.api.domain.collections.Raca;
import com.petdex.api.application.contracts.dto.PageDTO;
import com.petdex.api.application.contracts.dto.raca.RacaReqDTO;
import com.petdex.api.application.contracts.dto.raca.RacaResDTO;
import com.petdex.api.infrastructure.mongodb.EspecieRepository;
import com.petdex.api.infrastructure.mongodb.RacaRepository;
import com.petdex.api.infrastructure.exception.ResourceNotFoundException;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ImplRacaService implements RacaService {

    @Autowired
    ModelMapper mapper;

    @Autowired
    RacaRepository racaRepository;

    @Autowired
    EspecieRepository especieRepository;

    @Override
    public RacaResDTO findById(String id) {
        return mapper.map(racaRepository.findById(id), RacaResDTO.class);
    }

    @Override
    public Page<RacaResDTO> findAll(PageDTO pageDTO) {

        pageDTO.sortByName();

        Page<Raca> racaPage = racaRepository.findAll(pageDTO.mapPage());
        List<RacaResDTO> dtoList = racaPage.getContent().stream()
                .map(r -> mapper.map(r, RacaResDTO.class))
                .toList();


        return new PageImpl<RacaResDTO>(dtoList, pageDTO.mapPage(), racaPage.getTotalElements());
    }

    @Override
    public RacaResDTO create(RacaReqDTO racaReqDTO) {

        Especie especie = especieRepository.findById(racaReqDTO.getEspecie()).orElseThrow(() -> new ResourceNotFoundException("Espécie", "ID", racaReqDTO.getEspecie()));
        return mapper.map(racaRepository.save(mapper.map(racaReqDTO, Raca.class)), RacaResDTO.class);
    }

    @Override
    public RacaResDTO update(String id, RacaReqDTO racaReqDTO) {

        Raca racaUptade = racaRepository.findById(id).orElseThrow(()->new ResourceNotFoundException("Raça", "ID", id));

        if(racaReqDTO.getNome() != null) racaUptade.setNome(racaReqDTO.getNome());
        if(racaReqDTO.getEspecie()!=null) {
            Especie especie = especieRepository.findById(racaReqDTO.getEspecie()).orElseThrow(() -> new ResourceNotFoundException("Espécie", "ID", racaReqDTO.getEspecie()));
            racaUptade.setEspecie(racaReqDTO.getEspecie());
        }

        return mapper.map(racaRepository.save(racaUptade), RacaResDTO.class);
    }

    @Override
    public Page<RacaResDTO> findAllByEspecieId(String especieId, PageDTO pageDTO) {

        // Buscar TODAS as raças do banco
        List<Raca> todasRacas = racaRepository.findAll();

        // Filtrar manualmente as raças que pertencem à espécie
        List<Raca> racasFiltradas = todasRacas.stream()
                .filter(raca -> {
                    return raca.getEspecie() != null && raca.getEspecie().equals(especieId);
                })
                .toList();

        // Ordenar manualmente por nome
        List<Raca> racasOrdenadas = racasFiltradas.stream()
                .sorted((r1, r2) -> r1.getNome().compareToIgnoreCase(r2.getNome()))
                .toList();

        // Aplicar paginação manual
        int page = pageDTO.getPage();
        int size = pageDTO.getSize();
        int start = page * size;
        int end = Math.min(start + size, racasOrdenadas.size());

        List<Raca> racasPaginadas = (start < racasOrdenadas.size())
                ? racasOrdenadas.subList(start, end)
                : List.of();

        // Converter para DTO
        List<RacaResDTO> dtoList = racasPaginadas.stream()
                .map(r -> mapper.map(r, RacaResDTO.class))
                .toList();

        return new PageImpl<>(dtoList, pageDTO.mapPage(), racasOrdenadas.size());
    }

    @Override
    public void delete(String id) {
       Raca racaDelete =  racaRepository.findById(id)
               .orElseThrow(() -> new ResourceNotFoundException("Raça", "ID", id));
       racaRepository.delete(racaDelete);
    }
}
