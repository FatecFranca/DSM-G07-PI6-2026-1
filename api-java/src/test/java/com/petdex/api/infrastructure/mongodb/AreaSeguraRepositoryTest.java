package com.petdex.api.infrastructure.mongodb;

import com.petdex.api.domain.collections.AreaSegura;
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
public class AreaSeguraRepositoryTest {

    @Autowired
    private AreaSeguraRepository repository;

    @Autowired
    private MongoTemplate mongoTemplate;

    @BeforeEach
    public void setup() {
        mongoTemplate.dropCollection(AreaSegura.class);
    }

    @Test
    public void devePersistirUmaAreaSeguraNaBaseDeDados() {
        // cenário
        AreaSegura areaSegura = criarAreaSegura();

        // ação
        AreaSegura areaSalva = repository.save(areaSegura);

        // verificação
        Assertions.assertThat(areaSalva.getId()).isNotNull();
        Assertions.assertThat(areaSalva.getAnimal()).isEqualTo("animal123");
    }

    @Test
    public void deveBuscarUmaAreaSeguraPorAnimal() {
        // cenário
        AreaSegura areaSegura = criarAreaSegura();
        mongoTemplate.save(areaSegura);

        // ação
        Optional<AreaSegura> result = repository.findByAnimal("animal123");

        // verificação
        Assertions.assertThat(result.isPresent()).isTrue();
        Assertions.assertThat(result.get().getAnimal()).isEqualTo("animal123");
    }

    @Test
    public void deveVerificarAExistenciaDeAreaSeguraPorAnimal() {
        // cenário
        AreaSegura areaSegura = criarAreaSegura();
        mongoTemplate.save(areaSegura);

        // ação
        boolean result = repository.existsByAnimal("animal123");

        // verificação
        Assertions.assertThat(result).isTrue();
    }

    @Test
    public void deveRetornarFalsoQuandoNaoHouverAreaSeguraParaOAnimal() {
        // cenário

        // ação
        boolean result = repository.existsByAnimal("animal123");

        // verificação
        Assertions.assertThat(result).isFalse();
    }

    @Test
    public void deveDeletarAreaSeguraPorAnimal() {
        // cenário
        AreaSegura areaSegura = criarAreaSegura();
        mongoTemplate.save(areaSegura);

        // ação
        repository.deleteByAnimal("animal123");
        Optional<AreaSegura> result = repository.findByAnimal("animal123");

        // verificação
        Assertions.assertThat(result.isPresent()).isFalse();
    }

    public static AreaSegura criarAreaSegura() {
        return new AreaSegura(
                "animal123",
                -23.550520,
                -46.633308,
                500.0
        );
    }
}
