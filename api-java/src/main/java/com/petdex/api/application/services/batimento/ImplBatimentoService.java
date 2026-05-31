package com.petdex.api.application.services.batimento;

import com.petdex.api.application.services.ValidationService;
import com.petdex.api.application.contracts.websocket.NotificationService;
import com.petdex.api.domain.collections.Batimento;
import com.petdex.api.application.contracts.dto.batimento.BatimentoReqDTO;
import com.petdex.api.application.contracts.dto.batimento.BatimentoResDTO;
import com.petdex.api.application.contracts.dto.PageDTO;
import com.petdex.api.application.contracts.dto.websocket.BatimentoWebSocketDTO;
import com.petdex.api.infrastructure.exception.ResourceNotFoundException;
import com.petdex.api.infrastructure.mongodb.BatimentoRepository;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ImplBatimentoService implements BatimentoService {

    private static final Logger logger = LoggerFactory.getLogger(ImplBatimentoService.class);

    @Autowired
    private BatimentoRepository batimentoRepository;

    @Autowired
    private ValidationService validation;

    @Autowired
    private ModelMapper mapper;

    @Autowired
    private NotificationService notificationService;

    public BatimentoResDTO save(BatimentoReqDTO batimentoReq) {

        if (!validation.existAnimal(batimentoReq.getAnimal())) {
            logger.error("Falha ao salvar batimento: Animal ID {} não encontrado", batimentoReq.getAnimal());
            throw new ResourceNotFoundException("Animal", "ID", batimentoReq.getAnimal());
        }
        
        if (!validation.existColeira(batimentoReq.getColeira())) {
            logger.error("Falha ao salvar batimento: Coleira ID {} não encontrada", batimentoReq.getColeira());
            throw new ResourceNotFoundException("Coleira", "ID", batimentoReq.getColeira());
        }

        Batimento batimentoSalvo = batimentoRepository.save(mapper.map(batimentoReq, Batimento.class));
        BatimentoResDTO batimentoResDTO = mapper.map(batimentoSalvo, BatimentoResDTO.class);

        BatimentoWebSocketDTO webSocketDTO = new BatimentoWebSocketDTO(
                batimentoReq.getAnimal(),
                batimentoReq.getColeira(),
                batimentoReq.getFrequenciaMedia(),
                batimentoReq.getData()
        );

        notificationService.enviarNotificacaoBatimento(
                batimentoReq.getAnimal(),
                webSocketDTO
        );

        return batimentoResDTO;
    }

    public BatimentoResDTO fidById(String batimentoId) {
        return batimentoRepository.findById(batimentoId)
                .map(batimento -> mapper.map(batimento, BatimentoResDTO.class))
                .orElseThrow(() -> {
                    logger.error("Batimento não encontrado com ID: {}", batimentoId);
                    return new ResourceNotFoundException("Batimento", "ID", batimentoId);
                });
    }

    public Page<BatimentoResDTO> findAllByAnimalId(String animalId, PageDTO pageDTO) {
        pageDTO.sortByNewest();
        Page<Batimento> batimentosPage = batimentoRepository.findAllByAnimal(animalId, pageDTO.mapPage());

        List<BatimentoResDTO> dtoList = batimentosPage.getContent().stream()
                .map(b -> mapper.map(b, BatimentoResDTO.class))
                .toList();

        return new PageImpl<BatimentoResDTO>(dtoList, pageDTO.mapPage(), batimentosPage.getTotalElements());
    }

    public Page<BatimentoResDTO> findAllByColeiraId(String coleiraId, PageDTO pageDTO) {
        pageDTO.sortByNewest();
        Page<Batimento> batimentosPage = batimentoRepository.findAllByColeira(coleiraId, pageDTO.mapPage());

        List<BatimentoResDTO> dtoList = batimentosPage.getContent().stream()
                .map(b -> mapper.map(b, BatimentoResDTO.class))
                .toList();

        return new PageImpl<BatimentoResDTO>(dtoList, pageDTO.mapPage(), batimentosPage.getTotalElements());
    }

    @Override
    public Optional<BatimentoResDTO> findLastByAnimalId(String animalId) {
        Optional<Batimento> ultimoBatimento = batimentoRepository.findFirstByAnimalOrderByDataDesc(animalId);
        return ultimoBatimento.map(batimento -> mapper.map(batimento, BatimentoResDTO.class));
    }

}
