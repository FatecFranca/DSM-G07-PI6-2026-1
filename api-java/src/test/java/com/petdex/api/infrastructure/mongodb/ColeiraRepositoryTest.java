package com.petdex.api.infrastructure.mongodb;

import com.petdex.api.domain.collections.Coleira;
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
public class ColeiraRepositoryTest {

    @Autowired
    private ColeiraRepository repository;

    @Autowired
    private MongoTemplate mongoTemplate;

    @BeforeEach
    public void setup() {
        mongoTemplate.dropCollection(Coleira.class);
    }

    @Test
    public void devePersistirUmaColeiraNaBaseDeDados() {
        // cenário
        Coleira coleira = criarColeira();

        // ação
        Coleira coleiraSalva = repository.save(coleira);

        // verificação
        Assertions.assertThat(coleiraSalva.getId()).isNotNull();
        Assertions.assertThat(coleiraSalva.getDescricao()).isEqualTo("Coleira do Rex");
    }

    @Test
    public void deveBuscarUmaColeiraPorId() {
        // cenário
        Coleira coleira = criarColeira();
        mongoTemplate.save(coleira);

        // ação
        Optional<Coleira> result = repository.findById(coleira.getId());

        // verificação
        Assertions.assertThat(result.isPresent()).isTrue();
        Assertions.assertThat(result.get().getDescricao()).isEqualTo("Coleira do Rex");
    }

    public static Coleira criarColeira() {
        return new Coleira(
                "Coleira do Rex",
                "animal123"
        );
    }
}
