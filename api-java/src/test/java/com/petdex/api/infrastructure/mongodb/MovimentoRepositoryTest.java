package com.petdex.api.infrastructure.mongodb;

import com.petdex.api.domain.collections.Movimento;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.data.mongo.DataMongoTest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.test.context.ActiveProfiles;

import java.util.Date;

@DataMongoTest
@ActiveProfiles("test")
public class MovimentoRepositoryTest {

    @Autowired
    private MovimentoRepository repository;

    @Autowired
    private MongoTemplate mongoTemplate;

    @BeforeEach
    public void setup() {
        mongoTemplate.dropCollection(Movimento.class);
    }

    @Test
    public void devePersistirUmMovimentoNaBaseDeDados() {
        // cenário
        Movimento movimento = criarMovimento();

        // ação
        Movimento movimentoSalvo = repository.save(movimento);

        // verificação
        Assertions.assertThat(movimentoSalvo.getId()).isNotNull();
    }

    @Test
    public void deveBuscarMovimentosPorAnimal() {
        // cenário
        Movimento movimento = criarMovimento();
        mongoTemplate.save(movimento);

        // ação
        Page<Movimento> result = repository.findAllByAnimal("animal123", PageRequest.of(0, 10));

        // verificação
        Assertions.assertThat(result.getContent()).isNotEmpty();
        Assertions.assertThat(result.getContent().get(0).getAnimal()).isEqualTo("animal123");
    }

    public static Movimento criarMovimento() {
        return new Movimento(
                new Date(),
                1.0, 2.0, 3.0,
                0.1, 0.2, 0.3,
                "animal123",
                "coleira123"
        );
    }
}
