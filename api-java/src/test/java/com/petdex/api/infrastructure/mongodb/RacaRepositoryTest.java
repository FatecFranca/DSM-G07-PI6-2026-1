package com.petdex.api.infrastructure.mongodb;

import com.petdex.api.domain.collections.Raca;
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
public class RacaRepositoryTest {

    @Autowired
    private RacaRepository repository;

    @Autowired
    private MongoTemplate mongoTemplate;

    @BeforeEach
    public void setup() {
        mongoTemplate.dropCollection(Raca.class);
    }

    @Test
    public void devePersistirUmaRacaNaBaseDeDados() {
        // cenário
        Raca raca = criarRaca();

        // ação
        Raca racaSalva = repository.save(raca);

        // verificação
        Assertions.assertThat(racaSalva.getId()).isNotNull();
        Assertions.assertThat(racaSalva.getNome()).isEqualTo("Golden Retriever");
    }

    @Test
    public void deveBuscarUmaRacaPorId() {
        // cenário
        Raca raca = criarRaca();
        mongoTemplate.save(raca);

        // ação
        Optional<Raca> result = repository.findById(raca.getId());

        // verificação
        Assertions.assertThat(result.isPresent()).isTrue();
        Assertions.assertThat(result.get().getNome()).isEqualTo("Golden Retriever");
    }

    public static Raca criarRaca() {
        return new Raca("Golden Retriever", "especie123");
    }
}
