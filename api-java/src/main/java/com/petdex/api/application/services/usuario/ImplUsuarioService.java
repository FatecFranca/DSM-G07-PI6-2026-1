package com.petdex.api.application.services.usuario;

import com.petdex.api.application.services.security.EncryptionService;
import com.petdex.api.domain.collections.Usuario;
import com.petdex.api.application.contracts.dto.PageDTO;
import com.petdex.api.application.contracts.dto.usuario.UsuarioReqDTO;
import com.petdex.api.application.contracts.dto.usuario.UsuarioResDTO;
import com.petdex.api.infrastructure.exception.ConflictException;
import com.petdex.api.infrastructure.mongodb.UsuarioRepository;
import org.modelmapper.ModelMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ImplUsuarioService implements UsuarioService {

    private static final Logger logger = LoggerFactory.getLogger(ImplUsuarioService.class);
    @Autowired
    ModelMapper mapper;

    @Autowired
    UsuarioRepository usuarioRepository;

    @Autowired
    EncryptionService encryptionService;

    @Override
    public UsuarioResDTO findById(String id) {
        return mapper.map(usuarioRepository.findById(id), UsuarioResDTO.class);
    }

    @Override
    public Page<UsuarioResDTO> findAll(PageDTO pageDTO) {
        pageDTO.sortByName();

        Page<Usuario> usuariosPage = usuarioRepository.findAll(pageDTO.mapPage());
        List<UsuarioResDTO> dtoList = usuariosPage.getContent().stream()
                .map(b -> mapper.map(b, UsuarioResDTO.class))
                .toList();

        return new PageImpl<UsuarioResDTO>(dtoList, pageDTO.mapPage(), usuariosPage.getTotalElements());
    }

    @Override
    public UsuarioResDTO create(UsuarioReqDTO usuarioReqDTO) {
        // Verifica se o email já está cadastrado
        Optional<Usuario> usuarioExistente = usuarioRepository.findByEmail(usuarioReqDTO.getEmail());
        if (usuarioExistente.isPresent()) {
            logger.error("Falha ao criar usuário: O e-mail {} já está cadastrado", usuarioReqDTO.getEmail());
            throw new ConflictException("Usuário", "email", usuarioReqDTO.getEmail());
        }

        // Criptografa a senha antes de salvar
        Usuario usuario = mapper.map(usuarioReqDTO, Usuario.class);
        usuario.setSenha(encryptionService.hashPassword(usuarioReqDTO.getSenha()));

        return mapper.map(usuarioRepository.save(usuario), UsuarioResDTO.class);
    }

    @Override
    public UsuarioResDTO update(String id, UsuarioReqDTO usuarioReqDTO) {

        Usuario usuarioUpdate = usuarioRepository.findById(id).orElseThrow(() -> {
            logger.error("Falha ao atualizar: Usuário não encontrado com ID: {}", id);
            return new RuntimeException("Não foi possível contrar um usuário com este ID: " + id);
        });

        if (usuarioReqDTO.getCpf() != null) usuarioUpdate.setCpf(usuarioReqDTO.getCpf());
        if (usuarioReqDTO.getEmail() != null) usuarioUpdate.setEmail(usuarioReqDTO.getEmail());
        // Criptografa a senha antes de atualizar
        if (usuarioReqDTO.getSenha() != null) usuarioUpdate.setSenha(encryptionService.hashPassword(usuarioReqDTO.getSenha()));
        if (usuarioReqDTO.getNome() != null) usuarioUpdate.setNome(usuarioReqDTO.getNome());
        if (usuarioReqDTO.getWhatsApp() != null) usuarioUpdate.setWhatsApp(usuarioReqDTO.getWhatsApp());

        return mapper.map(usuarioRepository.save(mapper.map(usuarioUpdate, Usuario.class)), UsuarioResDTO.class);
    }

    @Override
    public void delete(String id) {
        Usuario usuario = usuarioRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Usuário não encontrado com id: " + id));
        usuarioRepository.delete(usuario);
    }
}
