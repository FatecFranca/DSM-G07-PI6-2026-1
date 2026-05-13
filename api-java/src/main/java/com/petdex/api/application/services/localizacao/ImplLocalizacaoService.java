package com.petdex.api.application.services.localizacao;

import com.petdex.api.application.services.ValidationService;
import com.petdex.api.application.services.areasegura.AreaSeguraService;
import com.petdex.api.application.contracts.websocket.NotificationService;
import com.petdex.api.domain.collections.Localizacao;
import com.petdex.api.application.contracts.dto.areasegura.AreaSeguraResDTO;
import com.petdex.api.application.contracts.dto.localizacao.LocalizacaoReqDTO;
import com.petdex.api.application.contracts.dto.localizacao.LocalizacaoResDTO;
import com.petdex.api.application.contracts.dto.PageDTO;
import com.petdex.api.application.contracts.dto.websocket.LocalizacaoWebSocketDTO;
import com.petdex.api.infrastructure.exception.ResourceNotFoundException;
import com.petdex.api.infrastructure.mongodb.LocalizacaoRepository;
import org.modelmapper.ModelMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ImplLocalizacaoService implements LocalizacaoService {

    private static final Logger logger = LoggerFactory.getLogger(ImplLocalizacaoService.class);

    @Autowired
    private LocalizacaoRepository localizacaoRepository;

    @Autowired
    private ValidationService validation;

    @Autowired
    private ModelMapper mapper;

    @Autowired
    private AreaSeguraService areaSeguraService;

    @Autowired
    private NotificationService notificationService;

    @Override
    public LocalizacaoResDTO save(LocalizacaoReqDTO localizacaoReq) {
        if (!validation.existAnimal(localizacaoReq.getAnimal())) {
            logger.error("Falha ao salvar localização: Animal ID {} não encontrado", localizacaoReq.getAnimal());
            throw new ResourceNotFoundException("Animal", "ID", localizacaoReq.getAnimal());
        }

        if (!validation.existColeira(localizacaoReq.getColeira())) {
            logger.error("Falha ao salvar localização: Coleira ID {} não encontrada", localizacaoReq.getColeira());
            throw new ResourceNotFoundException("Coleira", "ID", localizacaoReq.getColeira());
        }

        logger.info("Salvando localização para o animal: {} (Lat: {}, Lng: {})", 
                localizacaoReq.getAnimal(), localizacaoReq.getLatitude(), localizacaoReq.getLongitude());

        Localizacao localizacaoSalva = localizacaoRepository.save(mapper.map(localizacaoReq, Localizacao.class));
        LocalizacaoResDTO localizacaoResDTO = mapper.map(localizacaoSalva, LocalizacaoResDTO.class);

        boolean isForaDaAreaSegura = areaSeguraService.isForaDaAreaSegura(
                localizacaoReq.getAnimal(),
                localizacaoReq.getLatitude(),
                localizacaoReq.getLongitude()
        );

        Double distanciaDoPerimetro = null;
        Optional<AreaSeguraResDTO> areaSeguraOpt = areaSeguraService.findByAnimalId(localizacaoReq.getAnimal());
        if (areaSeguraOpt.isPresent()) {
            AreaSeguraResDTO areaSegura = areaSeguraOpt.get();
            double distanciaTotal = areaSeguraService.calcularDistanciaEmMetros(
                    areaSegura.getLatitude(),
                    areaSegura.getLongitude(),
                    localizacaoReq.getLatitude(),
                    localizacaoReq.getLongitude()
            );
            distanciaDoPerimetro = distanciaTotal - areaSegura.getRaio();
        }

        localizacaoResDTO.setIsOutsideSafeZone(isForaDaAreaSegura);
        localizacaoResDTO.setDistanciaDoPerimetro(distanciaDoPerimetro);

        LocalizacaoWebSocketDTO webSocketDTO = new LocalizacaoWebSocketDTO(
                localizacaoReq.getAnimal(),
                localizacaoReq.getColeira(),
                localizacaoReq.getLatitude(),
                localizacaoReq.getLongitude(),
                localizacaoReq.getData(),
                isForaDaAreaSegura,
                distanciaDoPerimetro
        );

        notificationService.enviarNotificacaoLocalizacao(
                localizacaoReq.getAnimal(),
                webSocketDTO
        );

        return localizacaoResDTO;
    }

    @Override
    public LocalizacaoResDTO fidById(String localizacaoId) {
        Optional<Localizacao> localizacaoOpt = localizacaoRepository.findById(localizacaoId);

        return localizacaoOpt.map(localizacao -> {
            LocalizacaoResDTO localizacaoResDTO = mapper.map(localizacao, LocalizacaoResDTO.class);

            boolean isForaDaAreaSegura = areaSeguraService.isForaDaAreaSegura(
                    localizacao.getAnimal(),
                    localizacao.getLatitude(),
                    localizacao.getLongitude()
            );
            localizacaoResDTO.setIsOutsideSafeZone(isForaDaAreaSegura);

            Double distanciaDoPerimetro = null;
            Optional<AreaSeguraResDTO> areaSeguraOpt = areaSeguraService.findByAnimalId(localizacao.getAnimal());
            if (areaSeguraOpt.isPresent()) {
                AreaSeguraResDTO areaSegura = areaSeguraOpt.get();
                double distanciaTotal = areaSeguraService.calcularDistanciaEmMetros(
                        areaSegura.getLatitude(),
                        areaSegura.getLongitude(),
                        localizacao.getLatitude(),
                        localizacao.getLongitude()
                );
                distanciaDoPerimetro = distanciaTotal - areaSegura.getRaio();
            }
            localizacaoResDTO.setDistanciaDoPerimetro(distanciaDoPerimetro);

            return localizacaoResDTO;
        }).orElse(null);
    }

    @Override
    public Page<LocalizacaoResDTO> findAllByAnimalId(String animalId, PageDTO pageDTO) {
        pageDTO.sortByNewest();
        Page<Localizacao> localizacaosPage = localizacaoRepository.findAllByAnimal(animalId, pageDTO.mapPage());

        List<LocalizacaoResDTO> dtoList = localizacaosPage.getContent().stream()
                .map(localizacao -> {
                    LocalizacaoResDTO localizacaoResDTO = mapper.map(localizacao, LocalizacaoResDTO.class);

                    boolean isForaDaAreaSegura = areaSeguraService.isForaDaAreaSegura(
                            animalId,
                            localizacao.getLatitude(),
                            localizacao.getLongitude()
                    );
                    localizacaoResDTO.setIsOutsideSafeZone(isForaDaAreaSegura);

                    Double distanciaDoPerimetro = null;
                    Optional<AreaSeguraResDTO> areaSeguraOpt = areaSeguraService.findByAnimalId(animalId);
                    if (areaSeguraOpt.isPresent()) {
                        AreaSeguraResDTO areaSegura = areaSeguraOpt.get();
                        double distanciaTotal = areaSeguraService.calcularDistanciaEmMetros(
                                areaSegura.getLatitude(),
                                areaSegura.getLongitude(),
                                localizacao.getLatitude(),
                                localizacao.getLongitude()
                        );
                        distanciaDoPerimetro = distanciaTotal - areaSegura.getRaio();
                    }
                    localizacaoResDTO.setDistanciaDoPerimetro(distanciaDoPerimetro);

                    return localizacaoResDTO;
                })
                .toList();

        return new PageImpl<LocalizacaoResDTO>(dtoList, pageDTO.mapPage(), localizacaosPage.getTotalElements());
    }

    @Override
    public Page<LocalizacaoResDTO> findAllByColeiraId(String coleiraId, PageDTO pageDTO) {
        pageDTO.sortByNewest();
        Page<Localizacao> localizacaosPage = localizacaoRepository.findAllByColeira(coleiraId, pageDTO.mapPage());

        List<LocalizacaoResDTO> dtoList = localizacaosPage.getContent().stream()
                .map(localizacao -> {
                    LocalizacaoResDTO localizacaoResDTO = mapper.map(localizacao, LocalizacaoResDTO.class);

                    boolean isForaDaAreaSegura = areaSeguraService.isForaDaAreaSegura(
                            localizacao.getAnimal(),
                            localizacao.getLatitude(),
                            localizacao.getLongitude()
                    );
                    localizacaoResDTO.setIsOutsideSafeZone(isForaDaAreaSegura);

                    Double distanciaDoPerimetro = null;
                    Optional<AreaSeguraResDTO> areaSeguraOpt = areaSeguraService.findByAnimalId(localizacao.getAnimal());
                    if (areaSeguraOpt.isPresent()) {
                        AreaSeguraResDTO areaSegura = areaSeguraOpt.get();
                        double distanciaTotal = areaSeguraService.calcularDistanciaEmMetros(
                                areaSegura.getLatitude(),
                                areaSegura.getLongitude(),
                                localizacao.getLatitude(),
                                localizacao.getLongitude()
                        );
                        distanciaDoPerimetro = distanciaTotal - areaSegura.getRaio();
                    }
                    localizacaoResDTO.setDistanciaDoPerimetro(distanciaDoPerimetro);

                    return localizacaoResDTO;
                })
                .toList();

        return new PageImpl<LocalizacaoResDTO>(dtoList, pageDTO.mapPage(), localizacaosPage.getTotalElements());
    }

    @Override
    public Optional<LocalizacaoResDTO> findLastByAnimalId(String animalId) {
        Optional<Localizacao> ultimaLocalizacao = localizacaoRepository.findFirstByAnimalOrderByDataDesc(animalId);

        return ultimaLocalizacao.map(localizacao -> {
            LocalizacaoResDTO localizacaoResDTO = mapper.map(localizacao, LocalizacaoResDTO.class);

            boolean isForaDaAreaSegura = areaSeguraService.isForaDaAreaSegura(
                    animalId,
                    localizacao.getLatitude(),
                    localizacao.getLongitude()
            );
            localizacaoResDTO.setIsOutsideSafeZone(isForaDaAreaSegura);

            Double distanciaDoPerimetro = null;
            Optional<AreaSeguraResDTO> areaSeguraOpt = areaSeguraService.findByAnimalId(animalId);
            if (areaSeguraOpt.isPresent()) {
                AreaSeguraResDTO areaSegura = areaSeguraOpt.get();
                double distanciaTotal = areaSeguraService.calcularDistanciaEmMetros(
                        areaSegura.getLatitude(),
                        areaSegura.getLongitude(),
                        localizacao.getLatitude(),
                        localizacao.getLongitude()
                );
                distanciaDoPerimetro = distanciaTotal - areaSegura.getRaio();
            }
            localizacaoResDTO.setDistanciaDoPerimetro(distanciaDoPerimetro);

            return localizacaoResDTO;
        });
    }

}
