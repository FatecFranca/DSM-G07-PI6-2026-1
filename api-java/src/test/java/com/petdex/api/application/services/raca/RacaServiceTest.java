package com.petdex.api.application.services.raca;

import com.petdex.api.domain.collections.Especie;
import com.petdex.api.domain.collections.Raca;
import com.petdex.api.application.contracts.dto.raca.RacaReqDTO;
import com.petdex.api.application.contracts.dto.raca.RacaResDTO;
import com.petdex.api.infrastructure.mongodb.EspecieRepository;
import com.petdex.api.infrastructure.mongodb.RacaRepository;
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
public class RacaServiceTest {

    @InjectMocks
    private ImplRacaService service;

    @Mock
    private RacaRepository racaRepository;

    @Mock
    private EspecieRepository especieRepository;

    @Spy
    private ModelMapper mapper = new ModelMapper();

    @Test
    public void deveCriarRacaComSucesso() {
        // cenário
        RacaReqDTO req = new RacaReqDTO();
        req.setNome("Golden Retriever");
        req.setEspecie("especie123");

        Especie especie = new Especie();
        especie.setId("especie123");

        Mockito.when(especieRepository.findById("especie123")).thenReturn(Optional.of(especie));
        Mockito.when(racaRepository.save(Mockito.any(Raca.class))).thenAnswer(i -> i.getArguments()[0]);

        // ação
        RacaResDTO result = service.create(req);

        // verificação
        Assertions.assertThat(result).isNotNull();
        Assertions.assertThat(result.getNome()).isEqualTo("Golden Retriever");
        Mockito.verify(racaRepository, Mockito.times(1)).save(Mockito.any());
    }

    @Test
    public void deveLancarErroAoCriarRacaParaEspecieInexistente() {
        // cenário
        RacaReqDTO req = new RacaReqDTO();
        req.setEspecie("inexistente");

        Mockito.when(especieRepository.findById("inexistente")).thenReturn(Optional.empty());

        // ação e verificação
        Assertions.assertThatThrownBy(() -> service.create(req))
                .isInstanceOf(RuntimeException.class);
    }
}
