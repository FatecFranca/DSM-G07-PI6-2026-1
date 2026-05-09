package com.petdex.api.infrastructure.mongodb;

import com.petdex.api.domain.collections.Usuario;
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
public class UsuarioRepositoryTest {

    @Autowired
    private UsuarioRepository repository;

    @Autowired
    private MongoTemplate mongoTemplate;

    @BeforeEach
    public void setup() {
        mongoTemplate.dropCollection(Usuario.class);
    }

    @Test
    public void deveVerificarAExistenciaDeUmEmail() {
        // cenário
        Usuario usuario = criarUsuario();
        mongoTemplate.save(usuario);

        // ação/execução
        boolean result = repository.existsByEmail("alexandre@fatec.gov.br");

        // verificação
        Assertions.assertThat(result).isTrue();
    }

    @Test
    public void deveRetornarFalsoQuandoNaoHouverUsuarioCadastradoComOEmail() {
        // cenário

        // ação/execução
        boolean result = repository.existsByEmail("alexandre@fatec.gov.br");

        // verificação
        Assertions.assertThat(result).isFalse();
    }

    @Test
    public void devePersistirUmUsuarioNaBaseDeDados() {
        // cenário
        Usuario usuario = criarUsuario();

        // ação
        Usuario usuarioSalvo = repository.save(usuario);

        // verificação
        Assertions.assertThat(usuarioSalvo.getId()).isNotNull();
    }

    @Test
    public void deveBuscarUmUsuarioPorEmail() {
        // cenário
        Usuario usuario = criarUsuario();
        mongoTemplate.save(usuario);

        // ação
        Optional<Usuario> result = repository.findByEmail("alexandre@fatec.gov.br");

        // verificação
        Assertions.assertThat(result.isPresent()).isTrue();
    }

    @Test
    public void deveRetornarVazioAoBuscarUmUsuarioPorEmailQuandoNaoExistirNaBase() {
        // cenário

        // ação
        Optional<Usuario> result = repository.findByEmail("alexandre@fatec.gov.br");

        // verificação
        Assertions.assertThat(result.isPresent()).isFalse();
    }

    public static Usuario criarUsuario() {
        return new Usuario(
                "Alexandre",
                "123.456.789-00",
                "(11) 99999-9999",
                "alexandre@fatec.gov.br",
                "1234"
        );
    }
}
