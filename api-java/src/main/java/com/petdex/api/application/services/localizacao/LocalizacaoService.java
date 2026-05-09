package com.petdex.api.application.services.localizacao;

import com.petdex.api.application.services.ValidationService;
import com.petdex.api.application.services.areasegura.IAreaSeguraService;
import com.petdex.api.application.services.websocket.interfaces.NotificationService;
import com.petdex.api.domain.collections.AreaSegura;
import com.petdex.api.domain.collections.Localizacao;
import com.petdex.api.domain.contracts.dto.areasegura.AreaSeguraResDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoReqDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoResDTO;
import com.petdex.api.domain.contracts.dto.PageDTO;
import com.petdex.api.domain.contracts.dto.websocket.LocalizacaoWebSocketDTO;
import com.petdex.api.infrastructure.mongodb.LocalizacaoRepository;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class LocalizacaoService implements ILocalizacaoService {

    @Autowired
    private LocalizacaoRepository localizacaoRepository;

    @Autowired
    private ValidationService validation;

    @Autowired
    private ModelMapper mapper;

    @Autowired
    private IAreaSeguraService areaSeguraService;

    @Autowired
    private NotificationService notificationService;

    public LocalizacaoResDTO save(LocalizacaoReqDTO localizacaoReq) {
        System.out.println("╔════════════════════════════════════════════════════════════════╗");
        System.out.println("║ 🔵 LocalizacaoService.save() CHAMADO                          ║");
        System.out.println("╠════════════════════════════════════════════════════════════════╣");
        System.out.println("   Animal: " + localizacaoReq.getAnimal());
        System.out.println("   Lat/Lng: " + localizacaoReq.getLatitude() + ", " + localizacaoReq.getLongitude());
        System.out.println("   Thread: " + Thread.currentThread().getName());
        System.out.println("╚════════════════════════════════════════════════════════════════╝");
//
//        if (!validation.existAnimal(localizacaoReq.getAnimalId()) || !validation.existColeira(localizacaoReq.getColeiraId())) {
//            return null; // Lançar excessão 404
//        }

        // Salva a localização no banco de dados
        Localizacao localizacaoSalva = localizacaoRepository.save(mapper.map(localizacaoReq, Localizacao.class));
        LocalizacaoResDTO localizacaoResDTO = mapper.map(localizacaoSalva, LocalizacaoResDTO.class);

        // Verifica se o animal está fora da área segura
        boolean isForaDaAreaSegura = areaSeguraService.isForaDaAreaSegura(
                localizacaoReq.getAnimal(),
                localizacaoReq.getLatitude(),
                localizacaoReq.getLongitude()
        );

        // Calcula a distância do perímetro (se houver área segura configurada)
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
            // Distância do perímetro = distância total - raio (positivo se fora, negativo se dentro)
            distanciaDoPerimetro = distanciaTotal - areaSegura.getRaio();
        }

        // Define os dados de área segura na resposta
        localizacaoResDTO.setIsOutsideSafeZone(isForaDaAreaSegura);
        localizacaoResDTO.setDistanciaDoPerimetro(distanciaDoPerimetro);

        // Cria o DTO para envio via WebSocket
        LocalizacaoWebSocketDTO webSocketDTO = new LocalizacaoWebSocketDTO(
                localizacaoReq.getAnimal(),
                localizacaoReq.getColeira(),
                localizacaoReq.getLatitude(),
                localizacaoReq.getLongitude(),
                localizacaoReq.getData(),
                isForaDaAreaSegura,
                distanciaDoPerimetro
        );

        // Envia notificação via WebSocket
        notificationService.enviarNotificacaoLocalizacao(
                localizacaoReq.getAnimal(),
                webSocketDTO
        );

        return localizacaoResDTO;
    }

    public LocalizacaoResDTO fidById(String localizacaoId) {
        Optional<Localizacao> localizacaoOpt = localizacaoRepository.findById(localizacaoId);

        return localizacaoOpt.map(localizacao -> {
            LocalizacaoResDTO localizacaoResDTO = mapper.map(localizacao, LocalizacaoResDTO.class);

            // Verifica se o animal está fora da área segura
            boolean isForaDaAreaSegura = areaSeguraService.isForaDaAreaSegura(
                    localizacao.getAnimal(),
                    localizacao.getLatitude(),
                    localizacao.getLongitude()
            );
            localizacaoResDTO.setIsOutsideSafeZone(isForaDaAreaSegura);

            // Calcula a distância do perímetro (se houver área segura configurada)
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
                // Distância do perímetro = distância total - raio (positivo se fora, negativo se dentro)
                distanciaDoPerimetro = distanciaTotal - areaSegura.getRaio();
            }
            localizacaoResDTO.setDistanciaDoPerimetro(distanciaDoPerimetro);

            return localizacaoResDTO;
        }).orElse(null);
    }

    public Page<LocalizacaoResDTO> findAllByAnimalId(String animalId, PageDTO pageDTO) {
        pageDTO.sortByNewest();
        Page<Localizacao> localizacaosPage = localizacaoRepository.findAllByAnimal(animalId, pageDTO.mapPage());

        List<LocalizacaoResDTO> dtoList = localizacaosPage.getContent().stream()
                .map(localizacao -> {
                    LocalizacaoResDTO localizacaoResDTO = mapper.map(localizacao, LocalizacaoResDTO.class);

                    // Verifica se o animal está fora da área segura
                    boolean isForaDaAreaSegura = areaSeguraService.isForaDaAreaSegura(
                            animalId,
                            localizacao.getLatitude(),
                            localizacao.getLongitude()
                    );
                    localizacaoResDTO.setIsOutsideSafeZone(isForaDaAreaSegura);

                    // Calcula a distância do perímetro (se houver área segura configurada)
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
                        // Distância do perímetro = distância total - raio (positivo se fora, negativo se dentro)
                        distanciaDoPerimetro = distanciaTotal - areaSegura.getRaio();
                    }
                    localizacaoResDTO.setDistanciaDoPerimetro(distanciaDoPerimetro);

                    return localizacaoResDTO;
                })
                .toList();

        return new PageImpl<LocalizacaoResDTO>(dtoList, pageDTO.mapPage(), localizacaosPage.getTotalElements());
    }

    public Page<LocalizacaoResDTO> findAllByColeiraId(String coleiraId, PageDTO pageDTO) {
        pageDTO.sortByNewest();
        Page<Localizacao> localizacaosPage = localizacaoRepository.findAllByColeira(coleiraId, pageDTO.mapPage());

        List<LocalizacaoResDTO> dtoList = localizacaosPage.getContent().stream()
                .map(localizacao -> {
                    LocalizacaoResDTO localizacaoResDTO = mapper.map(localizacao, LocalizacaoResDTO.class);

                    // Verifica se o animal está fora da área segura
                    boolean isForaDaAreaSegura = areaSeguraService.isForaDaAreaSegura(
                            localizacao.getAnimal(),
                            localizacao.getLatitude(),
                            localizacao.getLongitude()
                    );
                    localizacaoResDTO.setIsOutsideSafeZone(isForaDaAreaSegura);

                    // Calcula a distância do perímetro (se houver área segura configurada)
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
                        // Distância do perímetro = distância total - raio (positivo se fora, negativo se dentro)
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

            // Verifica se o animal está fora da área segura
            boolean isForaDaAreaSegura = areaSeguraService.isForaDaAreaSegura(
                    animalId,
                    localizacao.getLatitude(),
                    localizacao.getLongitude()
            );
            localizacaoResDTO.setIsOutsideSafeZone(isForaDaAreaSegura);

            // Calcula a distância do perímetro (se houver área segura configurada)
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
                // Distância do perímetro = distância total - raio (positivo se fora, negativo se dentro)
                distanciaDoPerimetro = distanciaTotal - areaSegura.getRaio();
            }
            localizacaoResDTO.setDistanciaDoPerimetro(distanciaDoPerimetro);

            return localizacaoResDTO;
        });
    }

}
