package com.petdex.api.application.services.animal;

import com.petdex.api.domain.collections.Animal;
import com.petdex.api.domain.collections.Especie;
import com.petdex.api.domain.collections.Raca;
import com.petdex.api.application.contracts.dto.animal.AnimalReqDTO;
import com.petdex.api.application.contracts.dto.animal.AnimalResDTO;
import com.petdex.api.infrastructure.exception.ResourceNotFoundException;
import com.petdex.api.infrastructure.mongodb.AnimalRepository;
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

import java.io.IOException;
import java.util.Optional;

@ExtendWith(SpringExtension.class)
public class AnimalServiceTest {

    @InjectMocks
    private ImplAnimalService service;

    @Mock
    private AnimalRepository animalRepository;

    @Mock
    private EspecieRepository especieRepository;

    @Mock
    private RacaRepository racaRepository;

    @Spy
    private ModelMapper mapper = new ModelMapper();

    @Test
    public void deveBuscarAnimalPorIdComSucesso() {
        // cenário
        String id = "123";
        Animal animal = new Animal();
        animal.setId(id);
        animal.setRaca("raca123");

        Raca raca = new Raca();
        raca.setId("raca123");
        raca.setNome("Poodle");
        raca.setEspecie("especie123");

        Especie especie = new Especie();
        especie.setId("especie123");
        especie.setNome("Cachorro");

        Mockito.when(animalRepository.findById(id)).thenReturn(Optional.of(animal));
        Mockito.when(racaRepository.findById("raca123")).thenReturn(Optional.of(raca));
        Mockito.when(especieRepository.findById("especie123")).thenReturn(Optional.of(especie));

        // ação
        AnimalResDTO result = service.findById(id);

        // verificação
        Assertions.assertThat(result).isNotNull();
        Assertions.assertThat(result.getRacaNome()).isEqualTo("Poodle");
        Assertions.assertThat(result.getEspecieNome()).isEqualTo("Cachorro");
    }

    @Test
    public void deveLancarErroAoBuscarAnimalInexistente() {
        // cenário
        String id = "123";
        Mockito.when(animalRepository.findById(id)).thenReturn(Optional.empty());

        // ação e verificação
        Assertions.assertThatThrownBy(() -> service.findById(id))
                .isInstanceOf(ResourceNotFoundException.class);
    }

    @Test
    public void deveCriarAnimalComSucesso() throws IOException {
        // cenário
        AnimalReqDTO req = new AnimalReqDTO();
        req.setNome("Rex");
        
        Animal animalSalvo = new Animal();
        animalSalvo.setId("123");
        animalSalvo.setNome("Rex");

        Mockito.when(animalRepository.save(Mockito.any(Animal.class))).thenReturn(animalSalvo);

        // ação
        AnimalResDTO result = service.create(req);

        // verificação
        Assertions.assertThat(result).isNotNull();
        Assertions.assertThat(result.getNome()).isEqualTo("Rex");
        Mockito.verify(animalRepository, Mockito.times(1)).save(Mockito.any());
    }

    @Test
    public void deveDeletarAnimalComSucesso() {
        // cenário
        String id = "123";

        // ação
        service.delete(id);

        // verificação
        Mockito.verify(animalRepository, Mockito.times(1)).deleteById(id);
    }
}
