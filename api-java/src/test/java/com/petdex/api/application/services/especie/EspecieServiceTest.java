package com.petdex.api.application.services.especie;

import com.petdex.api.domain.collections.Especie;
import com.petdex.api.application.contracts.dto.especie.EspecieReqDTO;
import com.petdex.api.application.contracts.dto.especie.EspecieResDTO;
import com.petdex.api.infrastructure.mongodb.EspecieRepository;
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
public class EspecieServiceTest {

    @InjectMocks
    private ImplEspecieService service;

    @Mock
    private EspecieRepository repository;

    @Spy
    private ModelMapper mapper = new ModelMapper();

    @Test
    public void deveBuscarEspeciePorIdComSucesso() {
        // cenário
        String id = "123";
        Especie especie = new Especie("Gato");
        especie.setId(id);

        Mockito.when(repository.findById(id)).thenReturn(Optional.of(especie));

        // ação
        EspecieResDTO result = service.findById(id);

        // verificação
        Assertions.assertThat(result).isNotNull();
        Assertions.assertThat(result.getNome()).isEqualTo("Gato");
    }

    @Test
    public void deveCriarEspecieComSucesso() {
        // cenário
        EspecieReqDTO req = new EspecieReqDTO("Cachorro");
        Especie especieSalva = new Especie("Cachorro");
        especieSalva.setId("123");

        Mockito.when(repository.save(Mockito.any(Especie.class))).thenReturn(especieSalva);

        // ação
        EspecieResDTO result = service.create(req);

        // verificação
        Assertions.assertThat(result).isNotNull();
        Assertions.assertThat(result.getNome()).isEqualTo("Cachorro");
        Mockito.verify(repository, Mockito.times(1)).save(Mockito.any());
    }
}
