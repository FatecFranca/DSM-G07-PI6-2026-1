package com.petdex.api.application.services.usuario;

import com.petdex.api.application.services.security.PasswordService;
import com.petdex.api.domain.collections.Usuario;
import com.petdex.api.domain.contracts.dto.usuario.UsuarioReqDTO;
import com.petdex.api.domain.contracts.dto.usuario.UsuarioResDTO;
import com.petdex.api.infrastructure.exception.ConflictException;
import com.petdex.api.infrastructure.mongodb.UsuarioRepository;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.Spy;
import org.modelmapper.ModelMapper;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import java.util.Optional;

@ExtendWith(SpringExtension.class)
public class UsuarioServiceTest {

    @InjectMocks
    private UsuarioService service;

    @Mock
    private UsuarioRepository repository;

    @Mock
    private PasswordService passwordService;

    @Spy
    private ModelMapper mapper = new ModelMapper();

    @Test
    public void deveLancarErroAoCriarUsuarioComEmailJaCadastrado() {
        // cenário
        UsuarioReqDTO req = new UsuarioReqDTO("John", "123", "123", "existente@email.com", "123");
        Usuario usuarioExistente = new Usuario();
        usuarioExistente.setEmail("existente@email.com");

        Mockito.when(repository.findByEmail("existente@email.com")).thenReturn(Optional.of(usuarioExistente));

        // ação e verificação
        Assertions.assertThatThrownBy(() -> service.create(req))
                .isInstanceOf(ConflictException.class);
        
        Mockito.verify(repository, Mockito.never()).save(Mockito.any());
    }

    @Test
    public void deveCriarUsuarioComSucesso() {
        // cenário
        UsuarioReqDTO req = new UsuarioReqDTO("John", "123.456.789-00", "(11) 99999-9999", "novo@email.com", "senha123");
        Usuario usuarioSalvo = new Usuario("1L", "John", "123.456.789-00", "(11) 99999-9999", "novo@email.com", "hash123");

        Mockito.when(repository.findByEmail("novo@email.com")).thenReturn(Optional.empty());
        Mockito.when(passwordService.hashPassword("senha123")).thenReturn("hash123");
        Mockito.when(repository.save(Mockito.any(Usuario.class))).thenReturn(usuarioSalvo);

        // ação
        UsuarioResDTO result = service.create(req);

        // verificação
        Assertions.assertThat(result).isNotNull();
        Assertions.assertThat(result.getEmail()).isEqualTo("novo@email.com");
        Mockito.verify(repository, Mockito.times(1)).save(Mockito.any());
    }

    @Test
    public void deveDeletarUsuarioComSucesso() {
        // cenário
        String id = "123";
        Usuario usuario = new Usuario();
        usuario.setId(id);
        
        Mockito.when(repository.findById(id)).thenReturn(Optional.of(usuario));
        
        // ação
        service.delete(id);
        
        // verificação
        Mockito.verify(repository, Mockito.times(1)).delete(usuario);
    }

    @Test
    public void deveBuscarPorIdComSucesso() {
        // cenário
        String id = "123";
        Usuario usuario = new Usuario();
        usuario.setId(id);
        usuario.setNome("Teste");

        Mockito.when(repository.findById(id)).thenReturn(Optional.of(usuario));

        // ação
        UsuarioResDTO result = service.findById(id);

        // verificação
        Assertions.assertThat(result).isNotNull();
        Assertions.assertThat(result.getNome()).isEqualTo("Teste");
    }

    @Test
    public void deveAtualizarUsuarioComSucesso() {
        // cenário
        String id = "123";
        UsuarioReqDTO req = new UsuarioReqDTO("Novo Nome", null, null, null, null);
        Usuario usuarioExistente = new Usuario();
        usuarioExistente.setId(id);
        usuarioExistente.setNome("Nome Antigo");

        Mockito.when(repository.findById(id)).thenReturn(Optional.of(usuarioExistente));
        Mockito.when(repository.save(Mockito.any(Usuario.class))).thenAnswer(invocation -> invocation.getArgument(0));

        // ação
        UsuarioResDTO result = service.update(id, req);

        // verificação
        Assertions.assertThat(result.getNome()).isEqualTo("Novo Nome");
        Mockito.verify(repository, Mockito.times(1)).save(Mockito.any());
    }
}
