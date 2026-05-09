package com.petdex.api.infrastructure.mongodb;

import com.petdex.api.domain.collections.Localizacao;
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
public class LocalizacaoRepositoryTest {

    @Autowired
    private LocalizacaoRepository repository;

    @Autowired
    private MongoTemplate mongoTemplate;

    @BeforeEach
    public void setup() {
        mongoTemplate.dropCollection(Localizacao.class);
    }

    @Test
    public void devePersistirUmaLocalizacaoNaBaseDeDados() {
        // cenário
        Localizacao localizacao = criarLocalizacao();

        // ação
        Localizacao localizacaoSalva = repository.save(localizacao);

        // verificação
        Assertions.assertThat(localizacaoSalva.getId()).isNotNull();
    }

    @Test
    public void deveBuscarLocalizacoesPorAnimal() {
        // cenário
        Localizacao localizacao = criarLocalizacao();
        mongoTemplate.save(localizacao);

        // ação
        Page<Localizacao> result = repository.findAllByAnimal("animal123", PageRequest.of(0, 10));

        // verificação
        Assertions.assertThat(result.getContent()).isNotEmpty();
        Assertions.assertThat(result.getContent().get(0).getAnimal()).isEqualTo("animal123");
    }

    @Test
    public void deveBuscarUltimaLocalizacaoPorAnimal() {
        // cenário
        Localizacao l1 = new Localizacao(new Date(System.currentTimeMillis() - 10000), -23.55, -46.63, "animal123", "coleira123");
        Localizacao l2 = new Localizacao(new Date(), -23.56, -46.64, "animal123", "coleira123");
        mongoTemplate.save(l1);
        mongoTemplate.save(l2);

        // ação
        Optional<Localizacao> result = repository.findFirstByAnimalOrderByDataDesc("animal123");

        // verificação
        Assertions.assertThat(result.isPresent()).isTrue();
        Assertions.assertThat(result.get().getLatitude()).isEqualTo(-23.56);
    }

    public static Localizacao criarLocalizacao() {
        return new Localizacao(
                new Date(),
                -23.550520,
                -46.633308,
                "animal123",
                "coleira123"
        );
    }
}
