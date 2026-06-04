package com.petdex.api.infrastructure.mongodb;

import com.petdex.api.domain.collections.Animal;
import com.petdex.api.domain.collections.PorteEnum;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.data.mongo.DataMongoTest;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.test.context.ActiveProfiles;

import java.util.Date;
import java.util.Optional;

@DataMongoTest
@ActiveProfiles("test")
public class AnimalRepositoryTest {

    @Autowired
    private AnimalRepository repository;

    @Autowired
    private MongoTemplate mongoTemplate;

    @BeforeEach
    public void setup() {
        mongoTemplate.dropCollection(Animal.class);
    }

    @Test
    public void devePersistirUmAnimalNaBaseDeDados() {
        // cenário
        Animal animal = criarAnimal();

        // ação
        Animal animalSalvo = repository.save(animal);

        // verificação
        Assertions.assertThat(animalSalvo.getId()).isNotNull();
        Assertions.assertThat(animalSalvo.getNome()).isEqualTo("Rex");
        Assertions.assertThat(animalSalvo.getCaminhadaDiariaKm()).isEqualTo(2.5);
        Assertions.assertThat(animalSalvo.getPorte()).isEqualTo(PorteEnum.medio);
    }

    @Test
    public void deveBuscarUmAnimalPorUsuario() {
        // cenário
        Animal animal = criarAnimal();
        mongoTemplate.save(animal);

        // ação
        Optional<Animal> result = repository.findByUsuario("usuario123");

        // verificação
        Assertions.assertThat(result.isPresent()).isTrue();
        Assertions.assertThat(result.get().getUsuario()).isEqualTo("usuario123");
    }

    @Test
    public void deveRetornarVazioAoBuscarUmAnimalPorUsuarioInexistente() {
        // cenário

        // ação
        Optional<Animal> result = repository.findByUsuario("inexistente");

        // verificação
        Assertions.assertThat(result.isPresent()).isFalse();
    }

    public static Animal criarAnimal() {
        Animal animal = new Animal(
                "Rex",
                new Date(),
                "M",
                10.5f,
                true,
                "usuario123",
                "raca123"
        );
        animal.setCaminhadaDiariaKm(2.5);
        animal.setPorte(PorteEnum.medio);
        return animal;
    }
}
