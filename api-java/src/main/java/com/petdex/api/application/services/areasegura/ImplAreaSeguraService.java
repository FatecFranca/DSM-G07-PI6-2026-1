package com.petdex.api.application.services.areasegura;

import com.petdex.api.domain.collections.AreaSegura;
import com.petdex.api.application.contracts.dto.areasegura.AreaSeguraReqDTO;
import com.petdex.api.application.contracts.dto.areasegura.AreaSeguraResDTO;
import com.petdex.api.application.services.ValidationService;
import com.petdex.api.infrastructure.exception.ResourceNotFoundException;
import com.petdex.api.infrastructure.mongodb.AreaSeguraRepository;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.Date;
import java.util.Optional;

/**
 * Serviço para gerenciamento de áreas seguras e cálculo de distâncias geográficas
 */
@Service
public class ImplAreaSeguraService implements AreaSeguraService {

    private static final Logger logger = LoggerFactory.getLogger(ImplAreaSeguraService.class);

    @Autowired
    private AreaSeguraRepository areaSeguraRepository;

    @Autowired
    private ModelMapper mapper;

    @Autowired
    private ValidationService validation;

    // Raio da Terra em metros (usado na fórmula de Haversine)
    private static final double RAIO_TERRA_METROS = 6371000.0;

    @Override
    public AreaSeguraResDTO createOrUpdate(AreaSeguraReqDTO areaSeguraReq) {
        if (!validation.existAnimal(areaSeguraReq.getAnimal())) {
            logger.error("Falha ao configurar área segura: Animal ID {} não encontrado", areaSeguraReq.getAnimal());
            throw new ResourceNotFoundException("Animal", "ID", areaSeguraReq.getAnimal());
        }

        try {
            Optional<AreaSegura> areaExistente = areaSeguraRepository.findByAnimal(areaSeguraReq.getAnimal());
            
            AreaSegura areaSegura;
            if (areaExistente.isPresent()) {
                areaSegura = areaExistente.get();
                areaSegura.setLatitude(areaSeguraReq.getLatitude());
                areaSegura.setLongitude(areaSeguraReq.getLongitude());
                areaSegura.setRaio(areaSeguraReq.getRaio());
                areaSegura.setDataAtualizacao(new Date());
            } else {
                areaSegura = mapper.map(areaSeguraReq, AreaSegura.class);
            }
            
            AreaSegura areaSalva = areaSeguraRepository.save(areaSegura);
            logger.info("Área segura configurada com sucesso para o animal: {}", areaSeguraReq.getAnimal());
            return mapper.map(areaSalva, AreaSeguraResDTO.class);
        } catch (Exception e) {
            logger.error("Erro ao criar ou atualizar área segura para o animal: {}", areaSeguraReq.getAnimal(), e);
            throw e;
        }
    }

    @Override
    public Optional<AreaSeguraResDTO> findByAnimalId(String animalId) {
        Optional<AreaSegura> areaSegura = areaSeguraRepository.findByAnimal(animalId);
        if (areaSegura.isEmpty()) {
            logger.warn("Área segura não encontrada para o animal ID: {}", animalId);
        }
        return areaSegura.map(area -> mapper.map(area, AreaSeguraResDTO.class));
    }

    @Override
    public AreaSeguraResDTO findById(String id) {
        Optional<AreaSegura> areaSegura = areaSeguraRepository.findById(id);
        return areaSegura.map(area -> mapper.map(area, AreaSeguraResDTO.class)).orElseGet(() -> {
            logger.error("Área segura não encontrada com ID: {}", id);
            return null;
        });
    }

    @Override
    public void deleteByAnimalId(String animalId) {
        areaSeguraRepository.deleteByAnimal(animalId);
    }

    @Override
    public double calcularDistanciaEmMetros(double lat1, double lon1, double lat2, double lon2) {
        double lat1Rad = Math.toRadians(lat1);
        double lon1Rad = Math.toRadians(lon1);
        double lat2Rad = Math.toRadians(lat2);
        double lon2Rad = Math.toRadians(lon2);

        double deltaLat = lat2Rad - lat1Rad;
        double deltaLon = lon2Rad - lon1Rad;

        double a = Math.sin(deltaLat / 2) * Math.sin(deltaLat / 2) +
                   Math.cos(lat1Rad) * Math.cos(lat2Rad) *
                   Math.sin(deltaLon / 2) * Math.sin(deltaLon / 2);
        
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

        return RAIO_TERRA_METROS * c;
    }

    @Override
    public boolean isForaDaAreaSegura(String animalId, double latitude, double longitude) {
        Optional<AreaSegura> areaSeguraOpt = areaSeguraRepository.findByAnimal(animalId);
        
        if (areaSeguraOpt.isEmpty()) {
            return false;
        }
        
        AreaSegura areaSegura = areaSeguraOpt.get();
        
        double distancia = calcularDistanciaEmMetros(
            areaSegura.getLatitude(),
            areaSegura.getLongitude(),
            latitude,
            longitude
        );
        
        return distancia > areaSegura.getRaio();
    }
}
