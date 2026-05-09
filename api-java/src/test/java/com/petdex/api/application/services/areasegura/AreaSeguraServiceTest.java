package com.petdex.api.application.services.areasegura;

import com.petdex.api.domain.collections.AreaSegura;
import com.petdex.api.domain.contracts.dto.areasegura.AreaSeguraReqDTO;
import com.petdex.api.domain.contracts.dto.areasegura.AreaSeguraResDTO;
import com.petdex.api.infrastructure.mongodb.AreaSeguraRepository;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.Spy;
import org.modelmapper.ModelMapper;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import java.util.Optional;

@ExtendWith(SpringExtension.class)
public class AreaSeguraServiceTest {

    @InjectMocks
    private AreaSeguraService service;

    @Mock
    private AreaSeguraRepository repository;

    @Spy
    private ModelMapper mapper = new ModelMapper();

    @Test
    public void deveCriarAreaSeguraComSucesso() {
        // cenário
        AreaSeguraReqDTO req = new AreaSeguraReqDTO("animal123", -23.55, -46.63, 500.0);
        Mockito.when(repository.findByAnimal("animal123")).thenReturn(Optional.empty());
        Mockito.when(repository.save(Mockito.any(AreaSegura.class))).thenAnswer(i -> i.getArguments()[0]);

        // ação
        AreaSeguraResDTO result = service.createOrUpdate(req);

        // verificação
        Assertions.assertThat(result).isNotNull();
        Assertions.assertThat(result.getAnimal()).isEqualTo("animal123");
        Mockito.verify(repository, Mockito.times(1)).save(Mockito.any());
    }

    @Test
    public void deveDetectarQuandoEstaForaDaAreaSegura() {
        // cenário
        String animalId = "animal123";
        AreaSegura area = new AreaSegura(animalId, -23.550520, -46.633308, 100.0);
        Mockito.when(repository.findByAnimal(animalId)).thenReturn(Optional.of(area));

        // Ponto bem longe (fora do raio de 100m)
        double latFora = -23.60;
        double lonFora = -46.70;

        // ação
        boolean isFora = service.isForaDaAreaSegura(animalId, latFora, lonFora);

        // verificação
        Assertions.assertThat(isFora).isTrue();
    }

    @Test
    public void deveDetectarQuandoEstaDentroDaAreaSegura() {
        // cenário
        String animalId = "animal123";
        AreaSegura area = new AreaSegura(animalId, -23.550520, -46.633308, 1000.0);
        Mockito.when(repository.findByAnimal(animalId)).thenReturn(Optional.of(area));

        // Ponto bem perto
        double latDentro = -23.550521;
        double lonDentro = -46.633309;

        // ação
        boolean isFora = service.isForaDaAreaSegura(animalId, latDentro, lonDentro);

        // verificação
        Assertions.assertThat(isFora).isFalse();
    }
}
