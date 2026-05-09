package com.petdex.api.application.services.auth;

import com.petdex.api.application.services.security.TokenService;
import com.petdex.api.application.services.security.EncryptionService;
import com.petdex.api.domain.collections.Animal;
import com.petdex.api.domain.collections.Usuario;
import com.petdex.api.application.contracts.dto.auth.LoginReqDTO;
import com.petdex.api.application.contracts.dto.auth.LoginResDTO;
import com.petdex.api.infrastructure.mongodb.AnimalRepository;
import com.petdex.api.infrastructure.mongodb.UsuarioRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class ImplAuthService implements AuthService {

    private static final Logger logger = LoggerFactory.getLogger(ImplAuthService.class);

    @Autowired
    private UsuarioRepository usuarioRepository;

    @Autowired
    private AnimalRepository animalRepository;

    @Autowired
    private EncryptionService encryptionService;

    @Autowired
    private TokenService tokenService;

    @Override
    public LoginResDTO login(LoginReqDTO loginReqDTO) {
        Usuario usuario = usuarioRepository.findByEmail(loginReqDTO.getEmail())
                .orElseThrow(() -> {
                    logger.error("Falha no login: Usuário não encontrado com e-mail {}", loginReqDTO.getEmail());
                    return new RuntimeException("Credenciais inválidas");
                });


        if (!encryptionService.validatePassword(loginReqDTO.getSenha(), usuario.getSenha())) {
            logger.error("Falha no login: Senha incorreta para o usuário {}", loginReqDTO.getEmail());
            throw new RuntimeException("Credenciais inválidas");
        }

        String token = tokenService.generateToken(usuario.getId(), usuario.getEmail());

        Optional<Animal> animalOpt = animalRepository.findByUsuario(usuario.getId());
        String animalId = animalOpt.map(Animal::getId).orElse(null);
        String petName = animalOpt.map(Animal::getNome).orElse(null);
        String animalImagemUrl = animalOpt.map(Animal::getUrlImagem).orElse(null);
        
        return new LoginResDTO(
                token,
                animalId,
                usuario.getId(),
                usuario.getNome(),
                usuario.getEmail(),
                petName,
                animalImagemUrl
        );
    }
}
