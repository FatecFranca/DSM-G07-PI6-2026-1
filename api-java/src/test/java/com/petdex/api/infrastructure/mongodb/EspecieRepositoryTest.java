package com.petdex.api.infrastructure.mongodb;

import com.petdex.api.domain.collections.Especie;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.data.mongo.DataMongoTest;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.test.context.ActiveProfiles;

import java.util.Optional;

@DataMongoTest
@ActiveProfiles("test")
public class EspecieRepositoryTest {

    @Autowired
    private EspecieRepository repository;

    @Autowired
    private MongoTemplate mongoTemplate;

    @BeforeEach
    public void setup() {
        mongoTemplate.dropCollection(Especie.class);
    }

    @Test
    public void devePersistirUmaEspecieNaBaseDeDados() {
        // cenário
        Especie especie = criarEspecie();

        // ação
        Especie especieSalva = repository.save(especie);

        // verificação
        Assertions.assertThat(especieSalva.getId()).isNotNull();
        Assertions.assertThat(especieSalva.getNome()).isEqualTo("Cachorro");
    }

    @Test
    public void deveBuscarUmaEspeciePorId() {
        // cenário
        Especie especie = criarEspecie();
        mongoTemplate.save(especie);

        // ação
        Optional<Especie> result = repository.findById(especie.getId());

        // verificação
        Assertions.assertThat(result.isPresent()).isTrue();
        Assertions.assertThat(result.get().getNome()).isEqualTo("Cachorro");
    }

    public static Especie criarEspecie() {
        return new Especie("Cachorro");
    }
}
