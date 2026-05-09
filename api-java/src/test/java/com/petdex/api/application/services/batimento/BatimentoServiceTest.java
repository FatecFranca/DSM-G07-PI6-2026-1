package com.petdex.api.application.services.batimento;

import com.petdex.api.application.services.websocket.interfaces.NotificationService;
import com.petdex.api.domain.collections.Batimento;
import com.petdex.api.domain.contracts.dto.batimento.BatimentoReqDTO;
import com.petdex.api.domain.contracts.dto.batimento.BatimentoResDTO;
import com.petdex.api.infrastructure.mongodb.BatimentoRepository;
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
public class BatimentoServiceTest {

    @InjectMocks
    private BatimentoService service;

    @Mock
    private BatimentoRepository repository;

    @Mock
    private NotificationService notificationService;

    @Spy
    private ModelMapper mapper = new ModelMapper();

    @Test
    public void deveSalvarBatimentoEEnviarNotificacao() {
        // cenário
        BatimentoReqDTO req = new BatimentoReqDTO();
        req.setAnimal("animal123");
        req.setFrequenciaMedia(80);
        req.setData(new Date());

        Batimento batimentoSalvo = new Batimento();
        batimentoSalvo.setId("123");
        batimentoSalvo.setAnimal("animal123");

        Mockito.when(repository.save(Mockito.any(Batimento.class))).thenReturn(batimentoSalvo);

        // ação
        BatimentoResDTO result = service.save(req);

        // verificação
        Assertions.assertThat(result).isNotNull();
        Mockito.verify(repository, Mockito.times(1)).save(Mockito.any());
        Mockito.verify(notificationService, Mockito.times(1)).enviarNotificacaoBatimento(Mockito.anyString(), Mockito.any());
    }

    @Test
    public void deveBuscarUltimoBatimentoComSucesso() {
        // cenário
        String animalId = "animal123";
        Batimento batimento = new Batimento();
        batimento.setFrequenciaMedia(90);

        Mockito.when(repository.findFirstByAnimalOrderByDataDesc(animalId)).thenReturn(Optional.of(batimento));

        // ação
        Optional<BatimentoResDTO> result = service.findLastByAnimalId(animalId);

        // verificação
        Assertions.assertThat(result.isPresent()).isTrue();
        Assertions.assertThat(result.get().getFrequenciaMedia()).isEqualTo(90);
    }
}
