package com.petdex.api.application.services.especie;

import com.petdex.api.domain.collections.Especie;
import com.petdex.api.domain.contracts.dto.PageDTO;
import com.petdex.api.domain.contracts.dto.especie.EspecieReqDTO;
import com.petdex.api.domain.contracts.dto.especie.EspecieResDTO;
import com.petdex.api.infrastructure.mongodb.EspecieRepository;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ImplEspecieService implements EspecieService {

    private static final Logger logger = LoggerFactory.getLogger(ImplEspecieService.class);

    @Autowired
    ModelMapper mapper;

    @Autowired
    EspecieRepository especieRepository;

    @Override
    public EspecieResDTO findById(String id) {
        return especieRepository.findById(id)
                .map(especie -> mapper.map(especie, EspecieResDTO.class))
                .orElseGet(() -> {
                    logger.error("Espécie não encontrada com ID: {}", id);
                    return null;
                });
    }

    @Override
    public Page<EspecieResDTO> findAll(PageDTO pageDTO) {

        pageDTO.sortByName();

        Page<Especie> especiesPage = especieRepository.findAll(pageDTO.mapPage());

        List<EspecieResDTO> dtoList = especiesPage.getContent().stream()
                .map(e -> mapper.map(e, EspecieResDTO.class))
                .toList();

        return new PageImpl<EspecieResDTO>(dtoList, pageDTO.mapPage(), especiesPage.getTotalElements());
    }

    @Override
    public EspecieResDTO create(EspecieReqDTO especieReqDTO) {
        return mapper.map(especieRepository.save(mapper.map(especieReqDTO, Especie.class)), EspecieResDTO.class);
    }

    @Override
    public EspecieResDTO update(String id, EspecieReqDTO especieReqDTO) {

        Especie especieUptade = especieRepository.findById(id).orElseThrow(() -> {
            logger.error("Falha ao atualizar espécie: ID {} não encontrado", id);
            return new RuntimeException("Não existe especie com esse ID: " + id);
        });
        if(especieReqDTO.getNome() != null) especieUptade.setNome(especieReqDTO.getNome());

        return mapper.map(especieRepository.save(especieUptade), EspecieResDTO.class);
    }

    @Override
    public void delete(String id) {

        Especie especieDelete = especieRepository.findById(id).orElseThrow(() -> new RuntimeException("Não existe especie com esse ID: " + id));

        especieRepository.delete(especieDelete);
    }
}
