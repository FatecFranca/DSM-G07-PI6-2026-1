package com.petdex.api.application.services.coleira;

import com.petdex.api.domain.collections.Animal;
import com.petdex.api.domain.collections.Coleira;
import com.petdex.api.domain.contracts.dto.coleira.ColeiraReqDTO;
import com.petdex.api.domain.contracts.dto.coleira.ColeiraResDTO;
import com.petdex.api.infrastructure.mongodb.AnimalRepository;
import com.petdex.api.infrastructure.mongodb.ColeiraRepository;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.Spy;
import org.modelmapper.ModelMapper;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.web.client.HttpServerErrorException;

import java.util.Optional;

@ExtendWith(SpringExtension.class)
public class ColeiraServiceTest {

    @InjectMocks
    private ColeiraService service;

    @Mock
    private ColeiraRepository repository;

    @Mock
    private AnimalRepository animalRepository;

    @Spy
    private ModelMapper mapper = new ModelMapper();

    @Test
    public void deveBuscarColeiraPorIdComSucesso() {
        // cenário
        String id = "123";
        Coleira coleira = new Coleira();
        coleira.setId(id);
        coleira.setDescricao("Teste");

        Mockito.when(repository.findById(id)).thenReturn(Optional.of(coleira));

        // ação
        ColeiraResDTO result = service.findById(id);

        // verificação
        Assertions.assertThat(result).isNotNull();
        Assertions.assertThat(result.getDescricao()).isEqualTo("Teste");
    }

    @Test
    public void deveCriarColeiraComSucesso() {
        // cenário
        ColeiraReqDTO req = new ColeiraReqDTO();
        req.setAnimal("animal123");
        req.setDescricao("Minha Coleira");

        Animal animal = new Animal();
        animal.setId("animal123");

        Mockito.when(animalRepository.findById("animal123")).thenReturn(Optional.of(animal));
        Mockito.when(repository.save(Mockito.any(Coleira.class))).thenAnswer(i -> i.getArguments()[0]);

        // ação
        ColeiraResDTO result = service.create(req);

        // verificação
        Assertions.assertThat(result).isNotNull();
        Assertions.assertThat(result.getDescricao()).isEqualTo("Minha Coleira");
        Mockito.verify(repository, Mockito.times(1)).save(Mockito.any());
    }

    @Test
    public void deveLancarErroAoCriarColeiraParaAnimalInexistente() {
        // cenário
        ColeiraReqDTO req = new ColeiraReqDTO();
        req.setAnimal("inexistente");

        Mockito.when(animalRepository.findById("inexistente")).thenReturn(Optional.empty());

        // ação e verificação
        Assertions.assertThatThrownBy(() -> service.create(req))
                .isInstanceOf(HttpServerErrorException.class);
    }
}
