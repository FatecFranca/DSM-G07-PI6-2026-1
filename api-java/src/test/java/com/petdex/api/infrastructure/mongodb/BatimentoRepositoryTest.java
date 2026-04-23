package com.petdex.api.infrastructure.mongodb;

import com.petdex.api.domain.collections.Batimento;
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
import java.util.Optional;

@DataMongoTest
@ActiveProfiles("test")
public class BatimentoRepositoryTest {

    @Autowired
    private BatimentoRepository repository;

    @Autowired
    private MongoTemplate mongoTemplate;

    @BeforeEach
    public void setup() {
        mongoTemplate.dropCollection(Batimento.class);
    }

    @Test
    public void devePersistirUmBatimentoNaBaseDeDados() {
        // cenário
        Batimento batimento = criarBatimento();

        // ação
        Batimento batimentoSalvo = repository.save(batimento);

        // verificação
        Assertions.assertThat(batimentoSalvo.getId()).isNotNull();
    }

    @Test
    public void deveBuscarBatimentosPorAnimal() {
        // cenário
        Batimento batimento = criarBatimento();
        mongoTemplate.save(batimento);

        // ação
        Page<Batimento> result = repository.findAllByAnimal("animal123", PageRequest.of(0, 10));

        // verificação
        Assertions.assertThat(result.getContent()).isNotEmpty();
        Assertions.assertThat(result.getContent().get(0).getAnimal()).isEqualTo("animal123");
    }

    @Test
    public void deveBuscarUltimoBatimentoPorAnimal() {
        // cenário
        Batimento b1 = new Batimento(new Date(System.currentTimeMillis() - 10000), 80, "animal123", "coleira123");
        Batimento b2 = new Batimento(new Date(), 90, "animal123", "coleira123");
        mongoTemplate.save(b1);
        mongoTemplate.save(b2);

        // ação
        Optional<Batimento> result = repository.findFirstByAnimalOrderByDataDesc("animal123");

        // verificação
        Assertions.assertThat(result.isPresent()).isTrue();
        Assertions.assertThat(result.get().getFrequenciaMedia()).isEqualTo(90);
    }

    public static Batimento criarBatimento() {
        return new Batimento(
                new Date(),
                80,
                "animal123",
                "coleira123"
        );
    }
}
