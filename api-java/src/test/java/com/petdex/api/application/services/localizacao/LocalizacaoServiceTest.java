package com.petdex.api.application.services.localizacao;

import com.petdex.api.application.services.areasegura.AreaSeguraService;
import com.petdex.api.application.contracts.websocket.NotificationService;
import com.petdex.api.domain.collections.Localizacao;
import com.petdex.api.application.contracts.dto.areasegura.AreaSeguraResDTO;
import com.petdex.api.application.contracts.dto.localizacao.LocalizacaoReqDTO;
import com.petdex.api.application.contracts.dto.localizacao.LocalizacaoResDTO;
import com.petdex.api.infrastructure.mongodb.LocalizacaoRepository;
import com.petdex.api.application.services.ValidationService;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.Spy;
import org.modelmapper.ModelMapper;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import java.util.Date;
import java.util.Optional;

@ExtendWith(SpringExtension.class)
public class LocalizacaoServiceTest {

    @InjectMocks
    private ImplLocalizacaoService service;

    @Mock
    private LocalizacaoRepository repository;

    @Mock
    private AreaSeguraService areaSeguraService;

    @Mock
    private NotificationService notificationService;

    @Mock
    private ValidationService validation;

    @Spy
    private ModelMapper mapper = new ModelMapper();

    @Test
    public void deveSalvarLocalizacaoEVerificarAreaSegura() {
        // cenário
        LocalizacaoReqDTO req = new LocalizacaoReqDTO();
        req.setAnimal("animal123");
        req.setColeira("coleira123");
        req.setLatitude(-23.55);
        req.setLongitude(-46.63);
        req.setData(new Date());

        Localizacao localizacaoSalva = new Localizacao();
        localizacaoSalva.setId("123");
        localizacaoSalva.setAnimal("animal123");

        AreaSeguraResDTO area = new AreaSeguraResDTO();
        area.setLatitude(-23.55);
        area.setLongitude(-46.63);
        area.setRaio(100.0);

        Mockito.when(repository.save(Mockito.any(Localizacao.class))).thenReturn(localizacaoSalva);
        Mockito.when(areaSeguraService.isForaDaAreaSegura(Mockito.anyString(), Mockito.anyDouble(), Mockito.anyDouble())).thenReturn(false);
        Mockito.when(areaSeguraService.findByAnimalId("animal123")).thenReturn(Optional.of(area));
        Mockito.when(areaSeguraService.calcularDistanciaEmMetros(Mockito.anyDouble(), Mockito.anyDouble(), Mockito.anyDouble(), Mockito.anyDouble())).thenReturn(50.0);
        Mockito.when(validation.existAnimal(Mockito.anyString())).thenReturn(true);
        Mockito.when(validation.existColeira(Mockito.anyString())).thenReturn(true);

        // ação
        LocalizacaoResDTO result = service.save(req);

        // verificação
        Assertions.assertThat(result).isNotNull();
        Assertions.assertThat(result.getIsOutsideSafeZone()).isFalse();
        Mockito.verify(repository, Mockito.times(1)).save(Mockito.any());
        Mockito.verify(notificationService, Mockito.times(1)).enviarNotificacaoLocalizacao(Mockito.anyString(), Mockito.any());
    }
}
